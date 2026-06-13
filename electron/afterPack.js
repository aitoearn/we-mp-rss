/**
 * electron-builder afterPack hook
 * 设置后端可执行文件权限
 */

const fs = require('fs');
const path = require('path');

exports.default = async function afterPack(context) {
  const { appOutDir, electronPlatformName } = context;

  let resourcesPath;
  if (electronPlatformName === 'darwin') {
    const appName = context.packager.appInfo.productFilename;
    resourcesPath = path.join(appOutDir, `${appName}.app`, 'Contents', 'Resources');
  } else {
    resourcesPath = path.join(appOutDir, 'resources');
  }

  const backendExe = path.join(
    resourcesPath,
    'backend',
    'werss-gui',
    electronPlatformName === 'win32' ? 'werss-gui.exe' : 'werss-gui'
  );

  if (fs.existsSync(backendExe)) {
    fs.chmodSync(backendExe, 0o755);
    console.log('已设置后端可执行权限:', backendExe);
  } else {
    console.warn('未找到后端可执行文件:', backendExe);
  }
};
