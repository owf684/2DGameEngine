import pygame



class BlockFX:

    def __init__(self):
        pygame.mixer.init()

        self.bump = pygame.mixer.Sound('./Assets/AudioEffects/smb_bump.wav')
        self.bump_playing = False

        self.coin = pygame.mixer.Sound('./Assets/AudioEffects/smb_coin.wav')
        self.coin_playing = False

        self.powerup = pygame.mixer.Sound("./Assets/AudioEffects/smb_powerup_appears.wav")
        self.powerup_playing = False

        self.break_block = pygame.mixer.Sound("./Assets/AudioEffects/smb_breakblock.wav")
        self.break_block_playing = False

        self.number_of_bump_plays = 0
        self.trigger_block_audio = False
        self.trigger_break_block_audio = False
    def main_loop(self,objects,o_level_handler,o_player_engine):

        if 'Question' in objects.imagePath:
            self.trigger_block_audio = True
        elif 'break' in objects.imagePath and not o_player_engine.superMario:
            self.trigger_block_audio = True
        elif 'break' in objects.imagePath and o_player_engine.superMario:
            self.trigger_break_block_audio = True
        elif 'question_block_hit' in objects.imagePath:
          self.handle_question_block_hit_audio(objects)

        if self.trigger_block_audio:
            self.trigger_block_audio = False
            self.handle_block_audio(objects)

        if self.trigger_break_block_audio:
            self.trigger_break_block_audio = False
            self.handle_break_block_audio(o_player_engine)

    def handle_block_audio(self, objects):
        
        if objects.hit and not self.bump_playing:
            self.bump.play()
            self.bump_playing = True

            if objects.item is not None:
                if 'coin' in objects.item.imagePath and not self.coin_playing:
                    self.coin.play()
                    self.coin_playing = True

                elif objects.item.subClass == 'powerup' and not self.powerup_playing:
                    self.powerup.play()
                    self.powerup_playing = True

        if self.bump.get_num_channels() == 0 and self.bump_playing:
            self.bump.stop()
            self.bump_playing = False

        if self.coin.get_num_channels() == 0 and self.coin_playing:
            self.coin.stop()
            self.coin_playing = False

        if self.powerup.get_num_channels() == 0 and self.powerup_playing:
            self.powerup.stop()
            self.powerup_playing = False


    def handle_break_block_audio(self,o_player_engine):
        if o_player_engine.triggerBlockBreakAudio:
            o_player_engine.triggerBlockBreakAudio = False
            self.break_block.play()

    def handle_question_block_hit_audio(self,objects):
        if objects.isHit:
            #only play audio clip once when not already playing
            if self.number_of_bump_plays == 0 and self.bump.get_num_channels() == 0:

                self.bump.play()

            objects.isHit = False

            #prevents from audio clip from playing twice when it should only play it once
            self.number_of_bump_plays += 1   
            if self.number_of_bump_plays >= 2:
                self.number_of_bump_plays = 0
