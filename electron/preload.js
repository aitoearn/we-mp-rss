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
  }
});
