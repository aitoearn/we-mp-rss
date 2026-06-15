const { app, BrowserWindow, dialog, ipcMain, shell, Menu, session } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const net = require('net');
const fs = require('fs');

const APP_NAME = 'WeRSS';
const DEFAULT_PORT = 8001;

/** @type {import('child_process').ChildProcess | null} */
let backendProcess = null;
/** @type {import('electron').BrowserWindow | null} */
let mainWindow = null;
/** @type {number} */
let backendPort = DEFAULT_PORT;
/** @type {boolean} */
let appIsQuitting = false;

/**
 * 项目根目录（开发模式为 electron/ 的上级目录）
 * @returns {string}
 */
function getProjectRoot() {
  if (app.isPackaged) {
    return app.getPath('userData');
  }
  return path.join(__dirname, '..');
}

/**
 * 获取配置模板路径
 * @returns {string}
 */
function getExampleConfigPath() {
  if (app.isPackaged) {
    return path.join(process.resourcesPath, 'config.example.yaml');
  }
  return path.join(__dirname, '..', 'config.example.yaml');
}

/**
 * 桌面应用用户数据目录（配置、数据库、缓存）
 * @returns {string}
 */
function getUserDataRoot() {
  return path.join(app.getPath('userData'), 'we-mp-rss');
}

/**
 * 检查端口是否可用
 * @param {number} port
 * @returns {Promise<boolean>}
 */
function isPortAvailable(port) {
  return new Promise((resolve) => {
    const server = net.createServer();
    server.once('error', () => resolve(false));
    server.once('listening', () => {
      server.close();
      resolve(true);
    });
    server.listen(port, '127.0.0.1');
  });
}

/**
 * 查找可用端口
 * @param {number} startPort
 * @param {number} maxAttempts
 * @returns {Promise<number>}
 */
async function findAvailablePort(startPort = DEFAULT_PORT, maxAttempts = 50) {
  for (let port = startPort; port < startPort + maxAttempts; port += 1) {
    if (await isPortAvailable(port)) {
      return port;
    }
  }
  throw new Error(`无法在 ${startPort}-${startPort + maxAttempts - 1} 范围内找到可用端口`);
}

/**
 * 检查后端 TCP 是否就绪
 * @param {number} port
 * @returns {Promise<boolean>}
 */
function checkBackendHealth(port) {
  return new Promise((resolve) => {
    const client = new net.Socket();
    client.setTimeout(1000);
    client.once('connect', () => {
      client.end();
      resolve(true);
    });
    client.once('error', () => resolve(false));
    client.once('timeout', () => {
      client.destroy();
      resolve(false);
    });
    client.connect(port, '127.0.0.1');
  });
}

/**
 * 等待后端启动
 * @param {number} port
 * @param {number} timeout
 * @returns {Promise<boolean>}
 */
