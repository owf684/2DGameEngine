import GameObject
import sys
import pygame
sys.path.append("./AnimationSystem")
import anim_util

class _BlockObject(GameObject._GameObject, anim_util._anim_util):
    def __init__(self):
        super().__init__()

        self.question_block_object = None
        self.question_block_trigger = False
        self.push_block_trigger = False
        self.release_item_trigger = False
        self.theta = 1
        self.item = None
        self.changeHit = False
        self.pauseHit = False
        self.last_frame_time_2 = 0
        self.item_released = False