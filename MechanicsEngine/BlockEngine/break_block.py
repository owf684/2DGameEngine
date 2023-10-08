import sys
sys.path.append("./AnimationSystem")
sys.path.append('./GameObjects')
import BlockObject
import math


class _break_block():

    def __init__(self):
        self.step = 0.1


    def main_loop(self, GameObjects, levelObjects, PlayerEngine, delta_t, objects):
        try:

            if isinstance(objects, BlockObject._BlockObject):
                self.handle_break_blocks(objects, PlayerEngine)

                if objects.push_block_trigger:
                    self.push_block_animation(objects)

                if objects.release_item_trigger:
                    self.release_item(objects, GameObjects)

                if objects.pauseHit:
                    if objects.determine_time_elapsed() > 300:
                        objects.pauseHit = False
        except Exception as Error:
            print("runtime error in break_block.py::Function main_loop: ", Error)
    def handle_break_blocks(self, objects, PlayerEngine):
        try:

            if objects.hit:
                if "break" in objects.imagePath and not PlayerEngine.superMario:
                    objects.hit = False
                    objects.push_block_trigger = True
                    objects.release_item_trigger = True
        except Exception as Error:
            print("runetime error in break_block.py::Function handle_break_blocks(): ", Error)            

    def push_block_animation(self, objects):
        try:

            objects.position[1] += 2 * math.cos(objects.theta * math.pi)
            objects.theta -= self.step

            if objects.theta <= 0:
                objects.push_block_trigger = False
                objects.changeHit = False
                objects.theta = 1
        except Exception as Error:
            print("runtimer error in break_block.py::Function push_block_animation: ", Error)

    def release_item(self, push_block_object, GameObjects):
        try:

            if push_block_object.item is not None:
                item = push_block_object.item
                item.position[1] -= push_block_object.rect.height / 2
                item.rect.y = item.position[1]
                item.pause_physics = False
                item.x_direction = -1
                push_block_object.item = None
                item._set_mask()
                self.release_item_trigger = False     
                GameObjects.append(item)
        except Exception as Error:
            print("runtime error in break_block.py::Function release_item(): ", Error)