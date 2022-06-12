from .commands import Command
from .idgenerator import IdGenerator
from .ball import Ball
from .game import Game

from typing import Dict, Optional, List, Any

class Battle:
    games: Dict[int, Game]
    selfIndex: int

    def __init__(
        self,
        selfIndex: int,
        playerInfoList: List[Dict[str, Any]],
        battleType: int,
        viewStatus: int
    ):
        '''viewStatus 0普通战斗，1好友观战，2大神观战，3其他观战
        '''
        self.games = {}
        self.selfIndex = selfIndex
        for i in range(0, len(playerInfoList)):
            self.games[i + 1] = Game(IdGenerator())
            playerInfo = playerInfoList[i]
            self.games[i + 1].deck = playerInfo['balls']

    def find_game_by_ball_id(self, ball_id: int) -> Optional[Game]:
        for _, game in self.games.items():
            if game.find_ball_by_id(ball_id):
                return game
        return None
