import pygame
import copy

class _question_block:

    def __init__(self):
        self.current_time = 0
        self.elapsed_time = 0
        self.last_frame_time = 0
        self.frame_index = 0
        self.frame_size = (32, 32)
        self.frame_count = 3
        self.frame_duration = 200

        self.question_block_sprite_sheet = './Assets/Platforms/question_block_states/question_block_32x32_sprite_sheet.png'
        self.question_block_frames = self.extract_frames(self.question_block_sprite_sheet,self.frame_count,self.frame_size[0],self.frame_size[1])

    def main_loop(self, levelHandler):
        self.determine_frame_count()
        self.question_block_animation(levelHandler)
    def question_block_animation(self, levelHandler):
        for qb in levelHandler.question_blocks:
            if not qb.hit:

                qb.image = self.question_block_frames[self.frame_index]

    def determine_frame_count(self):

        self.current_time = pygame.time.get_ticks()
        self.elapsed_time = self.current_time - self.last_frame_time

        if self.elapsed_time >= self.frame_duration:
            self.frame_index = (self.frame_index + 1) % self.frame_count
            self.last_frame_time = self.current_time

    def extract_frames(self, path, num_frames, frame_width, frame_height):
        frames = list()
        sprite_sheet = pygame.image.load(path)
        for i in range(num_frames):
            frame = sprite_sheet.subsurface((0, i * frame_width, frame_width, frame_height))
            frames.append(frame)
        return frames