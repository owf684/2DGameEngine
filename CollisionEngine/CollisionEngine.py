import copy
import sys
sys.path.append("./GameObjects")
import BlockObject

class _CollisionEngine:

    def __init__(self):
        self.collision_tolerance = 10

    def main_loop(self, objects, GraphicsEngine, input_dict):

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
                            objects.subClass == 'powerup') and 
                            objs.subClass != 'environment'):
                        
                        self.detectCollisions(objects, objs)
            except Exception as Error:
                print("runtime error in CollisionEngine.py. Function main_loop: ", Error)

    def detectCollisions(self, objects, objs):
        try:
            self.left_collision(objects,objs)
            self.right_collision(objects,objs)
            self.up_collision(objects, objs)
            self.down_collision(objects, objs)
        except Exception as Error:
            print("runtime error in CollisionEngine.py Function detectCollisions: ", Error)

    def up_collision(self, objects, objs):
        try:
            if objects.rect.colliderect(objs.rect):
                if abs(objs.rect.bottom - objects.rect.top) < objs.rect.height:
                    objects.collisionUp = True
                    self.save_collision_object(objects, objs)
                    self.level_object_hit_box(objects,objs)     
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function up_collision: ", Error) 

    def down_collision(self, objects, objs):
        try:
            if objects.rect.colliderect(objs.rect):
                if abs(objs.rect.top - objects.rect.bottom) < objs.rect.height:
                    objects.collisionDown = True
                    self.save_collision_object(objects,objs)  
                    self.game_object_hit_box(objects,objs)
                    self.player_hit_box_y(objects,objs)
                    if not objects.jumping:
                        objects.position[1] = objs.rect.top - objects.rect.height       
        except Exception as Error:
            print('runtime error in CollisionEngine.py. Function down_collision: ', Error)
                                
    def left_collision(self,objects,objs):
        try:
            offset = objects.rect.width/2
            if objects.rect.left - offset< objs.rect.right:
                if objects.rect.right > objs.rect.left and objects.rect.right > objs.rect.right:
                    if (objs.rect.topright[1] < objects.rect.top < objs.rect.bottomright[1] or 
                        objs.rect.topright[1] < objects.rect.centery < objs.rect.bottomright[1] or 
                        objs.rect.topright[1] < objects.rect.bottom - offset< objs.rect.bottomright[1]):               
                        objects.collisionLeft = True
                        self.save_collision_object(objects,objs)  
                        self.player_hit_box_x(objects,objs)
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function left_collision: ", Error)
    
    def right_collision(self,objects,objs):
        try:
            offset = objects.rect.width/2
            if objects.rect.right + offset > objs.rect.left:
                if objects.rect.left < objs.rect.right and objects.rect.right < objs.rect.right:
                    if (objs.rect.topleft[1] < objects.rect.top < objs.rect.bottomleft[1]  or 
                        objs.rect.topleft[1] < objects.rect.centery < objs.rect.bottomleft[1] or 
                        objs.rect.topleft[1] < objects.rect.bottom - offset < objs.rect.bottomleft[1]):                  
                        objects.collisionRight = True   
                        self.save_collision_object(objects,objs)  
                        self.player_hit_box_x(objects,objs)
        except Exception as Error:
            print("runtime errir in CollisionEngine.py. Function right_collision: ", Error)
                                                
    def updateRectPosition(self, collisionObject):
        try:
            collisionObject.rect.x = collisionObject.position[0]
            collisionObject.rect.y = collisionObject.position[1]
            if collisionObject.hit_box is not None:
                collisionObject.hit_box.x = collisionObject.position[0]
                collisionObject.hit_box.y = collisionObject.position[1] - 8
                
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function updateRectPosition: ", Error)

    def save_collision_object(self, objects, objs):
        try:
            objects.collisionSubClass = objs.subClass
            objects.collisionObjDirection = objs.x_direction
            objects.collisionObject = objs
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function save_collision_object: ", Error)       

    def player_hit_box_x(self,objects,objs):
        try:
            enemyCollision = False
            if (objs.subClass == 'enemy' and not objects.subClass == 'enemy' ) or objs.subClass == 'powerup': 
                                enemyCollision = True
                                objects._set_mask()
                                objs._set_mask()
                                if objects.image_mask.overlap(objs.image_mask, (
                                objs.position[0] - objects.position[0], objs.position[1] - objects.position[1])):

                                    if objects.subClass == 'player' and objs.subClass == 'enemy':
                                        if objects.rect.top < objs.rect.centery < objects.rect.bottom:
                                            objects.isHit = True
                                    if objects.subClass == 'player' and objs.subClass == 'powerup':
                                        objs.isHit = True
                                        objects.powerUp = True
                                        self.save_collision_object(objects,objs)
            return enemyCollision
                         
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function player_hit_box: ", Error)
    
    def player_hit_box_y(self,objects,objs):
        try: 
            if objects.subClass == 'enemy' and objs.subClass == 'player':
                objs.isHit = True
            if objects.subClass == 'powerup' and objs.subClass == 'player':
                objects.isHit = True
                objs.powerUp = True
                self.save_collision_object(objs,objects)
            if objects.subClass == 'player' and objs.subClass == 'enemy':
                objs.isHit = True
                objects.powerUp = True
                self.save_collision_object(objects,objs)

        except Exception as Error:
            print("runtime error in CollisionEngine. Function payer_hit_box_y: ", Error)

    def game_object_hit_box(self,objects,objs):
        try:

            if objs.subClass =='enemy' and objects.subClass == 'player':  
                if objs.hitbox.colliderect(objects.rect):      
                #if objs.rect.left  < objects.rect.centerx < objs.rect.right:
                    objects.onEnemy = True
                    objs.isHit = True
            if objs.subClass == 'powerup' and objects.subClass == 'player':
                objs.isHit = True
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function game_object_hit_box: ", Error)

    def level_object_hit_box(self,objects,objs):
        try:
            if isinstance(objs, BlockObject._BlockObject):
                if (objs.rect.left < objects.rect.centerx < objs.rect.right):
                    objs.hit = True  
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function level_object_hit_box: ", Error)