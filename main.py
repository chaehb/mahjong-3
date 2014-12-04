# -*- coding: utf-8 -*-

from mahjong import *
from tiles import *
from rules import *

DEBUG = True

def logger(action):
    if action['from']:
        print action['from'],

    print action['name'],

    if action['to']:
        print action['to'],

    if action['tile'] != None:
        action['tile'] = tile2Str(action['tile'])
        print action['tile'],

    if action['from']:
        print '=>', action['from'].tiles,

    print 


# game = Mahjong()
# if DEBUG:
#     game.actionListeners.append(logger)

# game.run()

ts = Tiles()

import random

for i in range(14):
    ts[random.randint(0, 33)] += 1

# ts.add('1s')
# ts.add('2s')
# ts.add('3s')
# ts.add('4s')
# ts.add('6s')
# ts.add('7s')
# ts.add('7s')
# ts.add('8s')
# ts.add('8s')

# ts.add('N')
# ts.add('N')
# ts.add('N')
# ts.add('E')
# ts.add('E')

print ts

for t in ts.decompose():
    print t

# for i in range(34):
#     if ts[i] > 0:
#         ts[i] -= 1
#         for j in range(34):
#             if i != j:
#                 ts[j] += 1

#                 print 'replace', i, 'with', j

#                 for t in ts.decompose():
#                     print t

# j = Judger()
# game = Mahjong()
# game.newAction(name = 'Draw', tile = 0)

# print 'Judging:', ts
# score, wps = j.judge(ts.decompose(True), game)
# print 'Score:', score
# for wp in wps:
#     print wp
