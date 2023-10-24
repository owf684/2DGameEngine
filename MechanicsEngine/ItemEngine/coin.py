import pygame


class Coin:

    def __init__(self):
        None

    def main_loop(self,objects,l_level_objects, l_game_objects, o_level_handler, o_player_engine):        
        if objects.subClass == 'item' and 'coin' in objects.imagePath:
            self.track_scroll_coin(objects,o_player_engine)
            if objects.item_released:
                objects.item_released = False
                objects.velocityY = 800
                objects.jumping = True

            if objects.jumping and objects.velocityY < 0:
                objects.destroy = True
                
            if objects.destroy and objects in l_level_objects:
                objects.destroy = False
                l_level_objects.remove(objects)
                o_level_handler.clear_render_buffer = True
            elif objects.destroy and objects in l_game_objects:
                objects.destroy = False
                l_game_objects.remove(objects)
                o_level_handler.clear_render_buffer = True

    def track_scroll_coin(self,objects,o_player_engine):
        if o_player_engine.scroll_level and objects.jumping: # jumping in this case means coin is flying in the air
            objects.position[0] -= o_player_engine.x_displacement