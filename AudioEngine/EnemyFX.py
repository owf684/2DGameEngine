import pygame


class _EnemyFX:

    def __init__(self):
        self.bump = pygame.mixer.Sound("./Assets/AudioEffects/smb_stomp.wav") 
        

    def main_loop(self,objects,levelHandler,EnemyEngine):
        
        if EnemyEngine.triggerStompAudio:
            print("hello corona!")
            self.bump.play()
            EnemyEngine.triggerStompAudio = False