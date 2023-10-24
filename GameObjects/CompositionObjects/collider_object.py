from dataclasses import dataclasses
import pygame
class ColliderObject:
    collisions      : list
    on_enemy        : bool
    is_hit          : bool
    hit             : bool
    hit_state       : int
    detected_object : None
    item_released   : bool
    from_under      : bool
    hit_box         : pygame.rect
    kill_box        : pygame.rect


    def set_collision(self,direction=0,collision=False, detected_object=None):
        self.collisions[direction] = collision
        self.detected_object = detected_object
    
    def set_hit_box(self,position,y_offset,sprite_size):
        self.hit_box = pygame.Rect(position[0],position[1] - y_offset,sprite_size[0],sprite_size[1]/2)

    def set_kill_box(self, position, y_offset, sprite_size):
        self.kill_box = pygame.Rect(position[0],position[1]+ y_offset,16,sprite_size[1]/4)
	
    def get_collision(self,direction):
        return self.collisions[direction]
    
    def clear_collisions(self):
        self.collisions = [ False for _ in self.collisions ]