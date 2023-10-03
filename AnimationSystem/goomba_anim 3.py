import anim_util
import pygame



class _goomba_anim(anim_util._anim_util):
    def __init__(self):
        super().__init__()


        self.onEnemy = False
        self.goomba_idle = pygame.image.load("./Assets/EnemySprites/Goomba/goomba_32x32_idle.png").convert_alpha()
        self.goomba_walk = self.extract_frames("./Assets/EnemySprites/Goomba/sprite_sheet/goomba_32x32_walk.png" ,2 ,32 ,32)
        self.frame_duration = 200
        self.frame_count = 2

    def main_loop(self,objects):
        self.determine_frame_count()
        if objects.subClass == 'enemy' and "goomba" in objects.imagePath:
            self.goomba_walk_animation(objects)
    def goomba_walk_animation(self, objects):
        objects.image = self.goomba_walk[self.frame_index]