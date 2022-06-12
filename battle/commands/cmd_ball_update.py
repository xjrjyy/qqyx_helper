from .command_base import CommandBase

from typing import Dict, Any

from ..ball import Ball
from .. import game as game_module

class CmdBallUpdate(CommandBase):
    def excute(game: "game_module.Game", param: Dict[str, Any]):
        ''' 'id' or 'position',
        '''
        ball = None
        if 'position' in param:
            position = param['position']
            ball = game.balls[position[0]][position[1]]
        else:
            ball = game.find_ball_by_id(param['id'])
        if not ball: return
        if ball.star == 7: return
        game.balls[position[0]][position[1]].star += 1