async function waitForBackend(port, timeout = 120000) {
  const startTime = Date.now();
  while (Date.now() - startTime < timeout) {
    if (await checkBackendHealth(port)) {
      console.log(`后端服务已就绪: http://127.0.0.1:${port}`);
      return true;
    }
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  throw new Error(`后端服务启动超时 (${timeout}ms)`);
}

/**
 * 初始化桌面运行环境：用户数据目录、配置文件、数据库目录
 * @returns {{ userDataRoot: string, configPath: string, dataDir: string, dbPath: string, needInit: boolean }}
 */
/**
 * 桌面端登录状态文件路径（跨端口持久化 token）
 * @returns {string}
 */
function getAuthFilePath() {
  return path.join(getUserDataRoot(), 'auth.json');
}

/**
 * @returns {{ token: string, expire?: number } | null}
 */
function readAuthState() {
  const authFile = getAuthFilePath();
  if (!fs.existsSync(authFile)) {
    return null;
  }
  try {
    const raw = JSON.parse(fs.readFileSync(authFile, 'utf-8'));
    if (raw && typeof raw.token === 'string' && raw.token) {
      return raw;
    }
  } catch (error) {
    console.warn('读取登录状态失败:', error);
  }
  return null;
}

/**
 * @param {{ token: string, expire?: number }} state
 */
function writeAuthState(state) {
  fs.mkdirSync(getUserDataRoot(), { recursive: true });
  fs.writeFileSync(getAuthFilePath(), JSON.stringify(state, null, 2), 'utf-8');
}

function clearAuthState() {
  const authFile = getAuthFilePath();
  if (fs.existsSync(authFile)) {
    fs.unlinkSync(authFile);
  }
}

function ensureDesktopEnvironment() {
  const userDataRoot = getUserDataRoot();
  const dataDir = path.join(userDataRoot, 'data');
  const configPath = path.join(userDataRoot, 'config.yaml');
  const dbPath = path.join(dataDir, 'db.db');
  const exampleConfigPath = getExampleConfigPath();

  fs.mkdirSync(dataDir, { recursive: true });

  if (!fs.existsSync(configPath)) {
    if (fs.existsSync(exampleConfigPath)) {
      fs.copyFileSync(exampleConfigPath, configPath);
      // 桌面版默认关闭内嵌 Redis，避免 6379 端口冲突
      fs.appendFileSync(
        configPath,
        '\n# 桌面版默认配置\nredis:\n  server:\n    enabled: false\n'
      );
      console.log(`已创建默认配置: ${configPath}`);
    } else {
      throw new Error(`找不到配置模板: ${exampleConfigPath}`);
    }
  }

  return {
    userDataRoot,
    configPath,
    dataDir,
    dbPath,
    needInit: !fs.existsSync(dbPath)
  };
}

/**
 * 解析 Python 解释器路径
 * @param {string} projectRoot
 * @returns {string}
 */
function resolvePythonExecutable(projectRoot) {
  const candidates = [
    path.join(projectRoot, '.venv', 'bin', 'python'),
    path.join(projectRoot, '.venv', 'Scripts', 'python.exe'),
    process.env.WERSS_PYTHON,
    'python3',
    'python'
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (candidate.includes(path.sep) || candidate.includes('/')) {
      if (fs.existsSync(candidate)) {
        return candidate;
      }
      continue;
    }
    return candidate;
  }

  throw new Error('未找到 Python 解释器，请先创建 .venv 或设置 WERSS_PYTHON 环境变量');
}

/**
 * 启动 Python 后端
 * @returns {Promise<void>}
 */
async function startBackend() {
  const isDev = process.argv.includes('--dev') || !app.isPackaged;
  const projectRoot = path.join(__dirname, '..');
  const { userDataRoot, configPath, dataDir, dbPath, needInit } = ensureDesktopEnvironment();

  backendPort = await findAvailablePort(DEFAULT_PORT);

  const dbUrl = `sqlite:///${dbPath.replace(/\\/g, '/')}`;
  const prefs = readExportPrefs();
  const exportDir = getConfiguredExportDir();
  const baseEnv = {
    ...process.env,
    PORT: String(backendPort),
    DB: dbUrl,
    WERSS_DATA_DIR: dataDir,
    PLAYWRIGHT_BROWSERS_PATH: path.join(dataDir, 'playwright-browsers'),
    PYTHONUTF8: '1',
    PYTHONIOENCODING: 'utf-8',
    WERSS_DESKTOP: '1'
  };
  if (exportDir) {
    baseEnv.WERSS_EXPORT_DIR = exportDir;
  }

  let backendExe;
  let args;
  let cwd;

  if (isDev) {
    backendExe = resolvePythonExecutable(projectRoot);
    const mainScript = path.join(projectRoot, 'main.py');
    if (!fs.existsSync(mainScript)) {
      throw new Error(`找不到后端入口: ${mainScript}`);
    }
    args = [
      mainScript,
      '-config', configPath,
      '-job', 'True',
      '-init', needInit ? 'True' : 'False'
    ];
    cwd = projectRoot;
  } else {
    const backendDir = path.join(process.resourcesPath, 'backend', 'werss-gui');
    backendExe = path.join(
      backendDir,
      process.platform === 'win32' ? 'werss-gui.exe' : 'werss-gui'
    );
    if (!fs.existsSync(backendExe)) {
      throw new Error(`找不到打包后端: ${backendExe}`);
    }
    args = [
      '--port', String(backendPort),
      '--config', configPath,
      '--data-dir', dataDir,
      '--job', 'True',
      '--init', needInit ? 'True' : 'False'
    ];
    cwd = userDataRoot;
  }

  console.log(`启动模式: ${isDev ? '开发' : '生产'}`);
  console.log(`启动后端: ${backendExe} ${args.join(' ')}`);
  console.log(`工作目录: ${cwd}`);
  console.log(`用户数据: ${userDataRoot}`);
  console.log(`监听端口: ${backendPort}`);

  backendProcess = spawn(backendExe, args, {
    env: baseEnv,
    cwd,
    stdio: ['ignore', 'pipe', 'pipe']
  });

  let stderrOutput = '';

  backendProcess.stdout.on('data', (data) => {
    process.stdout.write(`[后端] ${data}`);
  });

  backendProcess.stderr.on('data', (data) => {
    const text = data.toString();
    stderrOutput += text;
    process.stderr.write(`[后端] ${text}`);
  });

  backendProcess.on('error', (error) => {
    console.error('后端进程启动失败:', error);
    dialog.showErrorBox('后端启动失败', `无法启动 WeRSS 后端服务:\n${error.message}`);
    app.quit();
  });

  backendProcess.on('exit', (code, signal) => {
    console.log(`后端进程退出 (code=${code}, signal=${signal})`);
    backendProcess = null;
    if (!appIsQuitting && code !== 0 && code !== null) {
      dialog.showErrorBox(
        '后端异常退出',
        `WeRSS 后端已停止 (code=${code})。\n\n${stderrOutput.slice(-2000)}`
      );
      app.quit();
    }
  });

  await waitForBackend(backendPort);
}

/**
 * 停止后端进程
 * @returns {Promise<void>}
 */
function stopBackend() {
  return new Promise((resolve) => {
    if (!backendProcess || backendProcess.killed) {
      resolve();
      return;
    }

    const proc = backendProcess;
    const timer = setTimeout(() => {
      if (!proc.killed) {
        proc.kill('SIGKILL');
      }
      resolve();
    }, 5000);

    proc.once('exit', () => {
      clearTimeout(timer);
      resolve();
    });

    proc.kill('SIGTERM');
  });
}

/**
 * 创建应用菜单
 */
function createMenu() {
  const template = [
    {
      label: APP_NAME,
      submenu: [
        {
          label: '在浏览器中打开',
          click: () => {
            shell.openExternal(`http://127.0.0.1:${backendPort}`);
          }
        },
        { type: 'separator' },
        { role: 'quit', label: '退出' }
      ]
    },
    {
      label: '视图',
      submenu: [
        { role: 'reload', label: '重新加载' },
        { role: 'forceReload', label: '强制重新加载' },
        { role: 'toggleDevTools', label: '开发者工具' },
        { type: 'separator' },
        { role: 'resetZoom', label: '重置缩放' },
        { role: 'zoomIn', label: '放大' },
        { role: 'zoomOut', label: '缩小' }
      ]
    }
  ];

  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

/**
 * 创建主窗口
 */
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 860,
    minWidth: 960,
    minHeight: 640,
    title: APP_NAME,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      session: session.fromPartition('persist:werss')
    },
    show: false
  });

  const targetUrl = `http://127.0.0.1:${backendPort}`;
  mainWindow.loadURL(targetUrl);

  mainWindow.once('ready-to-show', () => {
    mainWindow?.show();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

function getConfiguredExportDir() {
  const prefs = readExportPrefs();
  if (prefs.defaultExportDir && fs.existsSync(prefs.defaultExportDir)) {
    return prefs.defaultExportDir;
  }
  if (prefs.lastExportDir && fs.existsSync(prefs.lastExportDir)) {
    return prefs.lastExportDir;
  }
  return path.join(getUserDataRoot(), 'data', 'docs', '_all');
}

function getExportPrefsPath() {
  return path.join(getUserDataRoot(), 'export_prefs.json');
}

function readExportPrefs() {
  const prefsFile = getExportPrefsPath();
  if (!fs.existsSync(prefsFile)) {
    return {};
  }
  try {
    return JSON.parse(fs.readFileSync(prefsFile, 'utf-8'));
  } catch (error) {
    console.warn('读取导出偏好失败:', error);
    return {};
  }
}

function writeExportPrefs(prefs) {
  fs.mkdirSync(getUserDataRoot(), { recursive: true });
  fs.writeFileSync(getExportPrefsPath(), JSON.stringify(prefs, null, 2), 'utf-8');
}

ipcMain.handle('dialog-select-export-dir', async (_event, currentDir) => {
  const prefs = readExportPrefs();
  const result = await dialog.showOpenDialog({
    title: '选择导出保存文件夹',
    defaultPath: currentDir || prefs.lastExportDir || getUserDataRoot(),
    properties: ['openDirectory', 'createDirectory']
  });
  if (result.canceled || !result.filePaths.length) {
    return { canceled: true, path: null };
  }
  const selected = result.filePaths[0];
  writeExportPrefs({ ...prefs, lastExportDir: selected });
  return { canceled: false, path: selected };
});

ipcMain.handle('export-get-default-dir', () => getConfiguredExportDir());

ipcMain.handle('export-open-dir', async (_event, dirPath) => {
  if (!dirPath || typeof dirPath !== 'string') {
    return false;
  }
  const resolved = path.resolve(dirPath);
  if (!fs.existsSync(resolved)) {
    return false;
  }
  await shell.openPath(resolved);
  return true;
});

ipcMain.handle('auth-get-state', () => readAuthState());

ipcMain.handle('auth-set-state', (_event, state) => {
  if (!state || typeof state.token !== 'string' || !state.token) {
    throw new Error('无效的登录状态');
  }
  writeAuthState({
    token: state.token,
    expire: typeof state.expire === 'number' ? state.expire : undefined
  });
  return true;
});

ipcMain.handle('auth-clear-state', () => {
  clearAuthState();
  return true;
});

ipcMain.handle('app-relaunch', async () => {
  app.relaunch();
  appIsQuitting = true;
  await stopBackend();
  app.exit(0);
});

ipcMain.handle('app-get-paths', () => ({
  projectRoot: getProjectRoot(),
  userDataRoot: getUserDataRoot(),
  backendPort
}));

const gotSingleInstanceLock = app.requestSingleInstanceLock();
if (!gotSingleInstanceLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) {
        mainWindow.restore();
      }
      mainWindow.focus();
    }
  });

  app.whenReady().then(async () => {
    try {
      await startBackend();
      createMenu();
      createWindow();
    } catch (error) {
      console.error('应用启动失败:', error);
      dialog.showErrorBox('启动失败', `${error.message}`);
      app.quit();
    }
  });

  app.on('before-quit', async (event) => {
    if (appIsQuitting) {
      return;
    }
    event.preventDefault();
    appIsQuitting = true;
    await stopBackend();
    app.quit();
  });

  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit();
    }
  });

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0 && backendProcess) {
      createWindow();
    }
  });
}
