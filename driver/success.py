from sqlalchemy.util import b

from .token import set_token
from core.print import print_warning,print_success
from core.redis_client import redis_client
import json
#判断是否是有效登录 

# 初始化全局变量（作为Redis不可用时的回退）
WX_LOGIN_ED = False
WX_LOGIN_INFO = None

import threading

# 初始化线程锁
login_lock = threading.Lock()

# Redis key 常量
REDIS_KEY_STATUS = "werss:login:status"

def setStatus(status:bool):
    """设置登录状态，优先存储到Redis，失败则使用全局变量"""
    global WX_LOGIN_ED
    # 尝试存储到Redis
    if redis_client.is_connected:
        try:
            redis_client._client.set(REDIS_KEY_STATUS, "1" if status else "0")
        except Exception:
            pass
    # 同时更新全局变量作为回退
    with login_lock:
        WX_LOGIN_ED = status

def _is_token_expired(expiry: dict) -> bool:
    """判断微信 token 是否已过期（优先使用 expiry_timestamp）"""
    import time
    if not expiry:
        return False
    expiry_timestamp = expiry.get('expiry_timestamp')
    if expiry_timestamp:
        return expiry_timestamp <= time.time()
    remaining = expiry.get('remaining_seconds')
    if remaining is not None:
        return remaining <= 0
    return False

def getStatus():
    """获取登录状态：基于持久化 token 校验是否有效（服务重启后亦可恢复）"""
    token_data = getLoginInfo()
    if not token_data or not token_data.get('token'):
        setStatus(False)
        return False

    expiry = token_data.get('expiry')
    if expiry and _is_token_expired(expiry):
        print_warning("Token已过期，需要重新登录")
        setStatus(False)
        return False

    setStatus(True)
    return True

def sync_login_status():
    """服务启动时从持久化 token 同步微信登录状态"""
    if getStatus():
        print_success("微信授权状态有效，已恢复登录状态")
    else:
        print_warning("微信未授权或授权已过期，需扫码重新授权")
def getLoginInfo():
    from driver.token import _get_token_data
    return _get_token_data()

def Success_Msg(data:dict,ext_data:dict={}):
    from jobs.notice import sys_notice
    from core.config import cfg
    text="# 授权成功\n"
    text+=f"- 服务名：{cfg.get('server.name','')}\n"
    text+=f"- 名称：{ext_data['wx_app_name']}\n"
    text+=f"- Token: {data['token']}\n"
    text+=f"- 有效时间: {data['expiry']['expiry_time']}\n"
    
    sys_notice(text, str(cfg.get("server.code_title","WeRss授权完成")))
def Success(data:dict,ext_data:dict={}):
    if data != None:
            # print("\n登录结果:")
            if ext_data is not {}:
                print_success(f"名称：{ext_data['wx_app_name']}")
            if data['expiry'] !=None:
                Success_Msg(data,ext_data)
                print_success(f"有效时间: {data['expiry']['expiry_time']} (剩余秒数: {data['expiry']['remaining_seconds']}) Token: {data['token']}")
                set_token(data,ext_data)
                setStatus(True)
            else:
                print_warning("登录失败，请检查上述错误信息")
                setStatus(False)

    else:
            print("\n登录失败，请检查上述错误信息")
            setStatus(False)

def CanGetToken():
    """检查是否可以获取Token，包括检查登录状态和token过期时间"""
    if not getStatus():
        print_warning("当前未登录或Token已过期，请先扫码登录")
        return False
    return True
