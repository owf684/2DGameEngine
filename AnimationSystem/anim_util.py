import pygame
class _anim_util:

    def __init__(self):
        try:

            # variables used in main animation 
            self.elapsed_time = 0
            self.current_time = 0
            self.last_frame_time = 0
            self.frame_index = 0
            self.frame_duration = 0
            self.frame_count = 0
            self.damage_frame_index = 0
            self.damage_frame_index_captured = False
            self.damage_frame = None
            self.damage_count = 0    
            self.powerup_frame_index = 0
            self.powerup_frame_captured = False
            self.powerup_frame = None
            self.powerup_count = 0        
            self.transform_frame = None
            self.timer_started = False
            self.destroy_time = 0
            # variables used in damage handling
            self.current_time_2 = 0
            self.elapsed_time_2 = 0
            self.last_frame_time_2 = 0
        except Exception as Error:
            print("ERROR::anim_util.py::__init__()", Error)
            
    def determine_frame_count(self):
        try:
             
            self.current_time = pygame.time.get_ticks()
            self.elapsed_time = self.current_time - self.last_frame_time

            if self.elapsed_time >= self.frame_duration:
                self.frame_index = (self.frame_index + 1) % self.frame_count
                self.last_frame_time = self.current_time

        except Exception as Error:
            print("ERROR::anim_util.py::determine_frame_count", Error)
            
    def extract_frames(self, path, num_frames, frame_width, frame_height):
        try:
            frames = list()
            sprite_sheet = pygame.image.load(path).convert_alpha()
            for i in range(num_frames):
                frame = sprite_sheet.subsurface((0, i*frame_height, frame_width,frame_height))
                frames.append(frame)
            return frames
        except Exception as Error:
            print("ERROR::anim_util.py::extract_frames", Error)
            
    def determine_time_elapsed(self):
        try:

            self.current_time_2 = pygame.time.get_ticks()
            self.elapsed_time_2 = self.current_time_2 - self.last_frame_time_2
            return self.elapsed_time_2
        except Exception as Error:
            print("ERROR::anim_util.py::determine_time_elapsed", Error)

    def reset_time_variables(self):
        try:

            self.elapsed_time_2 = 0
            self.current_time_2 = 0
            self.last_frame_time_2 = 0
            self.frame_index = 0
        except Exception as Error:
            print("ERROR::anim_util.py::reset_time_variables", Error)