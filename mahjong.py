# -*- coding: utf-8 -*-

from tiles import *
from ai import *
from players import *
from rules import *

class Mahjong:

    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    ACTIONS = ['Start', 'Draw End', 'Win', 'Chow', 'Pung', 'Big Melded Kong', 'Small Melded Kong', 'Concealed Kong', \
               'Draw', 'Discard', 'Replace']

    def __init__(self, aiClass = [DummyAI, DummyAI, DummyAI, DummyAI], judger = Judger()):
        self.players = [Player(AI()) for AI in aiClass]
        for i in range(4):
            self.players[i].ai.game = self
            self.players[i].seatWind = i

        self.prevalentWind = Mahjong.EAST
        self.currentPlayerIndex = 0

        self.tilePool = []
        self.discardPool = []

        # action is one dict like this: {'name' : 'xxx', 'from' : p1, 'to' : p2, 'tile' : 1}
        self.actions = []
        self.judger = judger
        self.actionListeners = []


    def run(self):
        '''
        Run will start one match. There will be 16 games in one match(全庄).
        After Each 4 game, the prevalent wind will be changed:
            1 - 4: EAST
            5 - 8: SOUTH
            9 -12: WEST
            13-16: NORTH

        East Player(庄家) will be then random chosen. He will be the first one
        to discard tile in one game. After one game finished, the player at right(下家)
        of East Player will be the next East Player.
        The east wind of each player will be (from left to right): E, S, W, N

        In One Game:
            1. Generate tiles and shuffle them.
            2. Random Select one player to be East player.
            3. Loop normal turn util one can win or no more tile.
        '''
        self.runGame()


    def runGame(self):
        '''
        One game in match
        '''
        self.tilePool = Tiles.generateShuffledTilePool()
        self.newAction('Start')
        # each player draws 13 tiles
        for i in range(len(self.players)): 
            for j in range(13):
                self.sendTileTo(self.popOneTile(), self.players[i])

        # east player get 14th tile
        self.sendTileTo(self.popOneTile(), self.curPlayer())

        while not self.canFinish(self.curPlayer()):
            if self.singleTurnInGame():
                return


    def singleTurnInGame(self):
        '''
        Single turn in one game. Return true means this game is finished.
        '''
        # check concealed kong
        if self.canConcealedKong(self.curPlayer()) and self.curPlayer().concealedKong():
            self.curPlayer().draw(self.popLastOneTile())
            if self.canFinish(self.curPlayer()):
                return True

        # check small melded kong
        if self.canSmallMeldedKong(self.curPlayer()) and self.curPlayer().smallMeldedKong():
            self.curPlayer().draw(self.popLastOneTile())
            if self.canFinish(self.curPlayer()):
                return True

        tile = self.curPlayer().discard()
        self.newAction('Discard', self.curPlayer(), tile = tile)

        # check melded kong
        for i, p in enumerate(self.players):
            if i != self.currentPlayerIndex:
                if self.canBigMeldedKong(p, tile) and p.bigMeldedKong(tile):
                    p.draw(self.popLastOneTile())
                    if self.canFinish(p):
                        return True
                    else:
                        self.changePlayer(i)
                        return False

        # check pung
        for i, p in enumerate(self.players):
            if i != self.currentPlayerIndex:
                if self.canPung(p, tile) and p.pung(tile):
                    if self.canFinish(p):
                        return True
                    else:
                        self.changePlayer(i)
                        return False

        # check chow
        nextIndex = (self.currentPlayerIndex + 1) % len(self.players)
        nextPlayer = self.players[nextIndex]
        if self.canPung(nextPlayer, tile) and nextPlayer.pung(tile):
            if self.canFinish(nextPlayer):
                return True
            else:
                self.changePlayer(nextIndex)
                return False


        self.discardPool.append(tile)
        self.changePlayer(nextIndex)
        self.sendTileTo(self.popOneTile(), self.curPlayer())

        return False


    def curPlayer(self):
        '''
        Get current player
        '''
        return self.players[self.currentPlayerIndex]


    def canConcealedKong(self, player):
        '''
        Check if this player can conceal kong (暗杠)
        '''
        for i in range(Tiles.NUM):
            if player.tiles[i] == 4:
                return True

        return False


    def canBigMeldedKong(self, player, tile):
        '''
        Check if this player can big meld kong (大明杠)
        '''
        return player.tiles[tile] == 3


    def canSmallMeldedKong(self, player):
        '''
        Check if this player can small meld kong (小明杠)
        '''
        for ts in player.meldedTileSets:
            if ts.type == TileSet.PUNG and player.tiles[ts.index] == 1:
                return True

        return False


    def canPung(self, player, tile):
        '''
        Check if this player can pung (碰)
        '''
        return player.tiles[tile] == 2


    def canChow(self, player, tile):
        '''
        Check if this player can chow (吃)
        '''
        if tile >= 3 * 9:
            return False

        index = tile % 9
        if player.tiles[tile + 1] > 0 and player.tiles[tile + 2] > 0 and index < 7:
            return True
        if player.tiles[tile - 1] > 0 and player.tiles[tile + 1] > 0 and index < 8 and index > 0:
            return True
        if player.tiles[tile - 2] > 0 and player.tiles[tile - 1] > 0 and index > 1:
            return True

        return False


    def changePlayer(self, playerIndex):
        self.currentPlayerIndex = playerIndex


    def popOneTile(self):
        '''
        Get and remove one tile from tile pool
        '''
        return self.tilePool.pop(0)


    def popLastOneTile(self):
        '''
        Get and remove last one tile from tile pool
        '''
        return self.tilePool.pop()


    def canFinish(self, player):
        '''
        Check if the tiles of this player can match win pattern
        '''
        finish, fans = self.judger.judge(player, self)

        if finish:
            self.newAction('Win', player)
        elif len(self.tilePool) == 0:
            self.newAction('Draw End')

        return finish


    def sendTileTo(self, tile, player):
        player.draw(tile)
        self.newAction('Draw', fromPlayer = player, tile = tile)


    def newAction(self, name, fromPlayer = None, toPlayer = None, tile = None):
        action = {
            'name' : name,
            'from' : fromPlayer,
            'to'   : toPlayer,
            'tile' : tile
        }

        self.actions.append(action)
        for listener in self.actionListeners:
            listener(action)