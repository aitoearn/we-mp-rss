export interface StoredAuthState {
  token: string
  expire?: number
}

export const DESKTOP_DEFAULT_CREDENTIALS = {
  username: 'admin',
  password: 'admin@123'
} as const

export const getToken = (): string | null => {
  return localStorage.getItem('token')
}

export const isDesktopApp = (): boolean => {
  return Boolean(window.electronAPI?.auth?.isDesktop)
}

export async function initDesktopAuth(): Promise<void> {
  const authApi = window.electronAPI?.auth
  if (!authApi) {
    return
  }

  try {
    const state = await authApi.getState()
    if (!state?.token) {
      return
    }
    localStorage.setItem('token', state.token)
    if (state.expire) {
      localStorage.setItem('token_expire', String(state.expire))
    }
    const { verifyToken } = await import('@/api/auth')
    await verifyToken()
  } catch (error) {
    console.warn('桌面端登录状态无效，已清除:', error)
    await clearAuthToken()
  }
}

export async function saveAuthToken(token: string, expiresIn?: number): Promise<void> {
  localStorage.setItem('token', token)

  const expire = expiresIn ? Date.now() + expiresIn * 1000 : undefined
  if (expire) {
    localStorage.setItem('token_expire', String(expire))
  }

  const authApi = window.electronAPI?.auth
  if (!authApi) {
    return
  }

  await authApi.setState({ token, expire })
}

export async function clearAuthToken(): Promise<void> {
  localStorage.removeItem('token')
  localStorage.removeItem('token_expire')

  const authApi = window.electronAPI?.auth
  if (!authApi) {
    return
  }

  await authApi.clearState()
}
