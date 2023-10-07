import pygame
import copy
import threading
import sys
sys.path.append("./GameObjects")
import BlockObject

class _EnemyEngine():

    def __init__(self):
        self.enemy_index = 0
        self.goomba_troops = list()
        self.change_dir = False
        self.thread_started = False
        self.player_position = [0,0]
        self.player_direction = 1
    def main_loop(self, GameObjects, PlayerEngine, GraphicsEngine, objects):
        self.get_player_attr(objects)
        self.move_enemy(GameObjects, PlayerEngine, GraphicsEngine, objects)
        self.enemy_ai(GameObjects,PlayerEngine, GraphicsEngine, objects)

    def get_player_attr(self,objects):
        if objects.subClass == 'player':
            self.player_position = objects.position
            self.player_direction = objects.x_direction
    def move_enemy(self, GameObjects, PlayerEngine, GraphicsEngine, objects):

        if objects.subClass == 'enemy':

            if objects.isRendered:
                self.isHit(objects, GameObjects, GraphicsEngine)
                self.change_direction(objects)
                self.change_position(objects)

    def isHit(self, objects, GameObjects, GraphicsEngine):
        if objects.isHit:
            GameObjects.remove(objects)
            GraphicsEngine.render_buffer.remove(objects)

    def change_position(self, objects):
        objects.velocityX = 35

    def track_scroll(self, GameObjects, PlayerEngine):
        for objects in GameObjects:

            if PlayerEngine.scroll_level and objects.subClass == 'enemy':

                objects.position[0] -= PlayerEngine.x_displacement

    def change_direction(self, objects):
        if objects.collisionObject is not None:

            if objects.collisionObject.subClass != "player":

                if objects.collisionLeft:
                    objects.x_direction = 1
                if objects.collisionRight:
                    objects.x_direction = -1
            if isinstance(objects.collisionObject,BlockObject._BlockObject):
                if objects.collisionObject.changeHit:
                    objects.isHit = True
                    objects.collisionObject.changeHit = False
            

    def enemy_ai(self, GameObjects, PlayerEngine, GraphicsEngine, objects):
        inRangeX = 128
        inRangeY = 32
        x_distance = objects.position[0] - self.player_position[0]
        y_distance = objects.position[1] - self.player_position[1]
        if objects.subClass == 'enemy':
            if abs(x_distance) < inRangeX and abs(y_distance) <= inRangeY:
                if x_distance < 0:    
                    objects.x_direction = 1
                if x_distance > 0:
                    objects.x_direction = -1

