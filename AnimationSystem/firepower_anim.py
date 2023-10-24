import pygame
import anim_util
import sys
sys.path.append("./GameObjects")
import fire_power

class FirepowerAnim(anim_util.AnimUtil):

    def __init__(self):
        try:

            super().__init__()
            self.frame_size = (8,8)
            self.frame_count = 4
            self.frame_duration = 100
            self.fireball_sprites = self.extract_frames("./Assets/PlayerSprites/FlowerPowerMario/fire_ball_sprite_sheet.png",self.frame_count,16,16)
        except Exception as Error:
            print("ERROR::firepower_anim.py::__init__()", Error)


    def main_loop(self,objects,o_level_handler,delta_t,o_player_engine):
        try:

            if isinstance(objects, fire_power.FirePower):
                self.determine_frame_count()
                objects.image = self.fireball_sprites[self.frame_index]
                    
        except Exception as Error:
            print("runtime error in firepower_anim.py::function main_loop(): ", Error)