import anim_util
import sys
sys.path.append("./GameObjects")
import BlockObject
import copy
class _breakable_break_anim(anim_util._anim_util):

    def __init__(self):
        super().__init__()
        self.help = True
        self.brick_pieces = self.extract_frames("./Assets/Platforms/breakable_brick_sprite_sheet/breakable_brick_pieces.png", 4, 16, 16)
        self.frame_size = (16, 16)
        self.frame_count = 4
        self.frame_duration = 100
        
    def main_loop(self, objects, GameObjects, levelObjects, PlayerEngine, GraphicsEngine):
        self.determine_frame_count()

        self.break_brick(objects, GameObjects, levelObjects, PlayerEngine, GraphicsEngine)

    def break_brick(self, objects, GameObjects, levelObjects, PlayerEngine, GraphicsEngine):
        print("breakable_brick_anim.py::break_brick(): len(levelObjects) = ", len(levelObjects))

        if "break" in objects.imagePath:
            if objects.hit and PlayerEngine.superMario:
                if not objects.timer_started:
                    objects.reset_time_variables()
                    objects.timer_started = True
                    objects.last_frame_time_2 = objects.determine_time_elapsed()
                    objects.image = self.brick_pieces[self.frame_index]
                    objects.velocityY = 500
                    objects.velocityX = -30
                    objects.fromUnder = True
                    self.set_object(objects)
                    self.create_piece(objects, levelObjects, copy.deepcopy(objects.position[0]) + 16, copy.deepcopy(objects.position[1])     , 30 )
                    self.create_piece(objects, levelObjects, copy.deepcopy(objects.position[0])     , copy.deepcopy(objects.position[1]) - 32, -35 )
                    self.create_piece(objects, levelObjects, copy.deepcopy(objects.position[0]) + 16, copy.deepcopy(objects.position[1]) - 32, 35 )
                    objects.isRendered =True

            if objects.timer_started:
                objects.image = self.brick_pieces[self.frame_index]
                if objects.determine_time_elapsed() > 5000:
                    objects.timer_started = False
                    objects.hit = False
                    levelObjects.remove(objects)
        

    def set_object(self, objects):
        try:

            objects._set_sprite_size(objects.image)
            objects._set_rect(objects.sprite_size)
            objects._set_mask()
        except Exception as Error:
            print("Error in breakable_brick_anim::Function set_object: ", Error)

    def create_piece(self, objects,levelObjects, x,y,vx):
        levelObjects.append(BlockObject._BlockObject())
        levelObjects[-1].imagePath = objects.imagePath
        levelObjects[-1].reset_time_variables()
        levelObjects[-1].timer_started = True
        levelObjects[-1].last_frame_time_2 = levelObjects[-1].determine_time_elapsed()        
        levelObjects[-1].image = self.brick_pieces[self.frame_index]
        self.set_object(levelObjects[-1])
        levelObjects[-1].velocityY = 500
        levelObjects[-1].position = [x,y]
        levelObjects[-1].isRendered = True
        levelObjects[-1].velocityX = vx
        levelObjects[-1].fromUnder = True
     
