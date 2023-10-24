
from dataclasses import dataclass

@dataclass
class PhysicsObject:

    position        : list
    velocity        : list
    acceleration    : list
    force           : list
    displacement    : list
    mass            : float
    pause           : bool

    def set_position(self,position=[0,0]):
        self.position = position

    def set_velocity(self,velocity=[0,0]):
        self.velocity = velocity

    def set_acceleration(self,acceleration=[0,0]):
        self.acceleration = acceleration

    def set_force(self,force=[0,0]):
        self.force = force

    def set_displacement(self,displacement=[0,0]):
        self.displacement = displacement
    
    def set_mass(self, mass):
        self.mass = mass

    def get_position(self):
        return self.position
    
    def get_velocity(self):
        return self.velocity
    
    def get_acceleration(self):
        return self.acceleration
    
    def get_force(self):
        return self.force
    
    def get_displacement(self):
        return self.displacement
    
    def get_mass(self):
        return self.mass
