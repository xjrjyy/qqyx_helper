import time
from loguru import logger
import utils
from battle.commands import Command
from battle.ball import Ball
from . import current_battle

from typing import Dict, Tuple

class BS_C:
    _ball_props: Dict[int, Tuple[int, int, int]]
    def __init__(self):
        self._ball_props = {}
    def rpc_client_fight_ball_create(self, ballId: int, ballType: int, ballInfo, reason: int):
        logger.debug(f'rpc_client_fight_ball_create({ballId}, {ballType}, {ballInfo})')
        ballStar: int = ballInfo['star']
        ballSide: int = ballInfo['side']
        ballPos: int = ballInfo['pos']
        current_battle.battle.games[ballSide].run_command(Command.CmdBallCreate, {
            'id': ballId,
            'type': ballType,
            'star': ballStar,
            'position': (ballPos // 5, ballPos % 5),
        })
        if ballId in self._ball_props:
            game = current_battle.battle.games[ballSide]
            interval, bulletSpeed, defaultDamage = self._ball_props[ballId]
            del self._ball_props[ballId]
            ball = game.find_ball_by_id(ballId)
            ball.set_ball_props(interval, bulletSpeed, defaultDamage)

    def rpc_client_fight_ball_destroy(self, ballId: int):
        logger.debug(f'rpc_client_fight_ball_destroy({ballId})')
        game = current_battle.battle.find_game_by_ball_id(ballId)
        if not game: return
        ball = game.find_ball_by_id(ballId)
        ball = None

    def rpc_client_fight_ball_props(self, ballId: int, interval: int, bulletSpeed: int, defaultDamage: int):
        logger.debug(f'rpc_client_fight_ball_props({ballId}, {interval}, {bulletSpeed}, {defaultDamage})')
        game = current_battle.battle.find_game_by_ball_id(ballId)
        if not game:
            self._ball_props[ballId] = (interval, bulletSpeed, defaultDamage)
            return
        ball = game.find_ball_by_id(ballId)
        ball.set_ball_props(interval, bulletSpeed, defaultDamage)
    
    # TODO: 不完善
    def rpc_client_fight_ball_skill(self, skillInfo):
        logger.debug(f'rpc_client_fight_ball_skill({skillInfo})')
        # {"ballType":25,"extraInfo":[{"k":"target","v":2851}],"side":1,"skillType":1,"ballId":2361}
        ballSide: int = skillInfo['side']
        extraInfo = utils.kvlist2dict(skillInfo['extraInfo'])
        current_battle.battle.games[ballSide].run_command(Command.CmdBallSkill, {
            'id': skillInfo['ballId'],
            'type': skillInfo['ballType'],
            'skillType': skillInfo['skillType'],
            'extraInfo': extraInfo,
        })
    
    def rpc_client_fight_monster_create(self, monsterId: int, monsterType, monsterBaseInfo):
        pass
        # TODO: 
    
    def rpc_client_fight_emoji(self, side: int, emojiId: int):
        if emojiId == 1:
            with open(f'zdata/{time.strftime("%Y-%m-%d_%H-%M-%S")}.txt', 'w', encoding='utf-8') as f:
                for key, game in current_battle.battle.games.items():
                    f.write(f'game({key}):\n')
                    f.write(str(game))
    
    def rpc_client_fight_ball_attack(self, ballId: int, attackInfo):
        # logger.info(f'rpc_client_fight_ball_attack({ballId}, {attackInfo})')
        # TODO: 不完善
        pass
    
    def rpc_client_tell_me(self, color, str_: str):
        del color
        logger.info(f'[提示信息]: {str_}')

    def rpc_client_fight_frame_begin(self, frame: int, gameTime: int):
        pass

    def rpc_client_fight_frame_end(self):
        pass
