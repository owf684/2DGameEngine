import pygame


class _coin:

    def __init__(self):
        None

    def main_loop(self,objects,levelObjects, GameObjects, levelHandler, PlayerEngine):
        
        if objects.subClass == 'item' and 'coin' in objects.imagePath:
            self.track_scroll_coin(objects,PlayerEngine)
            if objects.item_released:
                objects.item_released = False
                objects.velocityY = 800
                objects.jumping = True

            print(objects.velocityY)

            if objects.jumping and objects.velocityY < 0:
                objects.destroy = True
                
            if objects.destroy and objects in levelObjects:
                objects.destroy = False
                levelObjects.remove(objects)
                levelHandler.clear_render_buffer = True
            elif objects.destroy and objects in GameObjects:
                objects.destroy = False
                GameObjects.remove(objects)
                levelHandler.clear_render_buffer = True

    def track_scroll_coin(self,objects,PlayerEngine):
        if PlayerEngine.scroll_level and objects.jumping: # jumping in this case means coin is flying in the air
            objects.position[0] -= PlayerEngine.x_displacement