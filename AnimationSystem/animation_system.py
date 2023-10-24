import question_block_anim
import mario_anim
import goomba_anim
import breakable_brick_anim
import firepower_anim
import coin_anim
import koopa_anim
class AnimationSystem:

    def __init__(self):
        try:
            self.question_block_anim = question_block_anim.QuestionBlockAnim()
            self.mario_anim = mario_anim.MarioAnim()
            self.goomba_anim = goomba_anim.GoombaAnim()
            self.breakable_brick_anim = breakable_brick_anim.BreakableBrickAnim()
            self.firepower_anim = firepower_anim.FirepowerAnim()
            self.coin_anim = coin_anim.CoinAnim()
            self.koopa_anim = koopa_anim.KoopaAnim()
            self.reset_animations = False
        except Exception as Error:
            print("ERROR::AnimationSystem.py::__init__()", Error)
    def main_loop(self, objects, l_game_objects, l_level_objects, d_inputs, o_level_handler, delta_t, o_player_engine, o_graphics_engine, o_enemy_engine):
        try:

            self.question_block_anim.main_loop(o_level_handler)
            self.mario_anim.main_loop(self, objects, d_inputs, o_level_handler, delta_t,o_player_engine)
            self.goomba_anim.main_loop(objects, o_enemy_engine)
            self.koopa_anim.main_loop(objects,o_enemy_engine)
            self.breakable_brick_anim.main_loop(objects,l_game_objects, l_level_objects, o_player_engine, o_graphics_engine)
            self.firepower_anim.main_loop(objects,o_level_handler,delta_t,o_player_engine)
            self.coin_anim.main_loop(objects)
        except Exception as Error:
            print("ERROR::AnimationSystem.py::main_loop()", Error)