# # -*- coding: utf-8 -*-

from tiles import *
import itertools
import math

class Pattern:

    def __init__(self, rule, tilesets):
        self.rule = rule
        self.tilesets = tilesets

    def __str__(self):
        return str(self.rule) + ' : ' + str(self.tilesets)

    def __repr__(self):
        return self.__str__()


class Rule:

    def __init__(self, func):
        self.func = func
        self.name = ''
        self.score = 0

    def __call__(self, tilesets, game):
        return self.func(tilesets, game)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __and__(self, b):
        return Rule(lambda t, g: self.func(t, g) and b.func(t, g))

    def __or__(self, b):
        return Rule(lambda t, g: self.func(t, g) or b.func(t, g))

    def __invert__(self):
        return Rule(lambda t, g: not self.func(t, g))


# Basic Atom Rules
def _sameTile(t, g):
    index = t[0].index
    for i in range(1, len(t)):
        if t[i].index != index:
            return False

    return True


def _sameIndex(tilesets, game):
    index = tilesets[0].index % 9
    for ts in tilesets:
        if ts.index > 3 * 9 or ts.index % 9 != index:
            return False

    return True


def _sameSuit(t, g):
    suit = t[0].index / 9
    for ts in t:
        if ts.index > 3 * 9 or ts.index / 9 != suit:
            return False

    return True


def _allChow(t, g):
    for ts in t:
        if ts.type != TileSet.CHOW:
            return False

    return True


def _allPung(t, g):
    for ts in t:
        if ts.type != TileSet.PUNG and ts.type != TileSet.KONG:
            return False

    return True


def _allKong(t, g):
    for ts in t:
        if ts.type != TileSet.KONG:
            return False

    return True


def _allConcealed(t, g):
    for ts in t:
        if ts.melded:
            return False

    return True


def _allTerminal(t, g):
    for ts in t:
        if ts.type == TileSet.CHOW:
            if ts.index % 9 != 0 or ts.index % 9 != 7:
                return True
        else:
            if ts.index not in [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33]:
                return False

    return True


def _allHonor(t, g):
    for ts in t:
        if ts.type != TileSet.CHOW:
            if ts.index not in [27, 28, 29, 30, 31, 32, 33]:
                return False

    return True


def _hasSuit(count):
    def __hasSuit(t, g):
        s = [0,0,0]
        for ts in t:
            if ts.index < 3 * 9:
                s[ts.index / 9] = 1
        return sum(s) == count

    return __hasSuit

SAME_TILE = Rule(_sameTile)
SAME_INDEX_IN_SUIT = Rule(_sameIndex)
SAME_SUIT = Rule(_sameSuit)
ALL_CHOW = Rule(_allChow)
ALL_TERMINAL = Rule(_allTerminal)
ALL_PUNG = Rule(_allPung)
ALL_KONG = Rule(_allKong)
ALL_CONCEALED = Rule(_allConcealed)
ALL_MELDED = ~ALL_CONCEALED
ALL_HONOR = Rule(_allHonor)

'''
Rule List
'''

# Win Rules
PureDoubleChow = ALL_CHOW & SAME_TILE
PureDoubleChow.name = 'Pure Double Chow' # 一般高
PureDoubleChow.score = 1

MixedDoubleChow = ALL_CHOW & SAME_INDEX_IN_SUIT & ~SAME_TILE
MixedDoubleChow.name = 'Mixed Double Chow' # 喜相逢
MixedDoubleChow.score = 1

ShortStraight = ALL_CHOW & SAME_SUIT & Rule(lambda t, g: math.fabs(t[0].index - t[1].index) == 3)
ShortStraight.name = 'Short Straight' # 连六
ShortStraight.score = 1

TwoTerminalChows = ALL_CHOW & SAME_SUIT & Rule(lambda t, g: math.fabs(t[0].index - t[1].index) == 6)
TwoTerminalChows.name = 'Two Terminal Chows' # 老少副
TwoTerminalChows.score = 1

PungOfTerminalsOrHonors = ALL_PUNG & ALL_TERMINAL
PungOfTerminalsOrHonors.name = 'Pung of Terminals or Honors' # 幺九刻
PungOfTerminalsOrHonors.score = 1

MeldedKong = ALL_KONG & ALL_MELDED
MeldedKong.name = 'Melded Kong' # 明杠
MeldedKong.score = 1

OneVoidedSuit = Rule(_hasSuit(2))
OneVoidedSuit.name = 'One Voided Suit' # 缺一门
OneVoidedSuit.score = 1

NoHonorTiles = ~ALL_HONOR
NoHonorTiles.name = 'No Honor Tiles' # 无字
NoHonorTiles.score = 1
'''
Rule List Ends
'''


class Judger:

    def __init__(self):
        self.rules = [
            None, 
            # 1 tileset rules
            [MeldedKong], 
            # 2 tileset rules
            [PureDoubleChow, MixedDoubleChow, ShortStraight, TwoTerminalChows], 
            # 3 tileset rules
            [], 
            # 4 tileset rules
            [],
            # all tileset rules
            [OneVoidedSuit, NoHonorTiles]
        ]

        self.specialRules = []


    def judge(self, decompositions, game):
        maxScore = 0
        winPatterns = []

        for d in decompositions:
            patterns = []
            for i in [4,3,2,1]:
                patterns += self.judgeSubset(self.rules[i], self.select(d, i), game)

            patterns += self.judgeSubset(self.rules[5], [d.sets], game)

            score = sum([p.rule.score for p in patterns])

            if score > maxScore:
                maxScore = score
                winPatterns = patterns

        return maxScore, winPatterns


    def judgeSubset(self, rules, subsetList, game):
        patterns = []

        for subset in subsetList:
            for r in rules:
                if r(subset, game) and not self.duplicate(subset, r, patterns):
                    patterns.append(Pattern(r, subset))

        return patterns


    def select(self, decomposition, count):
        sets = [ts for ts in decomposition.sets if ts.type != TileSet.PAIR]
        return itertools.combinations(sets, count)


    def duplicate(self, subset, rule, patterns):
        for p in patterns:
            if p.rule is rule:
                for ts in subset:
                    if ts in p.tilesets:
                        return True

        return False













