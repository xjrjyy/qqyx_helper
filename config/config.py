import os
import time
from slpp import slpp
from typing import Dict

class LuaConfigReader:
    _filename: str
    _begin_str: str
    _config: Dict
    def __init__(self, filename: str, begin_str: str):
        self._filename = filename
        self._begin_str = begin_str
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
            data = data[data.find(begin_str) + len(begin_str):]
            data = data.replace('T(\'', '\'')
            data = data.replace('\')', '\'')
            self._config = slpp.decode(data)
    def get(self) -> Dict:
        return self._config

dragon_ball = LuaConfigReader('config/cfg_dragon_ball.lua', 'cfg_dragon_ball = ')

def get_ball_name_by_type(ball_type: int):
    return dragon_ball.get()[ball_type]['name']

PORT = 5147

LOG_DIR = os.path.join(os.getcwd(), f'log/{time.strftime("%Y-%m-%d")}.log')
LOG_FORMAT = '<level>{level: <8}</level>  <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>\n'

PROJECT_NAME = 'qqyx_helper'
VERSION = '0.1.0'
DEBUG = True