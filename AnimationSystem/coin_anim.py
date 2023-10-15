import anim_util




class _coin_anim(anim_util._anim_util):


    def __init__(self):

        super().__init__()
        self.frame_count = 4
        self.frame_duration = 150

        self.coin_sprite_animation = self.extract_frames( './Assets/Items/coin_states/coin_sprite_sheet.png',4,32,32)

        self.spinning_coin_sprite_animation = self.extract_frames('./Assets/Items/coin_states/spinning_coin_sprite_sheet.png', 4,32,32)

    def main_loop(self,objects):
        self.determine_frame_count()
        if objects.subClass == 'item' and "coin.png" in objects.imagePath and not objects.jumping:
            objects.image = self.coin_sprite_animation[self.frame_index]
        elif objects.subClass == 'item' and "coin.png" in objects.imagePath and objects.jumping:
            objects.image = self.spinning_coin_sprite_animation[self.frame_index]
