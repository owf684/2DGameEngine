import math


class PhysicsEngine:

    def __init__(self):
        self.gravity = 9.8 * 135
        self.y_displacement = 0
        self.jump_displacement = 0
        self.x_displacement = 0
        self.x_direction = 0
        self.x_decelleration = 0.01
        self.y_displacement = 0

    def main_loop(self, objects, delta_t, o_level_handler):
        if not o_level_handler.pause_for_damage:
            self.simulate_gravity(objects, delta_t, o_level_handler)
            self.x_position(objects, delta_t, o_level_handler)

    def simulate_gravity(self, objects, delta_t, levelHandler):

        '''
		KINEMATIC EQUATIONS
		P(t) = VY * t + 0.5 * a * t^2

		V(t) = VY + a * t
		'''

        if objects.isRendered and not objects.pause_physics and ( not levelHandler.trigger_powerup_animation or objects.subClass == 'powerup') :

            objects.velocityY -= self.gravity * delta_t

            if not objects.collisionDown or objects.jumping:

                objects.y_displacement = objects.velocityY * delta_t + (self.gravity * math.pow(delta_t, 2))
                objects.position[1] -= objects.y_displacement

            elif objects.collisionDown:
                objects.y_displacement = 0
                objects.velocityY = 0

    def x_position(self, objects, delta_t, levelHandler):

        if objects.isRendered and not objects.pause_physics and not levelHandler.trigger_death_animation and not levelHandler.trigger_powerup_animation:

            objects.velocityX1 = objects.velocityX * objects.x_direction

            if delta_t != 0:

                objects.x_acceleration = objects.velocityX1 / delta_t

            else:
                objects.x_acceleration = 0

            if (not objects.collisionLeft and objects.x_direction == -1) or (
                not objects.collisionRight and objects.x_direction == 1): 
                '''or (
                    objects.subClass == 'powerup' and objects.collisionSubClass == 'player') or (
                    objects.subClass == 'enemy'   and objects.collisionSubClass == 'player'):'''
                
                objects.x_displacement = objects.velocityX1 * delta_t + (
                        0.5 * objects.x_acceleration * math.pow(delta_t, 2))
            else:
                objects.x_displacement = 0
            if not objects.scrolling:
                objects.position[0] += objects.x_displacement
