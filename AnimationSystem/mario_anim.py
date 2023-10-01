import anim_util
import pygame


class _mario_anim(anim_util._anim_util):

    def __init__(self):
        super().__init__()

        self.frame_size = (32, 32)
        self.frame_count = 3
        self.frame_duration = 100

        self.jumping = False

        #mario sprites
        self.mario_sprites = list()
        self.idle_right = pygame.image.load("./Assets/PlayerSprites/mario_32x32_idle_right.png").convert_alpha()
        self.idle_left = pygame.image.load('./Assets/PlayerSprites/mario_32x32_idle_left.png').convert_alpha()
        self.jump_left = pygame.image.load("./Assets/PlayerSprites/mario_32x32_jump_left.png").convert_alpha()
        self.jump_right = pygame.image.load("./Assets/PlayerSprites/mario_32x32_jump_right.png").convert_alpha()
        self.run_right = self.extract_frames("./Assets/PlayerSprites/mario_32x32_run_right.png", 3, 32, 32)
        self.run_left = self.extract_frames("./Assets/PlayerSprites/mario_32x32_run_left.png", 3, 32, 32)
        self.mario_sprites.append(self.idle_right)
        self.mario_sprites.append(self.idle_left)
        self.mario_sprites.append(self.jump_left)
        self.mario_sprites.append(self.jump_right)
        self.mario_sprites.append(self.run_right)
        self.mario_sprites.append(self.run_left)

        #super mario sprites
        self.super_mario_sprites = list()
        self.super_mario_idle_right = pygame.image.load("./Assets/PlayerSprites/SuperMario_64x32_idle_right.png").convert_alpha()
        self.super_mario_idle_left = pygame.image.load("./Assets/PlayerSprites/SuperMario_64x32_idle_left.png").convert_alpha()
        self.super_mario_jump_left = pygame.image.load("./Assets/PlayerSprites/SuperMario_64x32_jump_left.png").convert_alpha()
        self.super_mario_jump_right = pygame.image.load("./Assets/PlayerSprites/SuperMario_64x32_jump_right.png").convert_alpha()
        self.super_mario_run_right = self.extract_frames("./Assets/PlayerSprites/SuperMario_64x32_run_right.png", 3, 32, 64)
        self.super_mario_run_left = self.extract_frames("./Assets/PlayerSprites/SuperMario_64x32_run_left.png", 3, 32, 64)
        self.super_mario_sprites.append(self.super_mario_idle_right)
        self.super_mario_sprites.append(self.super_mario_idle_left)
        self.super_mario_sprites.append(self.super_mario_jump_left)
        self.super_mario_sprites.append(self.super_mario_jump_right)
        self.super_mario_sprites.append(self.super_mario_run_right)
        self.super_mario_sprites.append(self.super_mario_run_left)

        self.current_mario_sprites = self.mario_sprites

        self.x_direction = 1
        self.playerObjectStored = False
        self.playerObject = None

        self.current_power = 0

    def main_loop(self,objects, input_dict):
        self.determine_frame_count()
        if objects.subClass == 'player':
            self.handle_run_animations(objects, input_dict)

            self.handle_jump_animations(objects, input_dict)

            self.handle_idle_animations(objects, input_dict)

            self.handle_power_ups(objects)

    def handle_power_ups(self,objects):
        if objects.power_up == 0 and self.current_power != objects.power_up:
            self.current_mario_sprites = self.mario_sprites
            objects.image = self.current_mario_sprites[0]
            self.set_object(objects)
            self.current_power = objects.power_up

        if objects.power_up == 1 and self.current_power != objects.power_up:
            self.current_mario_sprites = self.super_mario_sprites
            objects.image = self.current_mario_sprites[0]
            self.set_object(objects)

            self.current_power = objects.power_up

    def handle_run_animations(self, objects, input_dict):

        if input_dict['l-shift'] == '1':
            self.frame_duration = 50
        else:
            self.frame_duration = 80

        if input_dict['right'] == '1':

            if not self.jumping:
                objects.image = self.current_mario_sprites[4][self.frame_index]
                self.x_direction = 1
            elif objects.collisionDown and self.jumping:
                self.jumping = False

        if input_dict['left'] == '-1':

            if not self.jumping:
                objects.image = self.current_mario_sprites[5][self.frame_index]
                self.x_direction = -1
            elif objects.collisionDown and self.jumping:
                self.jumping = False

    def handle_idle_animations(self, objects, input_dict):
        if input_dict['right'] == '0' and input_dict['left'] == '0':
            if self.x_direction == 1 and not self.jumping:
                objects.image = self.current_mario_sprites[0]
            elif self.x_direction == -1 and not self.jumping:
                objects.image = self.current_mario_sprites[1]
            elif objects.collisionDown and self.jumping:
                self.jumping = False

    def handle_jump_animations(self, objects, input_dict):

        if objects.velocityY > 0:
            if self.x_direction == 1:
                objects.image = self.current_mario_sprites[3]
                self.jumping = True
            elif self.x_direction == -1:
                objects.image = self.current_mario_sprites[2]
                self.jumping = True
            if objects.collisionDown and self.jumping:
                self.jumping = False
    def set_object(self,objects):
        objects._set_sprite_size(objects.image)
        objects._set_rect(objects.sprite_size)
        objects._set_mask()