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
    def main_loop(self, objects, delta_t, input_dict, CollisionEngine, levelHandler,GameObjects):
        if objects.subClass == 'player':
            if not levelHandler.pause_for_damage and not levelHandler.trigger_death_animation:
                self.horizontal_movement(objects, delta_t, input_dict, CollisionEngine, levelHandler)
                self.jump(objects, delta_t, input_dict)
                self.onEnemy(objects, input_dict, levelHandler)
                self.handle_damage(objects, levelHandler)
                self.handle_power(objects,input_dict,levelHandler,GameObjects)

            self.handle_power_ups(objects, levelHandler)
            
            if levelHandler.pause_for_damage or levelHandler.trigger_death_animation:
                self.scroll_level = False

        if isinstance(objects,FirePower._FirePower):
            self.handle_firePower(objects)    
    def handle_firePower(self,objects):
        if objects.collisionDown:
            objects.velocityY = 150
        if objects.collisionRight or objects.collisionLeft:
            if objects.collisionObject.subClass == 'enemy':
                objects.collisionObject.fromUnder = True
            objects.isHit = True
    def handle_power_ups(self, objects, levelHandler):

        if objects.powerUp:
            if "super_mushroom" in objects.collisionObject.imagePath and objects.power_up < 1:
                levelHandler.trigger_powerup_animation = True
                objects.power_up = 1
                objects.collisionObject.isHit = True
            if "flower_power" in objects.collisionObject.imagePath and not objects.power_up == 2:
                levelHandler.trigger_powerup_animation = True
                objects.collisionObject.isHit = True
                objects.power_up = 2
    def handle_power(self,objects,input_dict,levelHandler, GameObjects):
            if input_dict['attack'] == '1' and not self.latch and objects.power_up == 2:

                self.latch = True
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
                if firePowerObject.x_direction == 1:
                    firePowerObject.position[0] += 37
                else:
                    firePowerObject.position[0] -= 10
                GameObjects.append(firePowerObject)
            elif input_dict['attack'] == '0' and self.latch:
                self.latch = False
  

    def handle_damage(self, objects, levelHandler):
        if objects.isHit:
            if objects.power_up == 0:
                levelHandler.trigger_death_animation = True
                print("PlayerEngine.py::levelHandler.trigger_death_animation=", levelHandler.trigger_death_animation)
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

    def onEnemy(self, objects,input_dict, levelHandler):
        if objects.subClass == 'player':
            if objects.onEnemy:
                objects.velocityY = 250
                objects.velocityX = 125
                objects.jumping = True            
                objects.onEnemy = False
   
    def jump(self, objects, delta_t, input_dict):
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

    def horizontal_movement(self, objects, delta_t, input_dict, CollisionEngine, levelHandler):

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

    def set_scroll_state(self, objects, input_dict, levelHandler):

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
