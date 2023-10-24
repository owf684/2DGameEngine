import pygame
import anim_util
import copy

class QuestionBlockAnim(anim_util.AnimUtil):

    def __init__(self):
        try:

            super().__init__()
            self.frame_size = (32, 32)
            self.frame_count = 3
            self.frame_duration = 200
            self.question_block_sprite_sheet = './Assets/Platforms/question_block_states/question_block_32x32_sprite_sheet.png'
            self.question_block_frames = self.extract_frames(self.question_block_sprite_sheet,self.frame_count,self.frame_size[0],self.frame_size[1])
        except Exception as Error:
            print("ERROR::question_block_anim.py::__init__()", Error)

    def main_loop(self, o_level_handler):
        try:

            self.determine_frame_count()
            self.question_block_animation(o_level_handler)
        except Exception as Error:
            print("ERROR::question_block_anim.py::main_loop()", Error)

    def question_block_animation(self, o_level_handler):
        try:

            for qb in o_level_handler.question_blocks:
                if not qb.hit:
                    qb.image = self.question_block_frames[self.frame_index]
        except Exception as Error:
            print("ERROR::question_block_anim.py::question_block_animation()", Error)
