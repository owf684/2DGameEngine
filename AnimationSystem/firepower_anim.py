import pygame
import anim_util
import sys
sys.path.append("./GameObjects")
import FirePower

class _firepower_anim(anim_util._anim_util):

    def __init__(self):
        super().__init__()
        self.frame_size = (8,8)
        self.frame_count = 4
        self.frame_duration = 100
        self.fireball_sprites = self.extract_frames("./Assets/PlayerSprites/FlowerPowerMario/fire_ball_sprite_sheet.png",self.frame_count,16,16)



    def main_loop(self,objects,levelHandler,delta_t,PlayerEngine):
        try:

            if isinstance(objects, FirePower._FirePower):
                self.determine_frame_count()
                objects.image = self.fireball_sprites[self.frame_index]
                    
        except Exception as Error:
            print("runtime error in firepower_anim.py::function main_loop(): ", Error)