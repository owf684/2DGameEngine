import pygame



class MarioFX:

    def __init__(self):

        pygame.mixer.init()

        self.mario_jump = pygame.mixer.Sound("./Assets/AudioEffects/smb_jump-small.wav")
        self.mario_jump_playing = False

        self.super_mario_jump = pygame.mixer.Sound("./Assets/AudioEffects/smb_jump-super.wav")
        self.super_mario_jump_playing = False        

        self.powerup = pygame.mixer.Sound("./Assets/AudioEffects/smb_powerup.wav")

        self.fireball = pygame.mixer.Sound('./Assets/AudioEffects/smb_fireball.wav')
        self.fireball_playing = False

        self.mario_dies = pygame.mixer.Sound("./Assets/AudioEffects/smb_mario-dies.wav")

        self.mario_powerdown = pygame.mixer.Sound("./Assets/AudioEffects/smb_pipe.wav")
        self.number_of_powerdown_plays = 0
    def main_loop(self,objects,o_level_handler,o_player_engine):
        if objects.subClass == 'player':
            self.handle_jump_audio(objects,o_level_handler,o_player_engine)
            self.handle_flower_power_audio(objects,o_level_handler,o_player_engine)
            self.handle_powerup_audio(objects,o_level_handler,o_player_engine)
            self.handle_death_audio(objects,o_level_handler,o_player_engine)
            self.handle_power_down_audio(objects,o_level_handler,o_player_engine)
    def handle_jump_audio(self,objects,o_level_handler,o_player_engine):
        if o_player_engine.triggerPowerUpAudio:
            o_player_engine.triggerJumpFX = False
        if o_player_engine.triggerJumpFX and objects.power_up == 0 and not self.mario_jump_playing:
            # Play the sound with an event that triggers when the sound finishes playing

            self.mario_jump.play()
            self.mario_jump_playing = True

        elif o_player_engine.triggerJumpFX and objects.jumping and objects.power_up > 0 and not self.super_mario_jump_playing:

            self.super_mario_jump.play()
            self.super_mario_jump_playing = True

        if not o_player_engine.triggerJumpFX and self.mario_jump_playing:
            self.mario_jump.stop()
            self.mario_jump_playing = False

        if not o_player_engine.triggerJumpFX and self.super_mario_jump_playing:
            self.super_mario_jump.stop()
            self.super_mario_jump_playing = False

        if o_player_engine.triggerDeathAudio:
            self.super_mario_jump.stop()


    def handle_flower_power_audio(self,objects,o_level_handler,o_player_engine):
        if o_player_engine.triggerFlowerPowerAudio:
            o_player_engine.triggerFlowerPowerAudio = False
            
            self.fireball.play()
            
    def handle_powerup_audio(self,objects,o_level_handler,o_player_engine):
        if o_player_engine.triggerPowerUpAudio:
            o_player_engine.triggerPowerUpAudio = False
            self.powerup.play()
    def handle_death_audio(self,objects,levelHandler,PlayerEngine):
        if PlayerEngine.triggerDeathAudio:
            PlayerEngine.triggerDeathAudio = False
            self.mario_dies.play()
    def handle_power_down_audio(self,objects,o_level_handler,o_player_engine):

        if o_player_engine.triggerPowerDownAudio and o_level_handler.pause_for_damage:
            o_player_engine.triggerPowerDownAudio = False
            if self.number_of_powerdown_plays == 0:
                self.mario_powerdown.play()
            self.number_of_powerdown_plays += 1
            if self.number_of_powerdown_plays >= 2:
                self.number_of_powerdown_plays = 0
