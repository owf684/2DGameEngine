import sys
import pygame

sys.path.append('./GraphicsEngine')
sys.path.append('./InputsEngine')
sys.path.append('./UIEngine')
sys.path.append('./PhysicsEngine')
sys.path.append('./MechanicsEngine/PlayerEngine')
sys.path.append('./MechanicsEngine/PlatformsEngine')
sys.path.append('./MechanicsEngine/EnemyEngine')
sys.path.append('./GameObjects')
sys.path.append('./CollisionEngine')
sys.path.append('./LevelBuilder')
sys.path.append('./LevelHandler')
sys.path.append('./AnimationSystem')
sys.path.append('./MechanicsEngine/BlockEngine')
sys.path.append('./MechanicsEngine/PowerUpEngine')

#Custom Libraries Kinda
import GraphicsEngine
import InputsEngine
import UIEngine
import PhysicsEngine
import PlayerEngine
import PlatformsEngine
import GameObject
import CollisionEngine
import LevelBuilder
import LevelHandler
import EnemyEngine
import AnimationSystem
import BlockEngine
import PowerUpEngine

# Initialize Inputs engine
IE = InputsEngine._InputsEngine()
# Initialize UI Engine
UIE = UIEngine._UIEngine()

# Initialize Physics Engine
PE = PhysicsEngine._PhysicsEngine()

# Initialize Player Engine
PlE = PlayerEngine._PlayerEngine()

# Initialize Enemy Engine
EE = EnemyEngine._EnemyEngine()

# Initialize Platforms Engine
PfE = PlatformsEngine._PlatformsEngine()

# Initialize Graphics Engine
GE = GraphicsEngine._GraphicsEngine()
GE._setScreenSize(1280,720)

# Initialize Collision Engine
CE = CollisionEngine._CollisionEngine()

# Initialize Level Builder
LB = LevelBuilder._LevelBuilder()

# Initialize Level Handler
LH = LevelHandler._LevelHandler()

# Initialize Animation System
AS = AnimationSystem._AnimationSystem()

#Initialize Block Engine
BE = BlockEngine._BlockEngine()

#Initialize PowerUpEngine
PUP = PowerUpEngine._PowerUpEngine()

# This will have to change
# Initialize GameObjects
GameObjects = list()
PlayerObject = GameObject._GameObject()
PlayerObject._set_sub_class('player')
PlayerObject._set_image_path('./Assets/PlayerSprites/mario_32x32_idle_right.png')
PlayerObject._set_image()
PlayerObject._set_sprite_size(PlayerObject.image)
PlayerObject._set_rect(PlayerObject.sprite_size)
PlayerObject._set_pixel_collision_map()
PlayerObject._set_mask()
print(len(PlayerObject.pixelCollisionMap[0]))
GameObjects.append(PlayerObject)

levelObjects = list()

clock = pygame.time.Clock()

collisionList = list()
collisionList.extend(GameObjects)
collisionList.extend(levelObjects)

pygame_events = None
# simulation runtime variables
delta_t = 0
FPS = 120


		
# main loop
running = True
while running:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False

	pygame_events = pygame.event.get()

	# Inputs Engine
	input_dict = IE.main_loop(GameObjects,delta_t,pygame_events)

	# Graphics Engine
	screen = GE.main_loop(GameObjects, levelObjects, LH,LB)
	if not LB.edit:
		# UI Engine
		# UIE.main_loop()

		# Physics Engine
		PE.main_loop(GameObjects, delta_t)

		# Collision Engine
		CE.main_loop(collisionList, GE, input_dict,screen)

		#Block Engine
		BE.main_loop(GameObjects,levelObjects,PlE,delta_t)

		# PlayerMechanics Engine
		PlE.main_loop(GameObjects, delta_t, input_dict, CE,LH)

		# Enemy Engine
		EE.main_loop(GameObjects,PlE,GE)
		# PlatformMechanics Engine
		# PfE.main_loop()


		
		# Animation System
		AS.main_loop(GameObjects, input_dict,LH)
		LH.main_loop(LH,GameObjects,levelObjects,collisionList, screen,PlE,LB)

		#PowerUp Engine
		PUP.main_loop(GameObjects, LH, PlE)

	# Level Builder
	LB.main_loop(input_dict, screen, levelObjects, collisionList, LH, PlE, GameObjects,GE)

	delta_t = clock.tick(FPS)/1000

	#delta_t = clock.tick(FPS)/1000


pygame.quit()
