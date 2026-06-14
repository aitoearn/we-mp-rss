import { isDesktopApp } from '@/utils/auth'

export async function getDefaultExportDirectory(): Promise<string | null> {
  const dialogApi = window.electronAPI?.dialog
  if (!isDesktopApp() || !dialogApi) {
    return null
  }
  return dialogApi.getDefaultExportDir()
}

export async function pickExportDirectory(currentDir?: string): Promise<string | null> {
  const dialogApi = window.electronAPI?.dialog
  if (!isDesktopApp() || !dialogApi) {
    return null
  }
  const result = await dialogApi.selectExportDir(currentDir)
  if (result.canceled || !result.path) {
    return null
  }
  return result.path
}

export async function openExportDirectory(dirPath: string): Promise<boolean> {
  const dialogApi = window.electronAPI?.dialog
  if (!isDesktopApp() || !dialogApi) {
    return false
  }
  return dialogApi.openExportDir(dirPath)
}
