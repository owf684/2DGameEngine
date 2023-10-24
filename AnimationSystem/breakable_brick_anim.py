import anim_util
import sys
sys.path.append("./GameObjects")
import block_object
import copy
class BreakableBrickAnim(anim_util.AnimUtil):

    def __init__(self):
        try:

            super().__init__()
            self.help = True
            self.brick_pieces = self.extract_frames("./Assets/Platforms/breakable_brick_sprite_sheet/breakable_brick_pieces.png", 4, 16, 16)
            self.frame_size = (16, 16)
            self.frame_count = 4
            self.frame_duration = 100
        except Exception as Error:
            print("ERROR::breakable_brick_anim.py::__init__()", Error)

    def main_loop(self, objects, l_game_objects, l_level_objects, o_player_engine, o_graphics_engine):
        try:
            self.determine_frame_count()

            self.break_brick(objects, l_game_objects, l_level_objects, o_player_engine, o_graphics_engine)
        except Exception as Error:
            print("ERROR::breakable_brick_anim.py::main_loop()", Error)

    def break_brick(self, objects, l_game_objects, l_level_objects, o_player_engine, o_graphics_engine):
        try:
            if "break" in objects.imagePath:
                if objects.hit and o_player_engine.superMario:
                    if not objects.timer_started:
                        o_player_engine.triggerBlockBreakAudio = True
                        objects.hit = False
                        objects.reset_time_variables()
                        objects.timer_started = True
                        objects.last_frame_time_2 = objects.determine_time_elapsed()
                        objects.image = self.brick_pieces[self.frame_index]
                        objects.velocityY = 500
                        objects.velocityX = -30
                        objects.fromUnder = True
                        self.set_object(objects)
                        self.create_piece(objects, l_level_objects, copy.deepcopy(objects.position[0]) + 16, copy.deepcopy(objects.position[1])     , 30 )
                        self.create_piece(objects, l_level_objects, copy.deepcopy(objects.position[0])     , copy.deepcopy(objects.position[1]) - 32, -35 )
                        self.create_piece(objects, l_level_objects, copy.deepcopy(objects.position[0]) + 16, copy.deepcopy(objects.position[1]) - 32, 35 )
                        objects.isRendered =True

                if objects.timer_started:
                    objects.image = self.brick_pieces[self.frame_index]
                    if objects.determine_time_elapsed() > 5000:
                        objects.timer_started = False
                        if objects in l_level_objects:
                            l_level_objects.remove(objects)
        except Exception as Error:
             print("ERROR::breakable_brick_anim.py::break_brick()", Error)        

    def set_object(self, objects):
        try:

            objects._set_sprite_size(objects.image)
            objects._set_rect(objects.sprite_size)
            objects._set_mask()
        except Exception as Error:
            print("Error in breakable_brick_anim::Function set_object: ", Error)

    def create_piece(self, objects,l_level_objects, x,y,vx):
        try:
            l_level_objects.append(block_object.BlockObject())
            l_level_objects[-1].imagePath = objects.imagePath
            l_level_objects[-1].reset_time_variables()
            l_level_objects[-1].timer_started = True
            l_level_objects[-1].last_frame_time_2 = l_level_objects[-1].determine_time_elapsed()        
            l_level_objects[-1].image = self.brick_pieces[self.frame_index]
            self.set_object(l_level_objects[-1])
            l_level_objects[-1].velocityY = 500
            l_level_objects[-1].position = [x,y]
            l_level_objects[-1].isRendered = True
            l_level_objects[-1].velocityX = vx
            l_level_objects[-1].fromUnder = True
        except Exception as Error:
            print("ERROR::breakable_brick_anim.py::create_piece()", Error)     
