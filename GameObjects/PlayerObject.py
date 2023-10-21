import pygame
import GameObject
class _PlayerObject(GameObject._GameObject):

    def __init__(self):
        super().__init__()
        self.powerUp = False
        self.powerType =''