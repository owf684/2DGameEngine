import pygame
import MechanicsEngine.PowerUpEngine.super_mushroom as super_mushroom
import MechanicsEngine.PowerUpEngine.flower_power as flower_power

class PowerupEngine:

    def __init__(self):
        self.o_super_mushroom = super_mushroom.SuperMushroom()
        self.o_flower_power = flower_power.FlowerPower()
    def main_loop(self, l_game_objects, o_level_handler, o_player_engine, o_graphics_engine, objects):
        self.o_super_mushroom.main_loop(l_game_objects, o_level_handler, o_player_engine, o_graphics_engine, objects)
        self.o_flower_power.main_loop(l_game_objects,o_level_handler, o_player_engine, objects)