
import anim_util
import pygame
class _koop_anim(anim_util._anim_util):

    def __init__(self):
        try:

            super().__init__()

            self.koopa_troopa_walk_left = self.extract_frames("./Assets/EnemySprites/KoopaTroopa/sprite_sheet/KoopaTroopa_walkiing_left.png",2, 32,48)
            self.koopa_troopa_walk_right = list()
            for frames in self.koopa_troopa_walk_left:
                self.koopa_troopa_walk_right.append(pygame.transform.flip(frames,True,False))

            self.koopa_shell = pygame.image.load("./Assets/EnemySprites/KoopaTroopa/states/KoopaShell.png")
            self.frame_count = 2
            self.frame_duration = 200
        except Exception as Error:
            print("ERROR::koopa_anim.py::__init__()", Error)

    def main_loop(self,objects, EnemyEngine):
        try:
            self.determine_frame_count()
            if objects.subClass == 'enemy' and "Koopa" in objects.imagePath:
                self.koopa_walk_animation(objects)

        except Exception as Error:
            print("ERROR::koopa_anim.py::main_loop()", Error)
    
    def koopa_walk_animation(self,objects):
        try:

            if objects.x_direction == -1:
                objects.image = self.koopa_troopa_walk_left[self.frame_index]
            elif objects.x_direction == 1:
                objects.image = self.koopa_troopa_walk_right[self.frame_index]
        except Exception as Error:
            print("ERROR::koopa_anim.py::koopa_walk_animation.py", Error)