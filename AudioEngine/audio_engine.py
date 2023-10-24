import pygame
import mario_fx
import block_fx
import enemy_fx

class AudioEngine:

    def __init__(self):
        self.ground_theme = pygame.mixer.Sound("./Assets/AudioEffects/Songs/GroundTheme.mp3")
        self.under_water_theme = pygame.mixer.Sound("./Assets/AudioEffects/Songs/UnderWaterTheme.mp3")
        self.castle_theme = pygame.mixer.Sound("./Assets/AudioEffects/Songs/CastleTheme.mp3")
        self.underground_theme = pygame.mixer.Sound("./Assets/AudioEffects/Songs/UndergroundTheme.mp3")

        self.o_mario_fx = mario_fx.MarioFX()
        self.o_block_fx = block_fx.BlockFX()
        self.o_enemy_fx = enemy_fx.EnemyFX()
        self.over_world_music = self.ground_theme

    def main_loop(self,objects,o_level_handler,o_player_engine, o_enemy_engine):
        try:
            if not o_level_handler.trigger_death_animation and self.o_mario_fx.mario_dies.get_num_channels() == 0:

                self.overWorldMusic()
            else:
                self.stop_over_world_music()

            self.o_mario_fx.main_loop(objects,o_level_handler,o_player_engine)
            self.o_block_fx.main_loop(objects,o_level_handler,o_player_engine)
            self.o_enemy_fx.main_loop(objects,o_level_handler,o_enemy_engine)
        except Exception as Error:
            print("ERROR::AudioEngine.py::main_loop(): ", Error)

    def overWorldMusic(self):
        try:

            if self.over_world_music.get_num_channels() == 0:
                self.over_world_music.play(-1)
        except Exception as Error:
            print("ERROR:AudioEngine.py::overWorldMusic(): ", Error)
    def set_over_world_music(self,Sound):
        try:

            #stop current music if playing
            if self.over_world_music.get_num_channels() > 0:
                self.over_world_music.stop()
            #update over world music to new sound
            self.over_world_music = Sound
        except Exception as Error:
            print("ERROR::AudioEngine.py::set_over_world_music: ", Error)
    def stop_over_world_music(self):
        try:
            if self.over_world_music.get_num_channels() > 0:

                self.over_world_music.stop()

        except Exception as Error:
            print("ERROR::AudioEngine.py::stop_over_world_music(): ", Error)