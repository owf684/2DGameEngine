import anim_util
import pygame



class _goomba_anim(anim_util._anim_util):
    def __init__(self):
        super().__init__()


        self.onEnemy = False
        self.goomba_idle = pygame.image.load("./Assets/EnemySprites/Goomba/goomba_32x32_idle.png").convert_alpha()
        self.goomba_walk = self.extract_frames("./Assets/EnemySprites/Goomba/sprite_sheet/goomba_32x32_walk.png" ,2 ,32 ,32)
        self.goomba_death = pygame.image.load("./Assets/EnemySprites/Goomba/goomba_32x32_death.png").convert_alpha()
        self.frame_duration = 200
        self.frame_count = 2

    def main_loop(self,objects):
        self.determine_frame_count()
        if objects.subClass == 'enemy' and "goomba" in objects.imagePath:
            if not objects.timer_started:
                self.goomba_walk_animation(objects)

            self.goomba_death_animation(objects)
    def goomba_walk_animation(self, objects):
        objects.image = self.goomba_walk[self.frame_index]
    
    def goomba_death_animation(self,objects):
        if objects.isHit and not objects.timer_started and not objects.fromUnder:
            objects.timer_started = True
            objects.reset_time_variables()
            objects.last_frame_time_2 = objects.determine_time_elapsed()
            objects.image = self.goomba_death
            objects.velocityX = 0
            objects.x_direction = 0
            objects.destroy_time = 1000
            
        if objects.isHit and objects.fromUnder and not objects.timer_started:
            #flip the image 
            objects.image = pygame.transform.flip(self.goomba_idle,False,True)
            objects.timer_started = True
            objects.reset_time_variables()
            objects.last_frame_time_2 = objects.determine_time_elapsed()
            objects.velocityY = 300
            objects.destroy_time = 10000 

        if objects.timer_started:
            print("gooma_anim.py::timer_started=True")
            if objects.determine_time_elapsed() > objects.destroy_time:
                objects.destroy = True
                print("goomba_anim.py::destroy=True")
                


            