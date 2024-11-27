import numpy
import pygame
import asyncio
import json
from global_items import glbls
import sys

if len(sys.argv) > 1:
    glbls['Full Screen'] = (sys.argv[1] == 'full')
    if len(sys.argv) > 2:
        glbls["start_level"] = int(sys.argv[2])


from gameplay import GamePlay
from scorescreen import ScoreScreen
from introscreen import IntroScreen
from game import Game
from level_objects import init_coords


pygame.init()
if glbls['Full Screen']:
    window = pygame.display.set_mode((glbls['WIDTH'], glbls['HEIGHT']),flags=pygame.FULLSCREEN | pygame.SCALED)
else:
    window = pygame.display.set_mode((glbls['WIDTH'], glbls['HEIGHT']))
init_coords(glbls)
pygame.display.set_caption("Dave's Delivery Disaster 64x64")
glbls['window'] = window

glbls['s_delivered'] = pygame.mixer.Sound("audio/delivered.ogg")
glbls['s_delivered'].set_volume(0.5)
glbls['s_gotzero'] = pygame.mixer.Sound("audio/got_zero.ogg")
glbls['s_gotzero'].set_volume(0.8)
glbls['s_explosion'] = pygame.mixer.Sound("audio/explosion.ogg")
glbls['s_explosion'].set_volume(0.5)

glbls['g_check'] = pygame.image.load('graphics/check.png').convert_alpha()
glbls['g_x'] = pygame.image.load('graphics/x.png').convert_alpha()


glbls['icount_good'] = 3
glbls['i_good_1'] = pygame.mixer.Sound("audio/I_thatwilldo.ogg")
glbls['i_good_2'] = pygame.mixer.Sound("audio/I_unbelievable.ogg")
glbls['i_good_3'] = pygame.mixer.Sound("audio/I_wow.ogg")
glbls['icount_med'] = 2
glbls['i_med_1'] = pygame.mixer.Sound("audio/I_iveseenbetter.ogg")
glbls['i_med_2'] = pygame.mixer.Sound("audio/I_thatsembarrassing.ogg")
glbls['icount_bad'] = 5
glbls['i_bad_1'] = pygame.mixer.Sound("audio/I_areyousure.ogg")
glbls['i_bad_2'] = pygame.mixer.Sound("audio/I_howmanytries.ogg")
glbls['i_bad_3'] = pygame.mixer.Sound("audio/I_isthathebest.ogg")
glbls['i_bad_4'] = pygame.mixer.Sound("audio/I_kiddingme.ogg")
glbls['i_bad_5'] = pygame.mixer.Sound("audio/I_pathetic.ogg")

glbls['STATES'] = {
    "IntroScreen": IntroScreen(glbls),
    "GamePlay": GamePlay(glbls),
    "ScoreScreen": ScoreScreen(glbls)
}

game = Game(window, glbls, glbls['start_state'])
asyncio.run(game.run())
