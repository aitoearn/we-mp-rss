const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  versions: {
    node: process.versions.node,
    chrome: process.versions.chrome,
    electron: process.versions.electron
  },
  platform: process.platform,
  app: {
    relaunch: () => ipcRenderer.invoke('app-relaunch'),
    getPaths: () => ipcRenderer.invoke('app-get-paths')
  },
  auth: {
    isDesktop: true,
    getState: () => ipcRenderer.invoke('auth-get-state'),
    setState: (state) => ipcRenderer.invoke('auth-set-state', state),
    clearState: () => ipcRenderer.invoke('auth-clear-state')
  },
  dialog: {
    selectExportDir: (currentDir) => ipcRenderer.invoke('dialog-select-export-dir', currentDir),
    getDefaultExportDir: () => ipcRenderer.invoke('export-get-default-dir'),
    openExportDir: (dirPath) => ipcRenderer.invoke('export-open-dir', dirPath)
  }
});
