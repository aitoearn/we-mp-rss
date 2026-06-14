export {}

declare global {
  interface Window {
    electronAPI?: {
      platform: string
      versions: {
        node: string
        chrome: string
        electron: string
      }
      app: {
        relaunch: () => Promise<void>
        getPaths: () => Promise<{
          projectRoot: string
          userDataRoot: string
          backendPort: number
        }>
      }
      auth?: {
        isDesktop: true
        getState: () => Promise<{ token: string; expire?: number } | null>
        setState: (state: { token: string; expire?: number }) => Promise<boolean>
        clearState: () => Promise<boolean>
      }
      dialog?: {
        selectExportDir: (currentDir?: string) => Promise<{ canceled: boolean; path: string | null }>
        getDefaultExportDir: () => Promise<string>
        openExportDir: (dirPath: string) => Promise<boolean>
      }
    }
  }
}
