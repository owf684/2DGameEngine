import math
import sys

sys.path.append('./GameObjects')
import block_object



class QuestionBlock:

    def __init__(self):
        self.question_block_trigger = False
        self.theta = 1
        self.step = .1
        self.question_block_object = None
        self.hit_state_path = './Assets/Platforms/question_block_states/question_block_hit_32x32.png'
        self.release_item_trigger = False

    def main_loop(self, l_game_objects, l_level_objects, o_player_engine, delta_t, objects):

        if isinstance(objects, block_object.BlockObject):

            self.handle_question_blocks(objects, o_player_engine)

            if objects.question_block_trigger:
                self.question_block_animation(objects)
                self.question_block_hit(objects)
            if objects.release_item_trigger:
                self.release_item(objects, l_game_objects, l_level_objects)
            if objects.pauseHit:
                if objects.determine_time_elapsed() > 300:
                    objects.pauseHit = False
    def handle_question_blocks(self, objects, o_player_engine):

        if objects.hit:
            if "Question" in objects.imagePath:
                objects.hit = False
                objects.question_block_trigger = True
                objects.release_item_trigger = True
                objects.reset_time_variables()
                objects.last_frame_time_2 = objects.determine_time_elapsed()     
    

    def question_block_hit(self, o_question_block):
        o_question_block.imagePath = self.hit_state_path
        o_question_block._set_image()
        o_question_block.image.convert_alpha()
        o_question_block.hit = True

    def question_block_animation(self, objects):

        objects.position[1] += 2 * math.cos(objects.theta * math.pi)
        objects.theta -= self.step

        if objects.theta <= 0:
            objects.question_block_trigger = False
            objects.changeHit = False
            objects.theta = 1

    def release_item(self, objects, l_game_objects, l_level_objects):

        if objects.item is not None:
            item = objects.item
            item.position[1] -= objects.rect.height
            item.rect.y = item.position[1]
            item.pause_physics = False
            item.x_direction = -1
            item._set_mask()
            item.item_released = True
            objects.item = None
            objects.release_item_trigger = False    
            l_game_objects.append(item)
