from .. import game as game_module

from typing import Dict, Any

class CommandBase:
    def excute(game: "game_module.Game", param: Dict[str, Any]):
        return NotImplemented
    