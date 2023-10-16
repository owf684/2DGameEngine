import pygame



class _MarioFX:

    def __init__(self):

        pygame.mixer.init()

        self.mario_jump = pygame.mixer.Sound("./Assets/AudioEffects/smb_jump-small.wav")
        self.mario_jump_playing = False

        self.super_mario_jump = pygame.mixer.Sound("./Assets/AudioEffects/smb_jump-super.wav")
        self.super_mario_jump_playing = False        

        self.powerup = pygame.mixer.Sound("./Assets/AudioEffects/smb_powerup.wav")

        self.stomp = pygame.mixer.Sound("./Assets/AudioEffects/smb_stomp.wav")
        self.stomp_playing = False

        self.fireball = pygame.mixer.Sound('./Assets/AudioEffects/smb_fireball.wav')
        self.fireball_playing = False

    def main_loop(self,objects,levelHandler,PlayerEngine):
        if objects.subClass == 'player':
            self.handle_jump_audio(objects,levelHandler,PlayerEngine)
            self.handle_stomp_audio(objects,levelHandler,PlayerEngine)
            self.handle_flower_power_audio(objects,levelHandler,PlayerEngine)
            self.handle_powerup_audio(objects,levelHandler,PlayerEngine)

    def handle_jump_audio(self,objects,levelHandler,PlayerEngine):

        if PlayerEngine.triggerJumpFX and objects.power_up == 0 and not self.mario_jump_playing:
            # Play the sound with an event that triggers when the sound finishes playing

            self.mario_jump.play()
            self.mario_jump_playing = True

        elif PlayerEngine.triggerJumpFX and objects.jumping and objects.power_up > 0 and not self.super_mario_jump_playing:

            self.super_mario_jump.play()
            self.super_mario_jump_playing = True

        if not PlayerEngine.triggerJumpFX and self.mario_jump_playing:
            self.mario_jump.stop()
            self.mario_jump_playing = False

        if not PlayerEngine.triggerJumpFX and self.super_mario_jump_playing:
            self.super_mario_jump.stop()
            self.super_mario_jump_playing = False


    def handle_stomp_audio(self,objects,levelHandler,PlayerEngine):

        if objects.onEnemy and not self.stomp_playing:
            self.stomp.play()
            self.stomp_playing = True

        if self.stomp.get_num_channels() == 0 and self.stomp_playing:
            self.stomp_playing = False

    def handle_flower_power_audio(self,objects,levelHandler,PlayerEngine):
        if PlayerEngine.triggerFlowerPowerAudio:
            PlayerEngine.triggerFlowerPowerAudio = False
            
            self.fireball.play()
            
    def handle_powerup_audio(self,objects,levelHandler,PlayerEngine):
        if PlayerEngine.triggerPowerUpAudio:
            PlayerEngine.triggerPowerUpAudio = False
            self.powerup.play()

