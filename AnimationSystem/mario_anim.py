import anim_util
import pygame
import copy

class _mario_anim(anim_util._anim_util):

    def __init__(self):
        super().__init__()

        self.frame_size = (32, 32)
        self.frame_count = 3
        self.frame_duration = 100

        self.jumping = False
        self.latch = False


        # mario sprites
        self.mario_sprites = list()
        self.idle_right = pygame.image.load("./Assets/PlayerSprites/mario_32x32_idle_right.png").convert_alpha()
        self.idle_left = pygame.image.load('./Assets/PlayerSprites/mario_32x32_idle_left.png').convert_alpha()
        self.jump_left = pygame.image.load("./Assets/PlayerSprites/mario_32x32_jump_left.png").convert_alpha()
        self.jump_right = pygame.image.load("./Assets/PlayerSprites/mario_32x32_jump_right.png").convert_alpha()
        self.run_right = self.extract_frames("./Assets/PlayerSprites/mario_32x32_run_right.png", 3, 32, 32)
        self.run_left = self.extract_frames("./Assets/PlayerSprites/mario_32x32_run_left.png", 3, 32, 32)
        self.death = pygame.image.load("./Assets/PlayerSprites/mario_32x32_death.png").convert_alpha()

        self.mario_sprites.append(self.idle_right)
        self.mario_sprites.append(self.idle_left)
        self.mario_sprites.append(self.jump_left)
        self.mario_sprites.append(self.jump_right)
        self.mario_sprites.append(self.run_right)
        self.mario_sprites.append(self.run_left)

        # super mario sprites
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

        self.super_mario_transform = self.extract_frames("./Assets/PlayerSprites/SuperMario_32x64_powerup_transform.png",7,32,64)
        self.current_mario_sprites = self.mario_sprites

        self.x_direction = 1
        self.playerObjectStored = False
        self.playerObject = None
        self.damage_count = 0
        self.current_power = 0
        self.current_sprite = 0
        self.alpha = 255
        self.damage_frame = self.idle_right
        self.transform_frame = self.idle_right
        self.damage_frame_captured = False

    def main_loop(self, objects, input_dict, levelHandler,delta_t, PlayerEngine):
        try:
            if objects.subClass == 'player':
                if not levelHandler.pause_for_damage and not levelHandler.trigger_death_animation and not levelHandler.trigger_powerup_animation:

                    self.determine_frame_count()

                    self.handle_run_animations(objects, input_dict)

                    self.handle_jump_animations(objects, input_dict)

                    self.handle_idle_animations(objects, input_dict)

                    self.handle_power_ups(objects)

                    objects.image.set_alpha(self.alpha)

                elif levelHandler.pause_for_damage:

                    self.damage_animation(objects, levelHandler,delta_t, PlayerEngine)

                if levelHandler.trigger_death_animation:
                    self.death_animation(objects,levelHandler,delta_t, PlayerEngine)

                if levelHandler.trigger_powerup_animation:
                    self.power_up_animation(objects,levelHandler,delta_t,PlayerEngine)

                if levelHandler.freeze_damage:

                    self.alpha = 128
                    
                    if self.determine_time_elapsed() >1500:
                        levelHandler.freeze_damage = False
                else:
                    self.alpha = 255

        except Exception as Error:
            print("runtime error in mario_anim. Function main_loop: ", Error)

    def power_up_animation(self, objects, levelHandler, delta_t, PlayerEngine):
        try:      
            # resets time variables and capture relevant sprites/frame when damaged
            if not self.powerup_frame_captured:
                self.frame_count = 7
                self.frame_duration = 150
                objects.position[1] -= 32
                self.powerup_frame_captured = True
                if objects.x_direction == 1:

                    objects.image = pygame.transform.flip(self.super_mario_transform[0],True,False)
                self.set_object(objects)
            print("mario_anim.py::self.frame_index= ", self.frame_index)
            self.determine_frame_count()
            if objects.x_direction == 1:
                objects.image = pygame.transform.flip(self.super_mario_transform[self.frame_index],True,False)
            else:
                objects.image = self.super_mario_transform[self.frame_index]

            if self.frame_index >= 6:
                # reset flags
                print("mario_anim.py::resetting variables")
                self.frame_count = 3
                levelHandler.trigger_powerup_animation = False
                self.powerup_frame_captured = False
                objects.powerup = False
                objects.collisionObject.imagePath = 'None'
                #set flags
                PlayerEngine.superMario = True
                objects.power_up = 1
                # setup player object image
                self.current_mario_sprites = self.super_mario_sprites
                self.set_object(objects)
            
        except Exception as Error:
            print("runtime error in mario_anim.py::function powerup_animation(): ", Error)

    def death_animation(self, objects,levelHandler,delta_t, PlayerEngine):
        if not self.damage_frame_captured:

            objects.image = self.death
            self.reset_time_variables()
            self.last_frame_time_2 = self.determine_time_elapsed()
    
            self.damage_frame_captured = True
        time_elapsed = self.determine_time_elapsed()
        if time_elapsed > 500 and not self.latch:
            objects.velocityY = 500
            self.latch = True
            objects.fromUnder = True
            objects.rect.width = 0
            objects.rect.height = 0
        if self.latch:
            objects.collisionUp = False
        if time_elapsed > 3000:
            levelHandler.load_level = True
            levelHandler.trigger_death_animation = False
            self.damage_frame_captured = False
            PlayerEngine.superMario = False
            self.latch = False
            objects.fromUnder = False
    def damage_animation(self, objects, levelHandler, delta_t, PlayerEngine):
        try:      
            # resets time variables and capture relevant sprites/frame when damaged
            if not self.damage_frame_captured:

                self.damage_frame = objects.image

                if self.current_sprite == 4 or self.current_sprite == 5:
                    self.transform_frame = self.mario_sprites[self.current_sprite][self.frame_index]
                else:
                    self.transform_frame = self.mario_sprites[self.current_sprite]

                self.damage_frame_captured = True
                self.reset_time_variables()
                self.last_frame_time_2 = self.determine_time_elapsed()

            # go little
            if self.damage_count == 0:
            
                objects.image = self.transform_frame
                objects.image.set_alpha(128)
                self.set_object(objects)

            # go big
            if self.damage_count > 0.4:
                objects.image = self.damage_frame
                objects.image.set_alpha(128)
                self.set_object(objects)

            # increment damage count by delta_t. ensures consistent damage animation
            self.damage_count += delta_t

            # reset damage count
            if self.damage_count > 0.8:
                self.damage_count = 0

            # check elapsed time
            if self.determine_time_elapsed() > 1200:

                # reset flags
                levelHandler.pause_for_damage = False
                self.damage_frame_captured = False
                PlayerEngine.superMario = False

                # set flags
                levelHandler.decrease_power = True
                levelHandler.freeze_damage = True

                # restart timer for freeze damage
                self.reset_time_variables()
                self.last_frame_time_2 = self.determine_time_elapsed()

                # setup player object image
                objects.image = self.transform_frame
                self.current_mario_sprites = self.mario_sprites
                self.set_object(objects)
        except Exception as Error:
            print("runtime error in mario_anim. function damage_animation: ", Error)

    def handle_power_ups(self,objects):
        try:
            if objects.power_up == 0 and self.current_power != objects.power_up:
                self.current_mario_sprites = self.mario_sprites
                objects.image = self.current_mario_sprites[0]
                self.set_object(objects)
                self.current_power = objects.power_up

            if objects.power_up == 1 and self.current_power != objects.power_up:
                self.current_mario_sprites = self.super_mario_sprites
                objects.image = self.current_mario_sprites[0]
                objects.position[1] -= 32
                self.set_object(objects)


                self.current_power = objects.power_up
        except Exception as Error:
            print("runtime error in mario_anim. Function handle_power_ups: ", Error)
    def handle_run_animations(self, objects, input_dict):
        try:
            if input_dict['l-shift'] == '1':
                self.frame_duration = 50
            else:
                self.frame_duration = 80

            if input_dict['right'] == '1':

                if not self.jumping:
                    objects.image = self.current_mario_sprites[4][self.frame_index]
                    self.current_sprite = 4

                    self.x_direction = 1
                elif objects.collisionDown and self.jumping:
                    self.jumping = False

            if input_dict['left'] == '-1':

                if not self.jumping:
                    objects.image = self.current_mario_sprites[5][self.frame_index]
                    self.current_sprite = 5
                    self.x_direction = -1
                elif objects.collisionDown and self.jumping:
                    self.jumping = False
        except Exception as Error:
            print("runtime error in mario_anim. Function handle_run_animations: ", Error)

    def handle_idle_animations(self, objects, input_dict):
        try:
            
            if input_dict['right'] == '0' and input_dict['left'] == '0':
                if self.x_direction == 1 and not self.jumping:
                    objects.image = self.current_mario_sprites[0]
                    self.current_sprite = 0
                elif self.x_direction == -1 and not self.jumping:
                    objects.image = self.current_mario_sprites[1]
                    self.current_sprite = 1
                elif objects.collisionDown and self.jumping:
                    self.jumping = False
        except Exception as Error:
            print("runtime error in mario_anim. Function handle_idle_animations: ", Error)
    
    def handle_jump_animations(self, objects, input_dict):
        try:
            if objects.velocityY > 0:
                if self.x_direction == 1:
                    objects.image = self.current_mario_sprites[3]
                    self.current_sprite = 3
                    self.jumping = True
                elif self.x_direction == -1:
                    objects.image = self.current_mario_sprites[2]
                    self.current_sprite = 2
                    self.jumping = True
                if objects.collisionDown and self.jumping:
                    self.jumping = False
        except Exception as Error:
            print("runtime error in mario_anim. Function handle_jump_animations: ", Error)
            
    
    def set_object(self, objects):
        try:

            objects._set_sprite_size(objects.image)
            objects._set_rect(objects.sprite_size)
            objects._set_mask()
            
        except Exception as Error:
            print("runtime error in mario_anim. Function set_object: ", Error)