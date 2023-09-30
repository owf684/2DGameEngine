import question_block_anim
import mario_anim
import goomba_anim


class _AnimationSystem:

    def __init__(self):
        self.question_block = question_block_anim._question_block()
        self.mario_anim = mario_anim._mario_anim()
        self.goomba_anim = goomba_anim._goomba_anim()

    def main_loop(self, GameObjects, input_dict,levelHandler):
        self.question_block.main_loop(levelHandler)
        for objects in GameObjects:

            self.mario_anim.main_loop(objects,input_dict)
            self.goomba_anim.main_loop(objects)

