import question_block_anim
import mario_anim
import goomba_anim
import breakable_brick_anim
import firepower_anim
import coin_anim
class _AnimationSystem:

    def __init__(self):
        self.question_block = question_block_anim._question_block()
        self.mario_anim = mario_anim._mario_anim()
        self.goomba_anim = goomba_anim._goomba_anim()
        self.breakable_brick_anim = breakable_brick_anim._breakable_break_anim()
        self.firepower_anim = firepower_anim._firepower_anim()
        self.coin_anim = coin_anim._coin_anim()
        self.reset_animations = False
    def main_loop(self, objects, GameObjects, levelObjects, input_dict, levelHandler, delta_t, PlayerEngine, GraphicsEngine):

        self.question_block.main_loop(levelHandler)
        self.mario_anim.main_loop(self, objects, input_dict, levelHandler, delta_t,PlayerEngine)
        self.goomba_anim.main_loop(objects)
        self.breakable_brick_anim.main_loop(objects,GameObjects, levelObjects, PlayerEngine, GraphicsEngine)
        self.firepower_anim.main_loop(objects,levelHandler,delta_t,PlayerEngine)
        self.coin_anim.main_loop(objects)
