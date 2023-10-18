import pygame
import MarioFX
import BlockFX
import EnemyFX

class _AudioEngine:

    def __init__(self):
        self.GroundTheme = pygame.mixer.Sound("./Assets/AudioEffects/Songs/GroundTheme.mp3")
        self.UnderWaterTheme = pygame.mixer.Sound("./Assets/AudioEffects/Songs/UnderWaterTheme.mp3")
        self.CastleTheme = pygame.mixer.Sound("./Assets/AudioEffects/Songs/CastleTheme.mp3")
        self.UndergroundTheme = pygame.mixer.Sound("./Assets/AudioEffects/Songs/UndergroundTheme.mp3")

        self.MarioFX = MarioFX._MarioFX()
        self.BlockFX = BlockFX._BlockFX()
        self.EnemyFX = EnemyFX._EnemyFX()
        self.over_world_music = self.GroundTheme

    def main_loop(self,objects,levelHandler,PlayerEngine, EnemyEngine):
        try:

            self.overWorldMusic()
            self.MarioFX.main_loop(objects,levelHandler,PlayerEngine)
            self.BlockFX.main_loop(objects,levelHandler,PlayerEngine)
            self.EnemyFX.main_loop(objects,levelHandler,EnemyEngine)
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
            print('hello????')
            if self.over_world_music.get_num_channels() > 0:

                self.over_world_music.stop()

        except Exception as Error:
            print("ERROR::AudioEngine.py::stop_over_world_music(): ", Error)