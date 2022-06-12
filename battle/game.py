from loguru import logger

from .commands.command import Command
from .commands.cmd_ball_create import CmdBallCreate
from .commands.cmd_ball_destroy import CmdBallDestroy
from .commands.cmd_ball_update import CmdBallUpdate
from .commands.cmd_ball_skill import CmdBallSkill

from .idgenerator import IdGenerator
from .ball import Ball
import config
import random
from typing import List, Dict, Any, Tuple, Optional

class Game:
    balls: List[List[Ball]]
    '''{'dbType': 49, 'talentSkill': 38, 'lv': 14}'''
    deck: List[Dict[str, int]]
    _id_generator: IdGenerator
    def __init__(self, id_generator: IdGenerator):
        self.balls = []
        self.deck = [] # set deck
        self._id_generator = id_generator
        for i in range(0, 3):
            self.balls.append([]);
            for j in range(0, 5):
                # ball = Ball(DECK[(i * 5 + j) % 5], (i * 5 + j) % 7 + 1, (i, j))
                ball = None
                self.balls[i].append(ball)
    
    def __str__(self):
        result = ''
        for ball_info in self.deck:
            title = ''
            if ball_info['talentSkill'] != 0:
                title += '天赋技能'
            result += f'{config.get_ball_name_by_type(ball_info["dbType"])}({title}): '
            result += f'lv.{ball_info["lv"]} '
        result += '\n'
        for i in range(0, 3):
            for j in range(0, 5):
                ball = self.balls[i][j]
                if not ball: continue
                result += str(ball)
                result += f' {config.get_ball_name_by_type(ball.type)}'
                result += f' interval: {ball.interval}'
                result += f' bulletSpeed: {ball.bulletSpeed}'
                result += f' defaultDamage: {ball.defaultDamage}'
                result += '\n'
        return result

    def get_random_ball_type(self):
        assert(self.deck)
        return self.deck[random.randrange(0, len(self.deck))]['dbType']
    
    def swap_ball(self, pos1: Tuple[int, int], pos2: Tuple[int, int]):
        self.balls[pos1[0]][pos1[1]], self.balls[pos2[0]][pos2[1]] = \
            self.balls[pos2[0]][pos2[1]], self.balls[pos1[0]][pos1[1]]
        if self.balls[pos1[0]][pos1[1]]:
            self.balls[pos1[0]][pos1[1]].position = pos1
        if self.balls[pos2[0]][pos2[1]]:
            self.balls[pos2[0]][pos2[1]].position = pos2

    def run_command(self, command: Command, command_args: Dict[str, Any]):
        '''path: battle/battle.lua onBallSkill
        '''
        # TODO: assert
        if command is Command.CmdBallCreate:
            CmdBallCreate.excute(self, command_args)
        elif command is Command.CmdBallDestroy:
            CmdBallDestroy.excute(self, command_args)
        elif command is Command.CmdBallUpdate:
            CmdBallUpdate.excute(self, command_args)
        elif command is Command.CmdBallSkill:
            CmdBallSkill.excute(self, command_args)
        else:
            logger.error(f'unknown command: {command}')
        
    def get_ball_count(self):
        count = 0
        for i in range(0, 3):
            for j in range(0, 5):
                if self.balls[i][j]:
                    count += 1
        return count

    def buy_ball(self) -> Optional[Tuple[int, int]]:
        if self.get_ball_count() == 15: return None
        free_position: List[Tuple[int, int]] = []
        for i in range(0, 3):
            for j in range(0, 5):
                if not self.balls[i][j]:
                    free_position.append((i, j))
        position = free_position[random.randrange(0, len(free_position))]
        new_ball_type = self.get_random_ball_type()
        self.run_command(Command.CmdBallCreate, {
            'id': self._id_generator.generate_id(),
            'type': new_ball_type,
            'star': 1,
            'position': position,
        })
        return position

    def update_ball(self) -> Optional[Tuple[int, int]]:
        if self.get_ball_count() == 0: return None
        free_position: List[Tuple[int, int]] = []
        for i in range(0, 3):
            for j in range(0, 5):
                if self.balls[i][j]:
                    free_position.append((i, j))
        position = free_position[random.randrange(0, len(free_position))]
        self.run_command(Command.CmdBallUpdate, {
            'position': position,
        })
        return position

    def merge_ball(self, from_ball: Ball, to_ball: Ball):
        commands = Ball.merge(from_ball, to_ball)
        for command in commands:
            self.run_command(command[0], command[1])
    
    def find_ball_by_id(self, ball_id: int) -> Optional[Ball]:
        for i in range(0, 3):
            for j in range(0, 5):
                ball = self.balls[i][j]
                if ball and ball.id == ball_id:
                    return ball
        return None
