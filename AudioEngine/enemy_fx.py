import pygame


class EnemyFX:

    def __init__(self):
        self.bump = pygame.mixer.Sound("./Assets/AudioEffects/smb_stomp.wav") 
        

    def main_loop(self,objects,o_level_handler,o_enemy_engine):
        
        if o_enemy_engine.triggerStompAudio:
            self.bump.play()
            o_enemy_engine.triggerStompAudio = False