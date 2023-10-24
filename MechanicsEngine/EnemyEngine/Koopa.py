import pygame
import copy
import threading
import sys
sys.path.append("./GameObjects")
import block_object

class Koopa():

    def __init__(self):
        self.player_position = [0,0]
        self.player_direction = 1

    def main_loop(self, l_game_objects, o_player_engine, o_graphics_engine, objects,o_enemy_engine):
        self.get_player_attr(objects)

        if objects.subClass == 'enemy' and (not objects.timer_started or objects.hit_state == 2)and 'Koopa' in objects.imagePath:

            self.move_enemy(l_game_objects, o_player_engine, o_graphics_engine, objects, o_enemy_engine)
            self.enemy_ai(l_game_objects, o_player_engine, o_graphics_engine, objects)
        if objects.subClass == 'enemy' and 'Koopa' in objects.imagePath:
            print ("objects.hit_state", objects.hit_state)
            self.isHit(objects, l_game_objects, o_graphics_engine,o_enemy_engine)
            self.handle_enemy_collisions(objects)

    def get_player_attr(self,objects):
        if objects.subClass == 'player':
            self.player_position = objects.position
            self.player_direction = objects.x_direction

    def move_enemy(self, l_game_objects, o_player_engine, o_graphics_engine, objects,o_enemy_engine):
        if objects.isRendered:
            self.isHit(objects, l_game_objects, o_graphics_engine,o_enemy_engine)
            self.change_direction(objects)
            self.change_position(objects)

    def isHit(self, objects, l_game_objects, o_graphics_engine,o_enemy_engine):
        if objects.destroy:
            objects.destroy = False
            l_game_objects.remove(objects)
            o_graphics_engine.render_buffer.remove(objects)
        if objects.isHit and objects.hit_state == 1:
            objects.hit_state = 2
            objects.x_direction = objects.collisionObject.x_direction
            objects.isHit = False
        if objects.isHit and objects.hit_state == 2:
            objects.hit_state = 0
            objects.velocityX = 0
            objects.timer_started = False
            
    def handle_enemy_collisions(self,objects):
        if objects.hit_state == 2:
            if objects.collisionObject is not None and objects.collisionObject.subClass == 'enemy':
                objects.collisionObject.isHit = True
                objects.collisionObject.fromUnder = True
    def change_position(self, objects):
        if objects.hit_state == 2:
            objects.velocityX = 200
        else:
            objects.velocityX = 35


    def change_direction(self, objects):
        if objects.collisionObject is not None:

            if objects.collisionObject.subClass != "player":

                if objects.collisionLeft:
                    objects.x_direction = 1
                if objects.collisionRight:
                    objects.x_direction = -1
            if isinstance(objects.collisionObject,block_object.BlockObject):
                if objects.collisionObject.changeHit:
                    objects.isHit = True 
                    objects.fromUnder = True
                    objects.collisionObject.changeHit = False
            

    def enemy_ai(self, l_game_objects, o_player_engine, o_graphics_engine, objects):
        inRangeX = 128
        inRangeY = 32
        x_distance = objects.position[0] - self.player_position[0]
        y_distance = objects.position[1] - self.player_position[1]
        if objects.subClass == 'enemy' and objects.hit_state == 0:
            if abs(x_distance) < inRangeX and abs(y_distance) <= inRangeY:
                if x_distance < 0:    
                    objects.x_direction = 1
                if x_distance > 0:
                    objects.x_direction = -1

