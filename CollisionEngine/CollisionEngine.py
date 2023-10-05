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
            except:
                pass

    def detectCollisions(self, objects, objs):

        self.left_collision(objects,objs)
        self.right_collision(objects,objs)
        self.up_collision(objects, objs)
        self.down_collision(objects, objs)

    def up_collision(self, objects, objs):
        if objects.rect.colliderect(objs.rect):
            if objects.rect.top < objs.rect.bottom:
                if objects.rect.bottom > objs.rect.bottom and objects.rect.centery > objs.rect.bottom:
                    if objs.rect.left - objects.rect.width/2 < objects.rect.centerx < objs.rect.right + objects.rect.width/2:
                        objects._set_mask()
                        objs._set_mask()
                        if objects.image_mask.overlap(objs.image_mask, (
                                objects.position[0] - objs.position[0],
                                objects.position[1] - objs.position[1])):
                            objects.collisionSubClass = objs.subClass
                            objects.collisionObjDirection = objs.x_direction
                            objects.collisionObject = objs
                            objects.collisionUp = True
                            if isinstance(objs, BlockObject._BlockObject):
                                objs.hit = True

    def down_collision(self, objects, objs):
        if objects.rect.colliderect(objs.rect):
            if (objects.rect.bottom > objs.rect.top and objects.rect.top < objs.rect.top and 
                objects.rect.centery < objs.rect.top):

                if (objs.rect.left - objects.rect.width/2 < objects.rect.centerx < objs.rect.right + objects.rect.width/2):
                    objects._set_mask()
                    objs._set_mask()
                    if objects.image_mask.overlap(objs.image_mask, (
                        objs.position[0] - objects.position[0], objs.position[1] - objects.position[1])):    
                        objects.collisionDown = True
                        objects.collisionObject = objs
                        objects.collisionSubClass = objs.subClass
                        objects.collisionObjDirection = objs.x_direction

                        if objs.subClass =='enemy' and objects.subClass == 'player':    
                            objects.onEnemy = True
                            objs.isHit = True
                        else:
                            if not objects.jumping:
                                objects.position[1] = objs.rect.top - objects.rect.height
                                                                              
                            
    def left_collision(self,objects,objs):   
        offset =5
        if objects.rect.left - offset< objs.rect.right:
            if objects.rect.right > objs.rect.left and objects.rect.right > objs.rect.right:
                if (objs.rect.topright[1] < objects.rect.top < objs.rect.bottomright[1] or 
                    objs.rect.topright[1] < objects.rect.centery < objs.rect.bottomright[1] or 
                    objs.rect.topright[1] < objects.rect.bottom - offset< objs.rect.bottomright[1]):
                    
                    if True:
                        objects.collisionSubClass = objs.subClass
                        objects.collisionObjDirection = objs.x_direction
                        objects.collisionObjects = objs
                        objects.collisionLeft = True
                        if objs.subClass == 'enemy' or objs.subClass =='powerup':
                            objects._set_mask()
                            objs._set_mask()
                            if not objects.image_mask.overlap(objs.image_mask, (
                            objs.position[0] - objects.position[0], objs.position[1] - objects.position[1])):
                                objects.collisionLeft = False
  
    def right_collision(self,objects,objs):

        offset =5

        if objects.rect.right + offset > objs.rect.left:
            if objects.rect.left < objs.rect.right and objects.rect.right < objs.rect.right:
                if (objs.rect.topleft[1] < objects.rect.top < objs.rect.bottomleft[1]  or 
                    objs.rect.topleft[1] < objects.rect.centery < objs.rect.bottomleft[1] or 
                    objs.rect.topleft[1] < objects.rect.bottom - offset < objs.rect.bottomleft[1]):
                    if True:                     
                        objects.collisionSubClass = objs.subClass
                        objects.collisionObjDirection = objs.x_direction
                        objects.collisionObjects = objs
                        objects.collisionRight = True   
                        if objs.subClass == 'enemy' or objs.subClass == 'powerup':
                            objects._set_mask()
                            objs._set_mask()
                            if not objects.image_mask.overlap(objs.image_mask, (
                            objs.position[0] - objects.position[0], objs.position[1] - objects.position[1])):
                                objects.collisionRight = False 
          

    def updateRectPosition(self, collisionObject):

        collisionObject.rect.x = collisionObject.position[0]
        collisionObject.rect.y = collisionObject.position[1]
