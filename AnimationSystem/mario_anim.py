import anim_util
import pygame
import copy

class MarioAnim(anim_util.AnimUtil):

    def __init__(self):
        try:

            super().__init__()

            self.frame_size = (32, 32)
            self.frame_count = 3
            self.frame_duration = 100

            self.jumping = False
            self.latch = False

            self.shoot_latch = False
            self.pause_animation = False

            # mario sprites
            self.mario_sprites = list()
            self.idle_right = pygame.image.load("./Assets/PlayerSprites/mario/mario_32x32_idle_right.png").convert_alpha()
            self.idle_left = pygame.image.load('./Assets/PlayerSprites/mario/mario_32x32_idle_left.png').convert_alpha()
            self.jump_left = pygame.image.load("./Assets/PlayerSprites/mario/mario_32x32_jump_left.png").convert_alpha()
            self.jump_right = pygame.image.load("./Assets/PlayerSprites/mario/mario_32x32_jump_right.png").convert_alpha()
            self.run_right = self.extract_frames("./Assets/PlayerSprites/mario/mario_32x32_run_right.png", 3, 32, 32)
            self.run_left = self.extract_frames("./Assets/PlayerSprites/mario/mario_32x32_run_left.png", 3, 32, 32)
            self.death = pygame.image.load("./Assets/PlayerSprites/mario/mario_32x32_death.png").convert_alpha()

            self.mario_sprites.append(self.idle_right)
            self.mario_sprites.append(self.idle_left)
            self.mario_sprites.append(self.jump_left)
            self.mario_sprites.append(self.jump_right)
            self.mario_sprites.append(self.run_right)
            self.mario_sprites.append(self.run_left)

            # super mario sprites
            self.super_mario_sprites = list()
            self.super_mario_idle_right = pygame.image.load("./Assets/PlayerSprites/SuperMario/SuperMario_64x32_idle_right.png").convert_alpha()
            self.super_mario_idle_left = pygame.image.load("./Assets/PlayerSprites/SuperMario/SuperMario_64x32_idle_left.png").convert_alpha()
            self.super_mario_jump_left = pygame.image.load("./Assets/PlayerSprites/SuperMario/SuperMario_64x32_jump_left.png").convert_alpha()
            self.super_mario_jump_right = pygame.image.load("./Assets/PlayerSprites/SuperMario/SuperMario_64x32_jump_right.png").convert_alpha()
            self.super_mario_run_right = self.extract_frames("./Assets/PlayerSprites/SuperMario/SuperMario_64x32_run_right.png", 3, 32, 64)
            self.super_mario_run_left = self.extract_frames("./Assets/PlayerSprites/SuperMario/SuperMario_64x32_run_left.png", 3, 32, 64)
            self.super_mario_sprites.append(self.super_mario_idle_right)
            self.super_mario_sprites.append(self.super_mario_idle_left)
            self.super_mario_sprites.append(self.super_mario_jump_left)
            self.super_mario_sprites.append(self.super_mario_jump_right)
            self.super_mario_sprites.append(self.super_mario_run_right)
            self.super_mario_sprites.append(self.super_mario_run_left)


            self.flower_power_mario_idle_right = pygame.image.load("./Assets/PlayerSprites/FlowerPowerMario/FlowerPowerMario_idle_right.png").convert_alpha()
            self.flower_power_mario_run_right = self.extract_frames("./Assets/PlayerSprites/FlowerPowerMario/FlowerPowerMario_run_right.png",3,32,64)
            self.flower_power_mario_jump_right = pygame.image.load("./Assets/PlayerSprites/FlowerPowerMario/FlowerPowerMario_jump_right.png").convert_alpha()
            self.flower_power_mario_idle_left = pygame.transform.flip(self.flower_power_mario_idle_right,True,False)
            self.flower_power_mario_run_left = list()

            for frames in self.flower_power_mario_run_right:
                self.flower_power_mario_run_left.append(pygame.transform.flip(frames, True, False))

            self.flower_power_mario_jump_left = pygame.transform.flip(self.flower_power_mario_jump_right, True , False)
            self.flower_power_mario_sprites = list()
            self.flower_power_mario_sprites.append(self.flower_power_mario_idle_right)
            self.flower_power_mario_sprites.append(self.flower_power_mario_idle_left)
            self.flower_power_mario_sprites.append(self.flower_power_mario_jump_left)
            self.flower_power_mario_sprites.append(self.flower_power_mario_jump_right)
            self.flower_power_mario_sprites.append(self.flower_power_mario_run_right)
            self.flower_power_mario_sprites.append(self.flower_power_mario_run_left)

            self.flower_power_shoot_right = pygame.image.load("./Assets/PlayerSprites/FlowerPowerMario/FlowerPowerMario_shoot_right.png").convert_alpha()
            self.flower_power_shoot_left = pygame.transform.flip(self.flower_power_shoot_right,True,False)
            self.flower_power_shoot = list()
            self.flower_power_shoot.append(self.flower_power_shoot_right)
            self.flower_power_shoot.append(self.flower_power_shoot_left)

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
        except Exception as Error:
            print("ERROR::mario_anim.py::__init__()", Error)

    def main_loop(self, o_animation_system, objects, d_inputs, o_level_handler,delta_t, o_player_engine):
        try:
            if o_animation_system.reset_animations:
                self.current_mario_sprites = self.mario_sprites
                o_animation_system.reset_animations = False

            if objects.subClass == 'player':
                if not o_level_handler.pause_for_damage and not o_level_handler.trigger_death_animation and not o_level_handler.trigger_powerup_animation:

                    self.determine_frame_count()
                    if not self.pause_animation:

                        self.handle_run_animations(objects, d_inputs)

                        self.handle_jump_animations(objects, d_inputs)

                        self.handle_idle_animations(objects, d_inputs)

                    self.handle_power_ups(objects)

                    self.handle_fire_power(objects,d_inputs, o_player_engine)

                    objects.image.set_alpha(self.alpha)

                elif o_level_handler.pause_for_damage:

                    self.damage_animation(objects, o_level_handler,delta_t, o_player_engine)

                if o_level_handler.trigger_death_animation:
                    self.death_animation(objects,o_level_handler,delta_t, o_player_engine)

                if o_level_handler.trigger_powerup_animation:
                    self.power_up_animation(objects,o_level_handler,delta_t,o_player_engine)

                if o_level_handler.freeze_damage:

                    self.alpha = 128
                    
                    if self.determine_time_elapsed() >1500:
                        o_level_handler.freeze_damage = False
                else:
                    self.alpha = 255

        except Exception as Error:
            print("ERROR::mario_anim::main_loop()", Error)

    def handle_fire_power(self,objects,d_inputs, o_player_engine):
        try:

            if objects.power_up == 2 and d_inputs['attack'] == '1' and not self.shoot_latch and not o_player_engine.delay_power:
            
                self.reset_time_variables()
                self.last_frame_time_2 = self.determine_time_elapsed()
                self.pause_animation = True
                self.shoot_latch = True

                if objects.x_direction == 1:

                    objects.image = self.flower_power_shoot[0]
                else:
                
                    objects.image = self.flower_power_shoot[1]
        
            elif d_inputs['attack'] == '0' and self.shoot_latch:
            
                self.shoot_latch = False
        
            if self.pause_animation and self.determine_time_elapsed() > 100:
            
                self.pause_animation = False
        
        except Exception as Error:
        
            print("ERROR::mario_anim.py::handle_fire_power() ", Error)

    def power_up_animation(self, objects, o_level_handler, delta_t, o_player_engine):
        try:      
            # resets time variables and capture relevant sprites/frame when damaged
            if not self.powerup_frame_captured:
                self.frame_count = 7
                self.frame_duration = 150
                objects.position[1] -= 32
                self.powerup_frame_captured = True
                if objects.x_direction == 1:

                    objects.image = pygame.transform.flip(self.super_mario_transform[0],True,False)
                else:
                    objects.image = self.super_mario_transform[0]

                self.set_object(objects)
            
            self.determine_frame_count()
            
            if objects.x_direction == 1:
                objects.image = pygame.transform.flip(self.super_mario_transform[self.frame_index],True,False)
            else:
                objects.image = self.super_mario_transform[self.frame_index]

            if self.frame_index >= 6:
                # reset flags
                objects.powerUp = False
                self.frame_count = 3
                o_level_handler.trigger_powerup_animation = False
                self.powerup_frame_captured = False

                #set flags
                o_player_engine.superMario = True             

                # setup player object sprites
                if objects.power_up == 1:
                    self.current_mario_sprites = self.super_mario_sprites

                if objects.power_up == 2:
                    self.current_mario_sprites = self.flower_power_mario_sprites

                self.set_object(objects)
            
        except Exception as Error:
            print("ERROR::mario_anim.py::powerup_animation(): ", Error)

    def death_animation(self, objects,o_level_handler,delta_t, o_player_engine):
        try:

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
                o_level_handler.load_level = True
                o_level_handler.trigger_death_animation = False
                self.damage_frame_captured = False
                o_player_engine.superMario = False
                self.latch = False
                self.current_mario_sprites = self.mario_sprites
                objects.fromUnder = False
        
        except Exception as Error:

            print("ERROR::mario_anim.py::death_animation()", Error)
    
    def damage_animation(self, objects, o_level_handler, delta_t, o_player_engine):
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
            if self.determine_time_elapsed() > 600:

                # reset flags
                o_level_handler.pause_for_damage = False
                self.damage_frame_captured = False
                o_player_engine.superMario = False

                # set flags
                o_level_handler.decrease_power = True
                o_level_handler.freeze_damage = True

                # restart timer for freeze damage
                self.reset_time_variables()
                self.last_frame_time_2 = self.determine_time_elapsed()

                # setup player object image
                objects.image = self.transform_frame
                self.current_mario_sprites = self.mario_sprites
                self.set_object(objects)
        except Exception as Error:
            print("ERROR::mario_anim::damage_animation()", Error)

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
                self.set_object(objects)
                self.current_power = objects.power_up

            if objects.power_up == 2 and self.current_power != objects.power_up:
                self.current_mario_sprites = self.flower_power_mario_sprites
                objects.image = self.current_mario_sprites[0]
                self.set_object(objects)
                self.current_power = objects.power_up

        except Exception as Error:
            print("ERROR::mario_anim::handle_power_ups()", Error)

    def handle_run_animations(self, objects, d_inputs):
        try:
            if d_inputs['l-shift'] == '1':
                self.frame_duration = 50
            else:
                self.frame_duration = 80

            if d_inputs['right'] == '1':

                if not self.jumping:
                    objects.image = self.current_mario_sprites[4][self.frame_index]
                    self.current_sprite = 4

                    self.x_direction = 1
                elif objects.collisionDown and self.jumping:
                    self.jumping = False

            if d_inputs['left'] == '-1':

                if not self.jumping:
                    objects.image = self.current_mario_sprites[5][self.frame_index]
                    self.current_sprite = 5
                    self.x_direction = -1
                elif objects.collisionDown and self.jumping:
                    self.jumping = False
        except Exception as Error:
            print("ERROR::mario_anim.py::handle_run_animations()", Error)

    def handle_idle_animations(self, objects, d_inputs):
        try:
            
            if d_inputs['right'] == '0' and d_inputs['left'] == '0':
                if self.x_direction == 1 and not self.jumping:
                    objects.image = self.current_mario_sprites[0]
                    self.current_sprite = 0
                elif self.x_direction == -1 and not self.jumping:
                    objects.image = self.current_mario_sprites[1]
                    self.current_sprite = 1
                elif objects.collisionDown and self.jumping:
                    self.jumping = False
        except Exception as Error:
            print("ERROR::mario_anim.py::handle_idle_animations()", Error)
    
    def handle_jump_animations(self, objects, d_inputs):
        try:
            if objects.jumping:
                if objects.x_direction == 1:
                    objects.image = self.current_mario_sprites[3]
                    self.current_sprite = 3
                    self.jumping = True
                elif objects.x_direction == -1:
                    objects.image = self.current_mario_sprites[2]
                    self.current_sprite = 2
                    self.jumping = True
                if objects.collisionDown and self.jumping:
                    self.jumping = False
        except Exception as Error:
            print("ERROR::mario_anim.py::handle_jump_animations()", Error)
            
    
    def set_object(self, objects):
        try:

            objects._set_sprite_size(objects.image)
            objects._set_rect(objects.sprite_size)
            objects._set_mask()
            
        except Exception as Error:
            print("ERROR::mario_anim.py::set_object()", Error)