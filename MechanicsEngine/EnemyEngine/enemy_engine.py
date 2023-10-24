import pygame
import copy
import threading
import sys
import goomba
import koopa
sys.path.append("./GameObjects")

class EnemyEngine():

    def __init__(self):
        self.o_goomba = goomba.Goomba()
        self.o_koopa = koopa.Koopa()
        self.triggerStompAudio = False

    def main_loop(self, l_game_objects, o_player_engine, o_graphics_engine, objects):
        self.o_goomba.main_loop(l_game_objects,o_player_engine,o_graphics_engine,objects,self)
        self.o_koopa.main_loop(l_game_objects,o_player_engine,o_graphics_engine,objects,self)

    def track_scroll(self, l_game_objects, o_player_engine):
        for objects in l_game_objects:

            if o_player_engine.scroll_level and objects.subClass == 'enemy':

                objects.position[0] -= o_player_engine.x_displacement
