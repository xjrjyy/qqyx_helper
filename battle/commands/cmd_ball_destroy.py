from .command_base import CommandBase

from typing import Dict, Any

from ..ball import Ball
from .. import game as game_module

class CmdBallDestroy(CommandBase):
    def excute(game: "game_module.Game", param: Dict[str, Any]):
        ''' 'id' or 'position',
        '''
        position = None
        if 'position' in param:
            position = param['position']
        else:
            ball = game.find_ball_by_id(param['id'])
            assert(ball)
            position = ball.position
        game.balls[position[0]][position[1]] = None
