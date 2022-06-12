from .command_base import CommandBase

from typing import Dict, Any

from ..ball import Ball
from .. import game as game_module

from loguru import logger

class CmdBallSkill(CommandBase):
    def excute(game: "game_module.Game", param: Dict[str, Any]):
        ''' 'id'
            'type'
            'skillType',
            'extraInfo'?,
        '''
        # TODO: 不完善
        id = param['id']
        type = param['type']
        if type == 25: # 换位
            '''
                {'target': 1}
            '''
            target_id = param['extraInfo']['target']
            from_ball = game.find_ball_by_id(id)
            to_ball = game.find_ball_by_id(target_id)
            assert(from_ball)
            assert(to_ball)
            game.swap_ball(from_ball.position, to_ball.position)
        else:
            logger.error(f'unknown param{param}')
