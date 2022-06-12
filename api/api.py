from loguru import logger
import re
import json

from typing import Optional, List

from .C_S import C_S
from .S_C import S_C
from .C_BS import C_BS
from .BS_C import BS_C

c_s = C_S()
s_c = S_C()
c_bs = C_BS()
bs_c = BS_C()

def before_handle_msg(msg: str) -> Optional[str]:
    msg = msg.replace('\'', '"')
    shield_str_ist = [
        '\\|@\\|[\\-]?\d+$',
        'LUA ERROR',
        'stack traceback:',
        'rpc_parse error',
        'pool size is',
        'Cannot read property',
        'prepare rpc_server_heartbeat_pto',
        '该商品列表在表中是属于id',
    ]
    if re.match('|'.join(shield_str_ist), msg): return None
    return msg

def is_exclude(msg_list: List[str]):
    exclude_list = [
        "^load csb:", # 资源加载不打印
        "^cur pop layer num", # 视图数
    ]
    msg_item = msg_list[0]
    for re_str in exclude_list:
        if re.match(re_str, msg_item): return True
    return False

async def handle_msg(msg: str) -> Optional[str]:
    eval_code: Optional[str] = None
    msg_list = msg.split('|@|')
    log_str = ''
    if msg_list:
        if re.match('^\[\w+\]:$', msg_list[0]):
            if msg_list[0] == '[QTZ_DEBUG]:':
                log_str = '[调试] '
            elif msg_list[0] == '[QTZ_INFO]:':
                log_str = '[信息] '
            elif msg_list[0] == '[QTZ_ERROR]:':
                log_str = '[错误] '
            else:
                log_str = msg_list[0]
            msg_list = msg_list[1:]
            if msg_list:
                if is_exclude(msg_list): return ''
                eval_code = await acquire_eval(msg_list)
    if eval_code is None:
        log_str += json.dumps(msg_list)
        logger.info(log_str)
    return eval_code

async def run_command(handle, cmd: str, write_log: bool) -> str:
    function_name = cmd[:cmd.find('(')]
    if not hasattr(handle, function_name):
        if write_log:
            logger.debug(f'handle hasn\'t attr {cmd}')
        return ''
    return eval('handle.' + cmd)

async def acquire_eval(msg_list: List[str]) -> str:
    if not msg_list: return ''
    eval_code = ''
    msg = msg_list[0]
    handles = {
        '[C->S] ': c_s,
        '[S->C] ': s_c,
        '[C->BS] ': c_bs,
        '[BS->C] ': bs_c,
    }
    for key, handle in handles.items():
        if msg.startswith(key):
            raw_msg = msg[len(key):]
            # TODO: 
            eval_code = await run_command(handle, raw_msg, False) # key == '[BS->C] '
    if eval_code is None: eval_code = ''
    return eval_code

async def api(msg: str):
    msg = before_handle_msg(msg)
    if not msg: return
    eval_code = await handle_msg(msg)
    if not eval_code: eval_code = ''
    result = {
        'code': 0,
        'msg': '请求成功',
        'data' : {
            'eval': eval_code,
            'debug': True,
            'ip': '127.0.0.1',
        }
    }
    return result