import pygame
import MarioFX
import BlockFX

class _AudioEngine:

    def __init__(self):
        self.MarioFX = MarioFX._MarioFX()
        self.BlockFX = BlockFX._BlockFX()
    def main_loop(self,objects,levelHandler,PlayerEngine):
        
        self.MarioFX.main_loop(objects,levelHandler,PlayerEngine)
        self.BlockFX.main_loop(objects,levelHandler,PlayerEngine)