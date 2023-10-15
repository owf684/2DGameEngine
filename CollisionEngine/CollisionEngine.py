import copy
import sys
sys.path.append("./GameObjects")
import BlockObject
import FirePower

class _CollisionEngine:

    def __init__(self):
        self.collision_tolerance = 10

    def main_loop(self, objects, GraphicsEngine, levelHandler):

        # Reset collisions 
        objects.collisionDown = False
        objects.collisionLeft = False
        objects.collisionRight = False
        objects.collisionUp = False

        # iterate through render buffer and determine collision states of variable objects
        for objs in GraphicsEngine.render_buffer:
            try:
                self.updateRectPosition(objects)
                if objects != objs:
                    if ((   objects.subClass == 'player' or 
                            objects.subClass == 'enemy' or 
                            objects.subClass == 'powerup' or 
                            isinstance(objects, FirePower._FirePower) or
                            objects.subClass == 'item') and 
                            objs.subClass != 'environment'):
                        
                        self.detectCollisions(objects, objs, levelHandler)
    
            except Exception as Error:
                print("runtime error in CollisionEngine.py. Function main_loop: ", Error)

    def detectCollisions(self, objects, objs, levelHandler):
        try:
        
            if not objects.fromUnder:

                self.left_collision(objects,objs,levelHandler)
                self.right_collision(objects,objs, levelHandler)
                self.up_collision(objects, objs, levelHandler)   
                self.down_collision(objects, objs, levelHandler)
                
        except Exception as Error:
            print("runtime error in CollisionEngine.py Function detectCollisions: ", Error)

    def up_collision(self, objects, objs, levelHandler):
        try:
            if objects.rect.colliderect(objs.rect):
                if abs(objs.rect.bottom - objects.rect.top) < objs.rect.height and not objs.fromUnder:
                    if objs.rect.left-10 <= objects.rect.centerx <= objs.rect.right+10:
                    
                        if objects.subClass == 'player':
                            objects.collisionUp = self.player_collision_hanlder_y(objects,objs, 'up')
                    
                        if objects.subClass == 'enemy':
                            objects.collisionUp = self.enemy_collision_handler_y(objects,objs, levelHandler, 'up')                 

                        if objects.subClass == 'powerup' or isinstance(objects,FirePower._FirePower) or objects.subClass=='item':
                            objects.collisionUp = self.powerup_collision_handler_y(objects,objs,levelHandler, 'up')                       

                        self.save_collision_object(objects, objs)
                        #self.level_object_hit_box(objects,objs)     
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function up_collision: ", Error) 

    def down_collision(self, objects, objs, levelHandler):
        try:
            if objects.rect.colliderect(objs.rect) and objects.subClass != 'player':
                if abs(objs.rect.top - objects.rect.bottom) < objs.rect.height:

                    self.save_collision_object(objects,objs)  
                                
                    if objects.subClass == 'enemy':
                        objects.collisionDown = self.enemy_collision_handler_y(objects,objs, levelHandler, 'down')                 

                    if objects.subClass == 'powerup' or isinstance(objects, FirePower._FirePower) or objects.subClass == 'item':
                        objects.collisionDown = self.powerup_collision_handler_y(objects,objs,levelHandler, 'down')
                        
                    if 'coin' not in objs.imagePath:
                        objects.position[1] = objs.rect.top - objects.rect.height 
            
            elif objects.kill_box is not None and objects.kill_box.colliderect(objs.rect):
                    if abs(objs.rect.top - objects.rect.bottom) <= objs.rect.height:

                        self.save_collision_object(objects,objs) 

                        if objects.subClass == 'player':
                            objects.collisionDown = self.player_collision_hanlder_y(objects,objs, 'down')

                        if not objs.timer_started and not objects.timer_started and 'coin' not in objs.imagePath:
                                objects.position[1] = objs.rect.top - objects.rect.height  
                                            
        except Exception as Error:
            print('runtime error in CollisionEngine.py. Function down_collision: ', Error)
                                
    def left_collision(self,objects,objs, levelHandler):
        try:
            y_tolerance = 10
            if objs.subClass == 'enemy':
                x2_tolerance = 16
            else:
                x2_tolerance = 10          
            if abs(objects.rect.left-objs.rect.right) < x2_tolerance and (objects.x_direction == -1 or objs.x_direction == 1):
                if (objs.rect.topright[1] < objects.rect.top < objs.rect.bottomright[1] or 
                    objs.rect.topright[1] < objects.rect.centery < objs.rect.bottomright[1] or 
                    objs.rect.topright[1] < objects.rect.bottom - y_tolerance < objs.rect.bottomright[1]):               

                    self.save_collision_object(objects,objs)  
                
                    # handle collision for each entity and object
                    if objects.subClass == 'enemy':
                        objects.collisionLeft = self.enemy_collision_handler_x(objects,objs,levelHandler)
                    elif objects.subClass == 'player':
                        objects.collisionLeft = self.player_collision_hanlder_x(objects,objs,levelHandler)
                        if objects.collisionLeft:
                            objects.position[0] = objs.rect.right + 5  
                    elif objects.subClass == 'powerup' or isinstance(objects, FirePower._FirePower):
                        objects.collisionLeft = self.powerup_collision_handler_x(objects, objs, levelHandler) 
                                                    
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function left_collision: ", Error)
    
    def right_collision(self,objects,objs, levelHandler):
        try:
            y_tolerance = 10
            if objs.subClass == 'enemy':
                x2_tolerance = 16
            else:
                x2_tolerance = 10

            if abs(objs.rect.left-objects.rect.right) < x2_tolerance and (objects.x_direction == 1  or objs.x_direction == -1):
                if (objs.rect.topleft[1] < objects.rect.top < objs.rect.bottomleft[1]  or 
                        objs.rect.topleft[1] < objects.rect.centery < objs.rect.bottomleft[1] or 
                        objs.rect.topleft[1] < objects.rect.bottom - y_tolerance < objs.rect.bottomleft[1]):     
                        
                    self.save_collision_object(objects,objs)  

                    # Handle Collision for each entity/object 
                    
                    if objects.subClass == 'enemy':
                        objects.collisionRight = self.enemy_collision_handler_x(objects,objs,levelHandler)
                    elif objects.subClass == 'player':
                        objects.collisionRight = self.player_collision_hanlder_x(objects,objs,levelHandler)
                        if objects.collisionRight:
                            objects.position[0] = objs.rect.left - objects.rect.width - 5 
                    elif objects.subClass == 'powerup' or isinstance(objects, FirePower._FirePower):
                        objects.collisionRight = self.powerup_collision_handler_x(objects, objs, levelHandler)

        except Exception as Error:
            print("runtime error in CollisionEngine.py::function right_collision2(): ", Error)
 
    def updateRectPosition(self, collisionObject):
        try:
            collisionObject.rect.x = collisionObject.position[0]
            collisionObject.rect.y = collisionObject.position[1]
            if collisionObject.hit_box is not None:
                collisionObject.hit_box.x = collisionObject.position[0]
                collisionObject.hit_box.y = collisionObject.position[1] - 8
            if collisionObject.kill_box is not None:
                collisionObject.kill_box.x = collisionObject.position[0]+8
                collisionObject.kill_box.y = collisionObject.position[1] + collisionObject.image.get_height()-8
        
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function updateRectPosition: ", Error)

    def save_collision_object(self, objects, objs):
        try:
            objects.collisionSubClass = objs.subClass
            objects.collisionObjDirection = objs.x_direction
            objects.collisionObject = objs

        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function save_collision_object: ", Error)       

    def enemy_collision_handler_x(self, objects, objs, levelHandler):
        try:
            objects._set_mask()
            objs._set_mask()
    
            if objects.image_mask.overlap(objs.image_mask, (
                objs.position[0] - objects.position[0], objs.position[1] - objects.position[1])): 

                if objects.subClass == 'enemy':
                    if objs.subClass == 'player':
                        if objs.rect.top+5 < objects.rect.centery < objs.rect.bottom-5 and not objects.timer_started and not levelHandler.freeze_damage:
                            objs.isHit = True
                            self.save_collision_object(objects,objs)                        
                        return False              
                    elif objs.subClass == 'powerup':
                        return False
                    else:
                        return True               

        except Exception as Error:
            print("runtime error in CollisionEngine.py::Function enemy_collision_handler_x: ", Error)

    def player_collision_hanlder_x(self, objects, objs, levelHandler):
        try:
            objects._set_mask()
            objs._set_mask()
    
            if objects.subClass == 'player' and (objs.subClass == 'enemy' or objs.subClass == 'powerup'):
            
                if objects.image_mask.overlap(objs.image_mask, (
                    objs.position[0] - objects.position[0], objs.position[1] - objects.position[1])): 

                    if objs.subClass == 'enemy':
                        if objects.rect.top+5 < objs.rect.centery < objects.rect.bottom-5 and not levelHandler.freeze_damage and not objs.timer_started:
                            objects.isHit = True
                            self.save_collision_object(objects,objs)
                        return False
                     
                    elif objs.subClass == 'powerup':
                        objs.isHit = True
                        objects.powerUp = True
                        self.save_collision_object(objects,objs)
                        return False
                    
            elif objs.subClass == 'item' and 'coin' in objs.imagePath:
                objs.destroy = True
                self.save_collision_object(objects,objs)
                return False
            else:
                return True
        except Exception as Error:
            print("runtime error in CollisionEngine.py::player_collision_handler_x: ", Error)
    
    def powerup_collision_handler_x(self, objects, objs, levelHandler):
        try:     
            if not isinstance(objects,FirePower._FirePower) and objects.subClass == 'powerup':
                objects._set_mask()
                objs._set_mask()
    
                if objects.image_mask.overlap(objs.image_mask, (
                    objs.position[0] - objects.position[0], objs.position[1] - objects.position[1])):  

                        if objs.subClass == 'enemy':
                            return False
                        elif objs.subClass == 'player':
                            objects.isHit = True
                            objs.powerUp = True
                            self.save_collision_object(objects,objs)
                            return False
                        else:
                            return True
            elif isinstance(objects,FirePower._FirePower):

                if objs.subClass == 'enemy':
                    objs.isHit = True
                    objs.fromUnder = True
                    objects.isHit = True
                    return True
            
                elif isinstance(objs,BlockObject._BlockObject):
                    objs.hit = True
                    objects.isHit = True
                    return True                
                else:
                    return True
                    
        except Exception as Error:
            print("runtime error in CollisionEngine.py::powerup_collision_handler_x: ", Error)
    
   
    def enemy_collision_handler_y(self,objects,objs, levelHandler, Direction):
        try: 
            if objs.subClass == 'player' and not objects.timer_started  and not levelHandler.freeze_damage and Direction == 'down':
                objs.isHit = True
                return True
            else:
                return True
        except Exception as Error:
            print("ERROR::CollisionEngine.py::enemy_collision_handler_y() ", Error)

    def powerup_collision_handler_y(self,objects,objs, levelHandler, Direction):
        try:    
         
            if objects.rect.colliderect(objs.rect) and not isinstance(objects,FirePower._FirePower):
                if objects.subClass == 'powerup' and objs.subClass == 'player': # Direction does not matter here
                    objects.isHit = True
                    objs.powerUp = True
                    self.save_collision_object(objs,objects)       
                    return False
                else:
                    return True
            if isinstance(objects,FirePower._FirePower) and objs.subClass != 'player':
                
                if objs.subClass == 'enemy':
                    objs.isHit = True
                    objs.fromUnder = True
                    objects.isHit = True
            
                elif isinstance(objs,BlockObject._BlockObject):
                    objs.hit = True

                return True
            else:
                return True
            
          

        except Exception as Error:
            print("runtime error in CollisionEngine. Function payer_hit_box_y: ", Error)

    def player_collision_hanlder_y(self,objects,objs, Direction):
        try:

            if objs.subClass =='enemy' and not objs.timer_started and objects.subClass == 'player' and Direction == 'down':  
                if objs.hit_box.colliderect(objects.kill_box):      
                    objects.onEnemy = True
                    objs.isHit = True
                    return False
                
            elif objs.subClass == 'enemy' and objs.timer_started and objects.subClass == 'player':
                return False

            if isinstance(objs, BlockObject._BlockObject) and not objs.pauseHit and Direction == 'up' and objs.subClass != 'item':
                if 'break' in objs.imagePath or 'Question' in objs.imagePath:

                    if (objs.rect.left < objects.rect.centerx < objs.rect.right):
                        objs.hit = True  
                        objs.changeHit = True
                        objs.pauseHit = True    
                
                return True     
            
            if objects.subClass == 'player' and objs.subClass == 'powerup':
                    objs.isHit = True
                    objects.powerUp = True
                    self.save_collision_object(objects,objs) 
                    return False
            
            if objs.subClass == 'item' and 'coin' in objs.imagePath:
                objs.destroy = True
                self.save_collision_object(objects,objs)
                return False
            else:
                return True           

        except Exception as Error:
            print("ERROR::CollisionEngine.py::game_object_hit_box() ", Error)

    def level_object_hit_box(self,objects,objs):
        try:
            if isinstance(objs, BlockObject._BlockObject) and not objs.pauseHit:
                if (objs.rect.left < objects.rect.centerx < objs.rect.right):
                    objs.hit = True  
                    objs.changeHit = True
                    objs.pauseHit = True          
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function level_object_hit_box: ", Error)