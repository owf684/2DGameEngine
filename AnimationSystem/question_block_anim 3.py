import pygame
import anim_util
import copy

class _question_block(anim_util._anim_util):

    def __init__(self):
        super().__init__()
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

