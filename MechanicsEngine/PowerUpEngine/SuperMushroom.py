import sys
import pygame
import copy
sys.path.append('./GameObjects')
sys.path.append("./AnimationSystem")
import BlockObject


class _SuperMushroom:

    def __init__(self):
        self.velocity_x = 1
        self.init_direction = 1
        self.destroy = False

    def main_loop(self, GameObjects, levelHandler, PlayerEngine, GraphicsEngine, objects):
        if objects.subClass == 'powerup' and 'mushroom' in objects.imagePath:
            if objects.isRendered:

                self.move_mushroom(objects)

                self.detectCollisions(objects)

                if self.destroy:
                    GameObjects.remove(objects)
                    self.destroy = False
                    levelHandler.clear_render_buffer = True

            self.track_scroll_mushroom(objects, levelHandler, PlayerEngine)

    def track_scroll_mushroom(self, objects, levelHandler, PlayerEngine):

        if PlayerEngine.scroll_level:
            objects.position[0] -= PlayerEngine.x_displacement

    def move_mushroom(self, objects):
        objects.velocityX = 50

    def detectCollisions(self, objects):
        if objects.collisionObject is not None:
            if objects.collisionObject.subClass != 'player':

                if objects.collisionLeft:
                    objects.x_direction = 1

                if objects.collisionRight:
                    objects.x_direction = -1

                if isinstance(objects.collisionObject, BlockObject._BlockObject):
                    if objects.collisionObject.changeHit:
                        objects.x_direction *= -1
                        objects.collisionObject.changeHit = False

        if objects.isHit:
            self.destroy = True
