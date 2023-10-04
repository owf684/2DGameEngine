import pygame



class _FlowerPower:

    def __init__(self):
        self.destroy = False
    def main_loop(self,GameObjects,levelHandler,PlayerEngine,objects):

        if objects.subClass == 'powerup' and 'flower' in objects.imagePath:

            self.track_scroll_flower(objects,levelHandler,PlayerEngine)

            self.detect_collisions(objects)

            if self.destroy:
                GameObjects.remove(objects)
                self.destroy = False
                levelHandler.clear_render_buffer = True

    def track_scroll_flower(self,objects,levelHandler,PlayerEngine):
        if PlayerEngine.scroll_level:
            objects.position[0] -= PlayerEngine.x_displacement

    def detect_collisions (self, objects):
        if objects.collisionObject is not None:
            if objects.collisionObject.subClass == 'player' and objects.collisionObject.power_up == 1:
                self.destroy = True
