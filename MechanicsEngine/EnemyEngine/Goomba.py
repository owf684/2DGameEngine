import pygame
import copy
import threading
import sys
sys.path.append("./GameObjects")
import BlockObject

class _Goomba():

    def __init__(self):
        self.player_position = [0,0]
        self.player_direction = 1

    def main_loop(self, GameObjects, PlayerEngine, GraphicsEngine, objects,EnemyEngine):
        self.get_player_attr(objects)

        if not objects.timer_started:

            self.move_enemy(GameObjects, PlayerEngine, GraphicsEngine, objects, EnemyEngine)
            self.enemy_ai(GameObjects, PlayerEngine, GraphicsEngine, objects)
        
        self.isHit(objects, GameObjects, GraphicsEngine,EnemyEngine)
    
    def get_player_attr(self,objects):
        if objects.subClass == 'player':
            self.player_position = objects.position
            self.player_direction = objects.x_direction
    def move_enemy(self, GameObjects, PlayerEngine, GraphicsEngine, objects,EnemyEngine):

        if objects.subClass == 'enemy':

            if objects.isRendered:
                self.isHit(objects, GameObjects, GraphicsEngine,EnemyEngine)
                self.change_direction(objects)
                self.change_position(objects)

    def isHit(self, objects, GameObjects, GraphicsEngine,EnemyEngine):
        if objects.destroy and objects.subClass == 'enemy':
            objects.destroy = False
            GameObjects.remove(objects)
            GraphicsEngine.render_buffer.remove(objects)

    def change_position(self, objects):
        objects.velocityX = 35


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
                    objects.fromUnder = True
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

