from .commands import Command
from .idgenerator import IdGenerator
import random

from typing import Tuple, List, Dict, Any

class Ball:
    id: int
    type: int
    star: int
    position: Tuple[int, int]
    interval: int # 攻击间隔
    bulletSpeed: int # 子弹速度
    defaultDamage: int # 伤害
    def __init__(self, id: int, type: int, star: int, position: Tuple[int, int]):
        self.id = id
        self.type = type
        self.star = star
        self.position = position
        self.interval = -1
        self.bulletSpeed = -1
        self.defaultDamage = -1

    def set_ball_props(self, interval: int, bulletSpeed: int, defaultDamage: int):
        self.interval = interval
        self.bulletSpeed = bulletSpeed
        self.defaultDamage = defaultDamage

    def __str__(self) -> str:
        return '#{} star{} position{}'.format(self.id, self.star, self.position)
    
    # TODO: refactor
    def can_merge(from_ball: "Ball", to_ball: "Ball") -> bool:
        from_star = from_ball.star
        to_star = to_ball.star
        if from_star != to_star:
            return False
        from_type, to_type = from_ball.type, to_ball.type
        if from_type == 44: # 复制
            return True
        if from_type == 25: # 换位
            return from_star != 7 or to_type != 25
        if from_star == 7:
            return False
        if from_type == to_type:
            return True
        if from_type == 39: # 升星
            return True
        return False
    
    # TODO: BUG: 未完善
    # TODO: 繁衍
    def merge(from_ball: "Ball", to_ball: "Ball", generator: IdGenerator) -> List[
        Tuple[Command, Dict[str, Any]]
    ]:
        if not Ball.can_merge(from_ball, to_ball):
            return []
        # TODO: read config
        if from_ball.type == 39: # 升星
            return [
                (Command.CmdBallDestroy, {
                    'position': from_ball.position,
                }),
                (Command.CmdBallDestroy, {
                    'position': to_ball.position,
                }),
                (Command.CmdBallCreate, {
                    'id': generator.generate_id(),
                    'type': to_ball.type,
                    'star': from_ball.star + 1,
                    'position': to_ball.position,
                }),
            ]
        if from_ball.type != to_ball.type:
            if from_ball.type == 44: # 复制
                return [
                    (Command.CmdBallDestroy, {
                        'position': from_ball.position,
                    }),
                    (Command.CmdBallCreate, {
                        'id': generator.generate_id(),
                        'type': to_ball.type,
                        'star': from_ball.star,
                        'position': from_ball.position,
                    }),
                ]
            if from_ball.type == 25: # 换位
                return [
                    (Command.CmdBallSkill, {
                        'id': generator.generate_id(),
                        'type': to_ball.type,
                        'star': from_ball.star,
                        'position': from_ball.position,
                    }),
                ]
            return []
        return [
            (Command.CmdBallDestroy, {
                'position': from_ball.position,
            }),
            (Command.CmdBallDestroy, {
                'position': to_ball.position,
            }),
            (Command.CmdBallCreate, {
                'id': generator.generate_id(),
                'star': from_ball.star + 1,
                'position': to_ball.position,
            }),
        ]
