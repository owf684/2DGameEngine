import pygame
import GameObjects.game_object as game_object


class PlayerObject(game_object.GameObject):

    def __init__(self):
        super().__init__()
        self.powerUp = False
        self.powerType =''