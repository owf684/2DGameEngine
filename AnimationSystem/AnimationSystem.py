import pygame
import question_block_anim
import sys


class _AnimationSystem:

    def __init__(self):

        self.goomba_current_time = 0
        self.goomba_last_frame_time = 0
        self.goomba_elapsed_time = 0
        self.frame_size = (32, 32)
        self.frame_count = 3
        self.frame_duration = 100

        self.current_time = 0
        self.elapsed_time = 0
        self.last_frame_time = 0
        self.frame_index = 0

        self.jumping = False
        self.idle_right = pygame.image.load("./Assets/PlayerSprites/mario_32x32_idle_right.png")
        self.idle_left = pygame.image.load('./Assets/PlayerSprites/mario_32x32_idle_left.png')
        self.jump_left = pygame.image.load("./Assets/PlayerSprites/mario_32x32_jump_left.png")
        self.jump_right = pygame.image.load("./Assets/PlayerSprites/mario_32x32_jump_right.png")
        self.run_right = self.extract_frames("./Assets/PlayerSprites/mario_32x32_run_right.png",3,32,32)
        self.run_left = self.extract_frames("./Assets/PlayerSprites/mario_32x32_run_left.png",3,32,32)
        self.jump_lock = False
        self.onEnemy = False
        self.x_direction = 1
        self.playerObjectStored = False
        self.playerObject = None

        self.goomba_idle = pygame.image.load("./Assets/EnemySprites/Goomba/goomba_32x32_idle.png")
        self.goomba_walk = self.extract_frames("./Assets/EnemySprites/Goomba/sprite_sheet/goomba_32x32_walk.png",2,32,32)
        self.goomba_frame_index = 0
        self.goomba_frame_duration = 200

        self.qb = question_block_anim._question_block()
    def main_loop(self, GameObjects, input_dict,levelHandler):
        self.qb.main_loop(levelHandler)
        self.determine_frame_count()

        for objects in GameObjects:
            if objects.subClass == 'player':
                self.handle_run_animations(objects, input_dict)

                self.handle_jump_animations(objects, input_dict)

                self.handle_idle_animations(objects, input_dict)
            if objects.subClass == 'enemy':
                self.goomba_walk_animation(objects)
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
    def goomba_walk_animation(self, objects):

        objects.image = self.goomba_walk[self.goomba_frame_index]
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

    def determine_frame_count(self):
        self.current_time = pygame.time.get_ticks()
        self.goomba_current_time = pygame.time.get_ticks()
        self.elapsed_time = self.current_time - self.last_frame_time
        self.goomba_elapsed_time = self.current_time - self.goomba_last_frame_time

        if self.elapsed_time >= self.frame_duration:
            self.frame_index = (self.frame_index + 1) % self.frame_count
            self.last_frame_time = self.current_time

        if self.goomba_elapsed_time >= self.goomba_frame_duration:
            self.goomba_frame_index = (self.goomba_frame_index + 1) % 2
            self.goomba_last_frame_time = self.goomba_current_time
    def extract_frames(self, path, num_frames, frame_width, frame_height):
        frames = list()
        sprite_sheet = pygame.image.load(path)
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((0, i*frame_width, frame_width,frame_height))
            frames.append(frame)
        return frames
    '''def extract_frames(self, frame_path):
        frames = list()
        sprite_sheet = pygame.image.load(frame_path)
        frame = sprite_sheet.subsurface((0, 0, self.frame_size[0], self.frame_size[1]))
        frames.append(frame)
        frame = sprite_sheet.subsurface((32, 0, self.frame_size[0], self.frame_size[1]))
        frames.append(frame)
        frame = sprite_sheet.subsurface((0, 32, self.frame_size[0], self.frame_size[1]))
        frames.append(frame)
        return frames'''
