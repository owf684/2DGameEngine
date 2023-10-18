import pygame
import copy
import threading
import sys
import Goomba
sys.path.append("./GameObjects")
import BlockObject

class _EnemyEngine():

    def __init__(self):
        self.Goomba = Goomba._Goomba()

        self.triggerStompAudio = False

    def main_loop(self, GameObjects, PlayerEngine, GraphicsEngine, objects):
        self.Goomba.main_loop(GameObjects,PlayerEngine,GraphicsEngine,objects,self)



    def track_scroll(self, GameObjects, PlayerEngine):
        for objects in GameObjects:

            if PlayerEngine.scroll_level and objects.subClass == 'enemy':

                objects.position[0] -= PlayerEngine.x_displacement
