import GameObjects.game_object as game_object
import sys
import pygame
sys.path.append("./AnimationSystem")
import anim_util

class BlockObject(game_object.GameObject, anim_util.AnimUtil):
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
        self.audio_clip = None
        self.audio_playing = False