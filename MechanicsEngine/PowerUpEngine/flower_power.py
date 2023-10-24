import pygame
import sys
sys.path.append('./GameObjects')
import fire_power


class FlowerPower:

    def __init__(self):
        self.destroy = False
    def main_loop(self,l_game_objects,o_level_handler,o_player_engine,objects):

        if objects.subClass == 'powerup' and 'flower' in objects.imagePath:

            self.track_scroll_flower(objects,o_level_handler,o_player_engine)

            self.detect_collisions(objects)

            if self.destroy:
                l_game_objects.remove(objects)
                self.destroy = False
                o_level_handler.clear_render_buffer = True

        if isinstance(objects,fire_power.FirePower):
            self.track_scroll_fire_ball(objects,o_player_engine)
            self.detect_collisions(objects)
            if self.destroy:
                l_game_objects.remove(objects)
                self.destroy = False
                o_level_handler.clear_render_buffer = True

    def track_scroll_fire_ball(self,objects,o_player_engine):
        if o_player_engine.scroll_level:
            objects.position[0] -= o_player_engine.x_displacement

    def track_scroll_flower(self,objects,o_level_handler,o_player_engine):
        if o_player_engine.scroll_level:
            objects.position[0] -= o_player_engine.x_displacement

    def detect_collisions (self, objects):
        if objects.isHit:
            self.destroy = True
