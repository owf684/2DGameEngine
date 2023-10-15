import pygame


class _coin:

    def __init__(self):
        None

    def main_loop(self,objects,levelObjects,levelHandler):
        
        if objects.subClass == 'item' and 'coin' in objects.imagePath:
            if objects.destroy and objects in levelObjects:
                objects.destroy = False
                levelObjects.remove(objects)
                levelHandler.clear_render_buffer = True