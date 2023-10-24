import pygame



class ItemContainer:

    def __init__(self):
        self.selected_image_path = None
        self.inactive_image_path = None
        self.item_selected_image = None
        self.item_inactive_image = None
        self.isActive = False
        self.active_image = None
        self.position = [0,0]
        self.item_position = [0,0]
        self.item_image = None
        self.item_image_path = None
        self.rect = None


    def set_active_image(self,active_image_path):
        self.selected_image_path = active_image_path
        self.item_selected_image = pygame.image.load(self.selected_image_path)
    
    def set_inactive_image(self, inactive_image_path):
        self.inactive_image_path = inactive_image_path
        self.item_inactive_image = pygame.image.load(self.inactive_image_path)
    
    def set_rect(self):
	    self.rect = pygame.Rect(self.position[0],self.position[1],self.item_selected_image.get_width(),self.item_selected_image.get_height())        
