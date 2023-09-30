import anim_util
import pygame


class _mario_anim(anim_util._anim_util):

    def __init__(self):
        super().__init__()

        self.frame_size = (32, 32)
        self.frame_count = 3
        self.frame_duration = 100

        self.jumping = False
        self.idle_right = pygame.image.load("./Assets/PlayerSprites/mario_32x32_idle_right.png").convert_alpha()
        self.idle_left = pygame.image.load('./Assets/PlayerSprites/mario_32x32_idle_left.png').convert_alpha()
        self.jump_left = pygame.image.load("./Assets/PlayerSprites/mario_32x32_jump_left.png").convert_alpha()
        self.jump_right = pygame.image.load("./Assets/PlayerSprites/mario_32x32_jump_right.png").convert_alpha()
        self.run_right = self.extract_frames("./Assets/PlayerSprites/mario_32x32_run_right.png", 3, 32, 32)
        self.run_left = self.extract_frames("./Assets/PlayerSprites/mario_32x32_run_left.png", 3, 32, 32)
        self.x_direction = 1
        self.playerObjectStored = False
        self.playerObject = None


    def main_loop(self,objects, input_dict):
        self.determine_frame_count()
        if objects.subClass == 'player':
            self.handle_run_animations(objects, input_dict)

            self.handle_jump_animations(objects, input_dict)

            self.handle_idle_animations(objects, input_dict)

    def handle_run_animations(self, objects, input_dict):

        if input_dict['l-shift'] == '1':
            self.frame_duration = 50
        else:
            self.frame_duration = 80

        if input_dict['right'] == '1':

            if not self.jumping:
                objects.image = self.run_right[self.frame_index]
                self.x_direction = 1
            elif objects.collisionDown and self.jumping:
                self.jumping = False

        if input_dict['left'] == '-1':

            if not self.jumping:
                objects.image = self.run_left[self.frame_index]
                self.x_direction = -1
            elif objects.collisionDown and self.jumping:
                self.jumping = False

    def handle_idle_animations(self, objects, input_dict):
        if input_dict['right'] == '0' and input_dict['left'] == '0':
            if self.x_direction == 1 and not self.jumping:
                objects.image = self.idle_right
            elif self.x_direction == -1 and not self.jumping:
                objects.image = self.idle_left
            elif objects.collisionDown and self.jumping:
                self.jumping = False

    def handle_jump_animations(self, objects, input_dict):

        if objects.velocityY > 0:
            if self.x_direction == 1:
                objects.image = self.jump_right
                self.jumping = True
            elif self.x_direction == -1:
                objects.image = self.jump_left
                self.jumping = True
            if objects.collisionDown and self.jumping:
                self.jumping = False
