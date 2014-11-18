# -*- coding: utf-8 -*-

from mahjong import *
from tiles import *

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


game = Mahjong()
if DEBUG:
    game.actionListeners.append(logger)

game.run()