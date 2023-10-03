import pygame
import SuperMushroom


class _PowerUpEngine:

    def __init__(self):
        self.SM = SuperMushroom._SuperMushroom()

    def main_loop(self, GameObjects, levelHandler, PlayerEngine, GraphicsEngine, objects):
        self.SM.main_loop(GameObjects, levelHandler, PlayerEngine, GraphicsEngine, objects)
