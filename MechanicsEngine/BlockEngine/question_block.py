import math
import sys

sys.path.append('./GameObjects')
import BlockObject



class _question_block:

    def __init__(self):
        self.question_block_trigger = False
        self.theta = 1
        self.step = .1
        self.question_block_object = None
        self.hit_state_path = './Assets/Platforms/question_block_states/question_block_hit_32x32.png'
        self.release_item_trigger = False

    def main_loop(self, GameObjects, levelObjects, PlayerEngine, delta_t, objects):

        if isinstance(objects, BlockObject._BlockObject):

            self.handle_question_blocks(objects, PlayerEngine)

            if objects.question_block_trigger:
                self.question_block_animation(objects)
                self.question_block_hit(objects)
            if objects.release_item_trigger:
                self.release_item(objects, GameObjects)
            if objects.pauseHit:
                if objects.determine_time_elapsed() > 300:
                    objects.pauseHit = False
    def handle_question_blocks(self, objects, PlayerEngine):

        # if objects.collisionObject is not None and objects.collisionObject.collisionSubClass == 'player':
        # print("hello!")
        if objects.hit:
            if "Question" in objects.imagePath:
                objects.hit = False
                objects.question_block_trigger = True
                objects.release_item_trigger = True
                objects.reset_time_variables()
                objects.last_frame_time_2 = objects.determine_time_elapsed()     

    def question_block_hit(self, questionBlock):
        questionBlock.imagePath = self.hit_state_path
        questionBlock._set_image()
        questionBlock.image.convert_alpha()
        questionBlock.hit = True

    def question_block_animation(self, objects):

        objects.position[1] += 2 * math.cos(objects.theta * math.pi)
        objects.theta -= self.step

        if objects.theta <= 0:
            objects.question_block_trigger = False
            objects.changeHit = False
            objects.theta = 1

    def release_item(self, objects, GameObjects):

        if objects.item is not None:
            item = objects.item
            item.position[1] -= objects.rect.height
            item.rect.y = item.position[1]
            item.pause_physics = False
            item.x_direction = -1
            item._set_mask()
            objects.item = None
            objects.release_item_trigger = False    
            GameObjects.append(item)
