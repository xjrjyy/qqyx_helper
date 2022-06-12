from .command_base import CommandBase

from typing import Dict, Any

from ..ball import Ball
from .. import game as game_module

class CmdBallCreate(CommandBase):
    def excute(game: "game_module.Game", param: Dict[str, Any]):
        ''' 'id',
            'type'?,
            'star',
            'position',
        '''
        id = param['id']
        type = param['type'] if 'type' in param else game.get_random_ball_type()
        star = param['star']
        position = param['position']
        game.balls[position[0]][position[1]] = Ball(id, type, star, position)
