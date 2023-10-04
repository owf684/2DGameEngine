import pygame
import SuperMushroom
import FlowerPower

class _PowerUpEngine:

    def __init__(self):
        self.SM = SuperMushroom._SuperMushroom()
        self.FP = FlowerPower._FlowerPower()
    def main_loop(self, GameObjects, levelHandler, PlayerEngine, GraphicsEngine, objects):
        self.SM.main_loop(GameObjects, levelHandler, PlayerEngine, GraphicsEngine, objects)
        self.FP.main_loop(GameObjects,levelHandler, PlayerEngine, objects)