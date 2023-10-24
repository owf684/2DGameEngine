import anim_util




class CoinAnim(anim_util.AnimUtil):


    def __init__(self):
        try:

            super().__init__()
            self.frame_count = 4
            self.frame_duration = 150
        
            self.coin_sprite_animation = self.extract_frames( './Assets/Items/coin_states/coin_sprite_sheet.png',4,32,32)

            self.spinning_coin_sprite_animation = self.extract_frames('./Assets/Items/coin_states/spinning_coin_sprite_sheet.png', 4,32,32)
        except Exception as Error:
            print("ERROR:coin_anim.py::__init__()", Error)

    def main_loop(self,objects):
        try:
             
            self.determine_frame_count()
            if objects.subClass == 'item' and "coin.png" in objects.imagePath and not objects.jumping:
                objects.image = self.coin_sprite_animation[self.frame_index]
            elif objects.subClass == 'item' and "coin.png" in objects.imagePath and objects.jumping:
                objects.image = self.spinning_coin_sprite_animation[self.frame_index]
        except Exception as Error:
            print("ERROR::coin_anim.py::main_loop()", Error)