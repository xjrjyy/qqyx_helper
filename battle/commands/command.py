from enum import Enum

class Command(Enum):
    # Monster
    CmdMonsterCreate = "cmd_monster_create",
    CmdMonsterDestroy = "cmd_monster_destroy",
    # Ball
    CmdBallCreate = "cmd_ball_create",
    CmdBallDestroy = "cmd_ball_destroy",
    CmdBallUpdate = "cmd_ball_update",
    CmdBallSkill = "cmd_ball_skill",