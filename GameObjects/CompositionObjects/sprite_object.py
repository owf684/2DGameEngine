from dataclasses import dataclass
import pygame

@dataclass
class SpriteObject:

    image_path : str
    sprite_sheet : bool
    frame_count : int
    sprite_size : list
    image : pygame.surface
    rect : pygame.rect
    rendered : bool
    animation_state : int
    image_mask : pygame.mask
    trigger_next_animation : bool

    '''Setters '''
    def set_image_path(self, image_path):
        try:
            self.set_image_path = image_path
        except Exception as Error:
            print("ERROR:sprite_object.py::set_image(): ", Error)

    def set_frame_count(self,frame_count):
        try:
            self.frame_count = frame_count
        except Exception as Error:
            print("ERROR::sprite_object.py::set_frame_count(): ", Error)
        
    def set_sprite_size(self,sprite_size):
        try:
            self.sprite_size = sprite_size
        except Exception as Error:
            print("ERROR::sprite_object.py::set_image(): ", Error)

    def set_image(self):
        try:
            self.image = pygame.image.load(self.image_path)
        except Exception as Error:
            print("ERROR:sprite_object.py::set_image():", Error)

    def set_rect(self):
        try:

            self.rect = pygame.Rect(self.position[0],self.position[1],self.sprite_size[0],self.sprite_size[1])  
        except Exception as Error:
            print("ERROR:sprite_object.py::set_rect(): ", Error)

    def create_sprite(self,image_path, sprite_sheet,sprite_size=[0,0],frame_count=0):
        self.set_image_path(image_path)
        self.sprite_sheet = sprite_sheet
        self.sprite_size = sprite_size
        self.frame_count = frame_count
        if not self.sprite_sheet:
            self.set_image()
            self.set_rect()

            

    '''Getters'''
    def get_image_path(self):
        return self.image_path
    
    def get_frame_count(self):
        return self.frame_count
  
    def get_sprite_size(self):
        return self.sprite_size
  
    def get_image(self):
        return self.image
    
    

