import copy
import sys

sys.path.append("./GameObjects")
import BlockObject


class _CollisionEngine:

    def __init__(self):

        self.collision = False
        self.collisionLeft = False
        self.collisionRight = False
        self.collisionDown = False
        self.threadStarted = False
        self.screen = None
        self.collisionThread = list()
        self.collision_tolerance = 10

    def main_loop(self, objects, GraphicsEngine, input_dict, screen):
        self.screen = screen
        i = 0
        currentObject = 0
        # Reset collisions here please!
        objects.collisionDown = False
        objects.collisionLeft = False
        objects.collisionRight = False
        objects.collisionUp = False

        for objs in GraphicsEngine.render_buffer:

            try:
                self.updateRectPosition(objects)
                if objects != objs:
                    if (
                            objects.subClass == 'player' or objects.subClass == 'enemy' or objects.subClass == 'powerup') and objs.subClass != 'environment':
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
                    self.save_collision_object(objects, objs)
                    objects.collisionUp = True
                    if isinstance(objs, BlockObject._BlockObject):
                        if (objs.rect.left < objects.rect.centerx < objs.rect.right):
                            objs.hit = True       
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function up_collision: ", Error) 

    def down_collision(self, objects, objs):
        try:
            if objects.rect.colliderect(objs.rect):
                if abs(objs.rect.top - objects.rect.bottom) < objs.rect.height:
                    objects.collisionDown = True
                    self.save_collision_object(objects,objs)  

                    if not objects.jumping:
                        objects.position[1] = objs.rect.top - objects.rect.height 
                    if objs.subClass =='enemy' and objects.subClass == 'player':        
                        if objs.rect.left  < objects.rect.centerx < objs.rect.right:
                            objects.onEnemy = True
                            objs.isHit = True
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
                        if True:
                            self.save_collision_object(objects,objs)  
                            objects.collisionLeft = True
                            if objs.subClass == 'enemy' or objs.subClass =='powerup':
                                objects._set_mask()
                                objs._set_mask()
                                if not objects.image_mask.overlap(objs.image_mask, (
                                objs.position[0] - objects.position[0], objs.position[1] - objects.position[1])):
                                    objects.collisionLeft = False
                                else:
                                    if objects.subClass =='player' and objs.subClass == 'enemy':
                                        if objects.rect.top < objs.rect.centery < objects.rect.bottom:
                                            objects.isHit = True
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
                        if True:                     
                            self.save_collision_object(objects,objs)  
                            objects.collisionRight = True   
                            if objs.subClass == 'enemy' or objs.subClass == 'powerup':
                                objects._set_mask()
                                objs._set_mask()
                                if not objects.image_mask.overlap(objs.image_mask, (
                                objs.position[0] - objects.position[0], objs.position[1] - objects.position[1])):
                                    objects.collisionRight = False 
                                else:
                                    if objects.subClass == 'player' and objs.subClass == 'enemy':
                                        if objects.rect.top < objs.rect.centery < objects.rect.bottom:
                                            objects.isHit = True
        except Exception as Error:
            print("runtime errir in CollisionEngine.py. Function right_collision: ", Error)
                                                

    def updateRectPosition(self, collisionObject):
        try:
            collisionObject.rect.x = collisionObject.position[0]
            collisionObject.rect.y = collisionObject.position[1]
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function updateRectPosition: ", Error)

    def save_collision_object(self, objects, objs):
        try:
            objects.collisionSubClass = objs.subClass
            objects.collisionObjDirection = objs.x_direction
            objects.collisionObject = objs
        except Exception as Error:
            print("runtime error in CollisionEngine.py. Function save_collision_object: ", Error)        