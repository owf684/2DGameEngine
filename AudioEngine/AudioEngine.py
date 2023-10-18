import pygame
import MarioFX
import BlockFX
import EnemyFX

class _AudioEngine:

    def __init__(self):
        self.MarioFX = MarioFX._MarioFX()
        self.BlockFX = BlockFX._BlockFX()
        self.EnemyFX = EnemyFX._EnemyFX()
    def main_loop(self,objects,levelHandler,PlayerEngine, EnemyEngine):
        
        self.MarioFX.main_loop(objects,levelHandler,PlayerEngine)
        self.BlockFX.main_loop(objects,levelHandler,PlayerEngine)
        self.EnemyFX.main_loop(objects,levelHandler,EnemyEngine)