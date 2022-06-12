import uvicorn
import asyncio
import json
from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse
import sys
import logging
from loguru import logger
import config
from extend import InterceptHandler, format_record

from api import current_battle

from api import api

def init_app():
    app = FastAPI(
        title=config.PROJECT_NAME,
        version=config.VERSION,
        debug=config.DEBUG,
    )
    logger.configure(
        handlers=[{'sink': sys.stdout, 'level': logging.INFO, 'format': format_record}]
    )
    # logging.getLogger().handlers = [InterceptHandler()]
    logger.add(config.LOG_DIR, encoding='utf-8', level=logging.DEBUG)
    logger.debug('日志系统已加载')
    # logging.getLogger('uvicorn.access').handlers = [InterceptHandler()]
    return app

app = init_app()

@app.post('/api.php')
async def helper_api(
    body: str=Body(..., example={
        'msg': '...',
    })
):
    data = json.loads(body)
    return await api.api(data['msg'])

def test_api(msg: str):
    loop = asyncio.get_event_loop()
    task = loop.create_task(api.api(msg))
    loop.run_until_complete(task)
    result = task.result()
    # loop.close()
    return result

def test():
    ball_info = {
        "star":7,
        "side":2,
        "pos":0,
        "extraInfo":[{"v":0,"k":"hitMonsterCnt"}]
    }
    api.s_c.rpc_client_battle_info(
        {
            'port': 27110,
            'domain': 'fightd6-dt.gzyueyou.cn',
            'roomId': 1044847330,
            'ip': 'fightd6-dt.gzyueyou.cn',
            'pwd': 125303,
            'ws': 'wss://fightd6-dt.gzyueyou.cn:9700/fight/27110'
        },
        2,
        [
            {
                'balls': [
                    {'dbType': 32, 'talentSkill': 0, 'lv': 8},
                    {'dbType': 35, 'talentSkill': 0, 'lv': 10},
                    {'dbType': 39, 'talentSkill': 0, 'lv': 11},
                    {'dbType': 40, 'talentSkill': 0, 'lv': 10},
                    {'dbType': 44, 'talentSkill': 0, 'lv': 8}
                ],
                'ballPatterns': [],
                'baseInfo': {
                    'legionId': '1267_1640227489_20000_8',
                    'grade': 16, 'name': '灵', 'legionIcon': '51',
                    'legionName': '水果篮', 'levelScore': 275,
                    'win': 69, 'lose': 68, 'historyLevelScore': 500,
                    'vserverId': 20000, 'uid': 37720952, 'normalScore': 10,
                    'kingMatchTimes': 1, 'maxHonor': 3999, 'sex': 0,
                    'activeTalentNum': 0, 'honor': 2708, 'icon': 50,
                    'achieveExp': 2940, 'kingMatchBestRank': 0, 'iconFrame': 7003, 
                    'kingsMarkCount': 0
                }, 
                'rewardBuffState': 0, 'monsterSkinId': 0, 'startAnimation': 0,
                'roleId': 0, 'skinId': 0, 'ballFrame': 5, 'ballLight': 0,
                'cfg': {'sp': 100, 'hp': 3, 'firstSp': 10}
            }, {
                'balls': [
                    {'dbType': 25, 'talentSkill': 0, 'lv': 20},
                    {'dbType': 44, 'talentSkill': 0, 'lv': 14},
                    {'dbType': 49, 'talentSkill': 38, 'lv': 14},
                    {'dbType': 28, 'talentSkill': 19, 'lv': 15},
                    {'dbType': 13, 'talentSkill': 0, 'lv': 20}
                ],
                'ballPatterns': [],
                'baseInfo': {
                    'legionId': '1255_1610525468_20532_297',
                    'grade': 25, 'name': '扯妹妹短裙', 'legionIcon': '37',
                    'legionName': '国威', 'levelScore': 1225,
                    'win': 4401, 'lose': 3750, 'historyLevelScore': 2075,
                    'vserverId': 20532, 'uid': 6292677, 'normalScore': 377,
                    'kingMatchTimes': 3, 'maxHonor': 20127, 'sex': 0,
                    'activeTalentNum': 1, 'honor': 3203, 'icon': 5009,
                    'achieveExp': 5220, 'kingMatchBestRank': 0, 'iconFrame': 1032,
                    'kingsMarkCount': 0
                },
                'rewardBuffState': 0, 'monsterSkinId': 0, 'startAnimation': 0,
                'roleId': 0, 'skinId': 20, 'ballFrame': 3, 'ballLight': 0,
                'cfg': {'sp': 100, 'hp': 3, 'firstSp': 10}
            }
        ],
        2, 
        0
    )
    api.bs_c.rpc_client_fight_ball_create(1, 49, ball_info, -1)
    ball_info["pos"] = 1
    api.bs_c.rpc_client_fight_ball_create(2, 25, ball_info, -1)
    api.bs_c.rpc_client_fight_ball_skill({"ballType":25,"extraInfo":[{"k":"target","v":1}],"side":2,"skillType":1,"ballId":2})
    print(current_battle.battle.games[2])

@app.get('/', response_class=PlainTextResponse)
async def show_board():
    result = ''
    for key, game in current_battle.battle.games.items():
        player_pos = '自己' if key == current_battle.battle.selfIndex else '对手'
        result += f'game({key} {player_pos}):\n'
        result += str(game)
    return result

if __name__ == '__main__':
    # test()
    # exit(0)
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=config.PORT,
        reload=True,
        access_log=True
    )