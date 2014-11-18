# -*- coding: utf-8 -*-

from tiles import *
import math

class RuleTemplate:

    def __init__(self, score, winPatternFunc):
        self.score = score
        self.winPatternFunc = winPatternFunc


    def __call__(self, d):
        return self.winPatternFunc(d)


def _PureDoubleChow(d):
    for i in range(len(d.sets)):
        for j in range(len(d.sets)):
            if i != j and \
               d.sets[i].type == TileSet.CHOW and \
               d.sets[j].type == TileSet.CHOW and \
               d.sets[i].index == d.sets[j].index:
                return True

    return False


def _MixedDoubleChow(d):
    for i in range(len(d.sets)):
        for j in range(len(d.sets)):
            if d.sets[i].type == TileSet.CHOW and \
               d.sets[j].type == TileSet.CHOW and \
               math.fabs(d.sets[i].index - d.sets[j].index) % 9 == 0 and \
               d.sets[i].index != d.sets[j].index:
                return True

    return False


def _ShortStraight(d):
    for i in range(len(d.sets)):
        for j in range(len(d.sets)):
            if d.sets[i].type == TileSet.CHOW and \
               d.sets[j].type == TileSet.CHOW and \
               math.fabs(d.sets[i].index - d.sets[j].index) == 3:
                return True

    return False


def _TwoTerminalChows(d):
    for i in range(len(d.sets)):
        for j in range(i + 1, len(d.sets)):
            if d.sets[i].type == TileSet.CHOW and \
               d.sets[j].type == TileSet.CHOW and \
               math.fabs(d.sets[i].index - d.sets[j].index) == 6 and \
               d.sets[i].index / 9 == d.sets[j].index / 9:
                return True

    return False


def _PungOfTerminalsOrHonors(d):
    for ts in d.sets:
        if (ts.type == TileSet.PUNG or ts.type == TileSet.KONG) and \
           ts.index in [str2Tile(s) for s in ['1s', '9s', '1m', '9m', '1p', '9p', 'E', 'S', 'W', 'N', 'P', 'F', 'C']]:
            return True

    return False


def _MeldedKong(d):
    for ts in d.sets:
        if ts.type == TileSet.KONG and ts.melded:
            return True

    return False


def _OneVoidedSuit(d):
    suitCount = [0, 0, 0]
    for ts in d.sets:
        if ts.index < 3 * 9:
            suitCount[ts.index / 9] = 1

    return sum(suitCount) == 2


def _NoHonorTiles(d):
    for ts in d.sets:
        if ts.index >= 3 * 9:
            return False

    return True


def _EdgeWait(d):
    pass 
    # TODO:  


PureDoubleChow = RuleTemplate(1, _PureDoubleChow) # 一般高
MixedDoubleChow = RuleTemplate(1, _MixedDoubleChow) # 喜相逢
ShortStraight = RuleTemplate(1, _ShortStraight) # 连六
TwoTerminalChows = RuleTemplate(1, _TwoTerminalChows) # 老少副
PungOfTerminalsOrHonors = RuleTemplate(1, _PungOfTerminalsOrHonors) # 幺九刻
MeldedKong = RuleTemplate(1, _MeldedKong) # 明杠
OneVoidedSuit = RuleTemplate(1, _OneVoidedSuit) # 缺一门
NoHonorTiles = RuleTemplate(1, _NoHonorTiles) # 无字
EdgeWait = RuleTemplate(1, _EdgeWait) # 边张

class Judger:

    def __init__(self):
        self.rules = [PureDoubleChow, 
                      MixedDoubleChow, 
                      ShortStraight, 
                      TwoTerminalChows,
                      PungOfTerminalsOrHonors,
                      MeldedKong]


    def judge(self, decompositions):
        maxScore = 0

        for d in decompositions:
            print 'Matching', d
            score = 0
            for r in self.rules:
                if r(d):
                    print r.winPatternFunc.__name__
                    score += r.score

            if score > maxScore:
                maxScore = score

        return maxScore