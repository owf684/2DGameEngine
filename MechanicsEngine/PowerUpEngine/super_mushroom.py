import sys
import pygame
import copy
sys.path.append('./GameObjects')
sys.path.append("./AnimationSystem")
import block_object


class SuperMushroom:

    def __init__(self):
        self.velocity_x = 1
        self.init_direction = 1
        self.destroy = False

    def main_loop(self, l_game_objects, o_level_handler, o_player_engine, o_graphics_engine, objects):
        if objects.subClass == 'powerup' and 'mushroom' in objects.imagePath:
            if objects.isRendered:

                self.move_mushroom(objects)

                self.detectCollisions(objects)

                if self.destroy:
                    l_game_objects.remove(objects)
                    self.destroy = False
                    o_level_handler.clear_render_buffer = True

            self.track_scroll_mushroom(objects, o_level_handler, o_player_engine)

    def track_scroll_mushroom(self, objects, o_level_handler, o_player_engine):

        if o_player_engine.scroll_level:
            objects.position[0] -= o_player_engine.x_displacement

    def move_mushroom(self, objects):
        objects.velocityX = 50

    def detectCollisions(self, objects):
        if objects.collisionObject is not None:
            if objects.collisionObject.subClass != 'player':

                if objects.collisionLeft:
                    objects.x_direction = 1

                if objects.collisionRight:
                    objects.x_direction = -1

                if isinstance(objects.collisionObject, block_object.BlockObject):
                    if objects.collisionObject.changeHit:
                        objects.x_direction *= -1
                        objects.collisionObject.changeHit = False

        if objects.isHit:
            self.destroy = True
