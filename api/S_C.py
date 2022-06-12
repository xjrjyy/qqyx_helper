from loguru import logger

from battle.battle import Battle

from . import current_battle

class S_C:
    def rpc_client_battle_info(
        self,
        serverInfo,
        selfIndex,
        playerInfoList,
        battleType,
        viewStatus
    ):
        '''
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
                ...
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
        '''
        # TODO: serverInfo
        logger.info(f'rpc_client_battle_info({serverInfo}, {selfIndex}, {playerInfoList}, {battleType}, {viewStatus})')
        current_battle.battle = Battle(selfIndex, playerInfoList, battleType, viewStatus)