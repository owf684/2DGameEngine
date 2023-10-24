
import anim_util
import pygame
class KoopaAnim(anim_util.AnimUtil):

    def __init__(self):
        try:

            super().__init__()

            self.koopa_troopa_walk_left = self.extract_frames("./Assets/EnemySprites/KoopaTroopa/sprite_sheet/KoopaTroopa_walkiing_left.png",2, 32,48)
            self.koopa_troopa_walk_right = list()
            for frames in self.koopa_troopa_walk_left:
                self.koopa_troopa_walk_right.append(pygame.transform.flip(frames,True,False))

            self.koopa_shell = pygame.image.load("./Assets/EnemySprites/KoopaTroopa/states/KoopaShell.png")
            self.koopa_shell_sprite_sheet = self.extract_frames("./Assets/EnemySprites/KoopaTroopa/states/KoopaShell_revive.png", 2 , 32 , 48)
            self.frame_count = 2
            self.frame_duration = 200
        except Exception as Error:
            print("ERROR::koopa_anim.py::__init__()", Error)

    def main_loop(self,objects, o_enemy_engine):
        try:
            self.determine_frame_count()
            if objects.subClass == 'enemy' and "Koopa" in objects.imagePath:
                if not objects.timer_started:

                    self.koopa_walk_animation(objects)

                self.handle_koopa_damage(objects, o_enemy_engine)

        except Exception as Error:
            print("ERROR::koopa_anim.py::main_loop()", Error)

    def handle_koopa_damage(self,objects, o_enemy_engine):
        try:
            if objects.isHit and not objects.timer_started and not objects.fromUnder and objects.hit_state == 0:
                o_enemy_engine.triggerStompAudio = True
                objects.timer_started = True
                objects.reset_time_variables()
                objects.last_frame_time_2 = objects.determine_time_elapsed()
                objects.image = self.koopa_shell
                objects.velocityX = 0
                objects.isHit = False
                objects.hit_state = 1 
                #objects.x_direction = 0
                objects.destroy_time = 3000
            
            elif objects.isHit and objects.fromUnder and not objects.timer_started:
                o_enemy_engine.triggerStompAudio = True
                #flip the image 
                objects.image = pygame.transform.flip(self.koopa_shell,False,True)
                objects.timer_started = True
                objects.reset_time_variables()
                objects.last_frame_time_2 = objects.determine_time_elapsed()
                objects.velocityY = 300
                objects.destroy_time = 10000 
            elif objects.hit_state == 2:
                objects.image = self.koopa_shell
                
            if objects.timer_started and objects.hit_state == 1:
                if objects.determine_time_elapsed() > objects.destroy_time and not objects.trigger_next_animation:
                    objects.reset_time_variables()
                    objects.last_frame_time_2 = objects.determine_time_elapsed()
                    objects.trigger_next_animation = True
                elif objects.determine_time_elapsed() > objects.destroy_time and objects.trigger_next_animation:
                    objects.timer_started = False
                    objects.trigger_next_animation = False
                    objects.isHit = False
                    objects.hit_state = 0
                    if objects.x_direction == -1:

                        objects.image = self.koopa_troopa_walk_left[0]
                    else:
                        objects.image = self.koopa_troopa_walk_right[0]

                if objects.trigger_next_animation:
                    objects.image = self.koopa_shell_sprite_sheet[self.frame_index]
            
        except Exception as Error:
            print("ERROR::koopa_anim.py::handle_koopa_damage()", Error)   

    def koopa_walk_animation(self,objects):
        try:

            if objects.x_direction == -1:
                objects.image = self.koopa_troopa_walk_left[self.frame_index]
            elif objects.x_direction == 1:
                objects.image = self.koopa_troopa_walk_right[self.frame_index]
        except Exception as Error:
            print("ERROR::koopa_anim.py::koopa_walk_animation.py", Error)