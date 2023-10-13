import copy
import math
import sys

sys.path.append('./GameObjects')
sys.path.append('./AnimationSystem')
import anim_util
import BlockObject
import FirePower


class _PlayerEngine(anim_util._anim_util):

    def __init__(self):
        super().__init__()
        self.gravity = 9.8 * 150
        self.y_displacement = 0
        self.x_displacement = 0
        self.x_direction = 0
        self.x_decelleration = 0.1
        self.screen_width = 1280
        self.scroll_level = False
        self.x_acceleration = 0
        self.total_y_displacement = 0
        self.reached_max_height = False
        self.max_walk_velocity = 150
        self.max_run_velocity = 300
        self.superMario = False
        self.jump_latch = False
        self.runningFactor = 1
        self.supressDamage = False
        self.latch = False
        self.shoot_limit = 2
        self.shots_taken = 0
        self.delay_power = False
        self.shoot_delay_milliseconds = 1000

    def main_loop(self, objects, delta_t, input_dict, CollisionEngine, levelHandler,GameObjects):
        try:

            if objects.subClass == 'player':

                if not levelHandler.pause_for_damage and not levelHandler.trigger_death_animation and not levelHandler.trigger_powerup_animation:
                
                    self.horizontal_movement(objects, delta_t, input_dict, CollisionEngine, levelHandler)
                    self.jump(objects, delta_t, input_dict)
                    self.onEnemy(objects, input_dict, levelHandler)
                    self.handle_damage(objects, levelHandler)
                    self.handle_flower_power_action(objects,input_dict,levelHandler,GameObjects)

                    if self.delay_power:
                        self.delay_flower_power()
            
                self.handle_power_ups(objects, levelHandler)
            
                if levelHandler.pause_for_damage or levelHandler.trigger_death_animation or levelHandler.trigger_powerup_animation:
                    self.scroll_level = False

            if isinstance(objects,FirePower._FirePower):
                self.handle_flower_power_object(objects)   

        except Exception as Error:

            print("runtime error in PlayerEngine.py::Function main_loop(): ", Error)

    def delay_flower_power(self):
        try:

            if self.determine_time_elapsed() > self.shoot_delay_milliseconds:
                
                self.delay_power = False 
                self.shots_taken = 0

        except Exception as Error:

            print("runtime error in PlayerEngine.py::Function delay_flower_power(): ", Error)

    def handle_flower_power_object(self,objects):
        try:

            if objects.collisionDown:
            
                objects.velocityY = 150
        
            '''if (objects.collisionRight or objects.collisionLeft) and objects.collisionObject.subClass != 'player':
                
                #if objects.collisionObject.subClass == 'enemy':
                #    objects.collisionObject.fromUnder = True
            
                objects.isHit = True'''
            
        except Exception as Error:

            print("runtime error in PlayerEngine.py::handle_flower_power(): ", Error)

    def handle_power_ups(self, objects, levelHandler):
        try:

            if objects.powerUp:
            
                if "super_mushroom" in objects.collisionObject.imagePath and objects.power_up < 1:
                
                    levelHandler.trigger_powerup_animation = True
                    objects.power_up = 1
                    objects.collisionObject.isHit = True
            
                if "flower_power" in objects.collisionObject.imagePath and not objects.power_up == 2:
                
                    levelHandler.trigger_powerup_animation = True
                    objects.collisionObject.isHit = True
                    objects.power_up = 2

        except Exception as Error:

            print("runtime error in PlayerEngine.py::Function handle_power_ups(): ", Error)

    def handle_flower_power_action(self,objects,input_dict,levelHandler, GameObjects):
        try:
            if input_dict['attack'] == '1' and not self.latch and objects.power_up == 2 and not self.delay_power:
                self.shots_taken += 1
                
                if self.shots_taken >= self.shoot_limit:
                    self.delay_power = True
                    self.reset_time_variables()
                    self.last_frame_time_2 = self.determine_time_elapsed()

                self.latch =   True

                # Create FirePower Object
                firePowerObject = FirePower._FirePower()
                firePowerObject.velocityX = 300
                firePowerObject.velocityY = 50
                firePowerObject.position = copy.deepcopy(objects.position)
                firePowerObject.imagePath = './Assets/PlayerSprites/FlowerPowerMario/fire_ball.png'                
                firePowerObject._set_image()
                firePowerObject._set_sprite_size(firePowerObject.image)
                firePowerObject._set_rect(firePowerObject.sprite_size)
                firePowerObject.isRendered = True
                firePowerObject.jumping = True
                firePowerObject.x_direction = objects.x_direction
                firePowerObject.position[1] += 10
                
                # handle direction and position accordingly
                if firePowerObject.x_direction == 1:
                    firePowerObject.position[0] += 37
                else:
                    firePowerObject.position[0] -= 10
               
               # add to GameObjects to be processed in Render Buffer later
                GameObjects.append(firePowerObject)
            
            elif input_dict['attack'] == '0' and self.latch:
                
                self.latch = False

        except Exception as Error:
            
            print("runtime error in PlayerEngine.py::Function handle_power(): ", Error)

    def handle_damage(self, objects, levelHandler):
        try:

            if objects.isHit:
            
                if objects.power_up == 0:
                    levelHandler.trigger_death_animation = True
            
                if objects.power_up > 0:
                    objects.isHit = False
                    levelHandler.pause_for_damage = True
                    self.superMario = False

                elif objects.power_up == 0 and not levelHandler.freeze_damage and not levelHandler.trigger_death_animation:
                    levelHandler.load_level = True
                    levelHandler.edit_mode = True
        
            elif objects.position[1] > self.screen_width:
                levelHandler.load_level = True
                levelHandler.edit_mode = True
        
            if objects.power_up == 0 and not objects.powerUp:
                self.superMario = False

            if levelHandler.decrease_power:
                objects.power_up = 0
                levelHandler.decrease_power = False

        except Exception as Error:
            
            print("runtime error in PlayerEngine.py::Function handle_damage(): ", Error)
    
    def onEnemy(self, objects,input_dict, levelHandler):
        try:
        
            if objects.subClass == 'player':
            
                if objects.onEnemy:
                    objects.velocityY = 250
                    objects.velocityX = 125
                    objects.jumping = True            
                    objects.onEnemy = False

        except Exception as Error:

            print("runtime error in PlayerEngine.py::Function onEnemy(): ", Error)

    def jump(self, objects, delta_t, input_dict):
        try:

            if input_dict['up'] == '1' and not self.reached_max_height:
                objects.velocityY = 300
                objects.jumping = True

            self.total_y_displacement += objects.y_displacement
        
            if self.total_y_displacement >= 90:
                self.reached_max_height = True

            if objects.collisionUp:
                self.reached_max_height = True
            
                if objects.velocityY > 0:
                    objects.velocityY *= -0.5
            
                self.total_y_displacement = 0
                objects.jumping = False

            if objects.collisionDown and objects.velocityY < 0:
            
                self.total_y_displacement = 0
                objects.jumping = False
            
                if self.reached_max_height:
                
                    if input_dict['up'] == '0':
                        self.reached_max_height = False

        except Exception as Error:

            print("runtime Error in PlayerEngine.py::Function jump(): ", Error)

    def horizontal_movement(self, objects, delta_t, input_dict, CollisionEngine, levelHandler):
        try:

            self.set_scroll_state(objects, input_dict, levelHandler)

            if input_dict['right'] == '1':
                objects.x_direction = 1

                if objects.velocityX >= 100*self.runningFactor:
                    objects.velociyX = 100 * self.runningFactor
                else:
                    objects.velocityX += 10 * self.runningFactor

            elif input_dict['left'] == '-1':
                objects.x_direction = -1

                if objects.velocityX > 100*self.runningFactor:
                    objects.velocityX = 100 *self.runningFactor
                else:
                    objects.velocityX += 10 * self.runningFactor

            else:
                if objects.velocityX > 20:
                    objects.velocityX -= 300*delta_t
                elif objects.velocityX < -20:
                    objects.velocityX += 300*delta_t
                else:
                    objects.velocityX = 0
            if input_dict['l-shift'] == '1':
                self.runningFactor = 1.5
            else:
                self.runningFactor = 1

            self.x_displacement = objects.x_displacement
            self.x_direction = objects.x_direction

        except Exception as Error:
            
            print("runtime Error in PlayerEngine.py::Function horizontal_movement(): ", Error)
    
    def set_scroll_state(self, objects, input_dict, levelHandler):
        try:

            # handle level scrolling left
            if objects.position[0] >= self.screen_width / 2 and self.x_direction > 0 and (input_dict['right'] == '1' or objects.onEnemy):
                self.scroll_level = True
                objects.scrolling = True
            # handle level scrolling right
            elif objects.position[0] < self.screen_width / 2 and self.x_direction < 0 and (input_dict[
                'left'] == '-1' or objects.onEnemy) and levelHandler.scroll_offset > 0:
                self.scroll_level = True
                objects.scrolling = True
            else:
                self.scroll_level = False
                objects.scrolling = False

        except Exception as Error:
            
            print("runtime error in PlayerEngine.py::Function set_scroll_state(): ", Error)