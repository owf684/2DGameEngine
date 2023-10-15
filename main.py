import sys
import pygame

#Library Paths
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
sys.path.append('./MechanicsEngine/ItemEngine')
#Game Libraries
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
import PlayerObject
import ItemEngine 

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

# Initialize Block Engine
BE = BlockEngine._BlockEngine()

# Initialize PowerUpEngine
PUP = PowerUpEngine._PowerUpEngine()

# Initialize ItemEngine
_ItemEngine = ItemEngine._ItemEngine()

# Initialize GameObjects
GameObjects = list()
PlayerObjects = PlayerObject._PlayerObject()
PlayerObjects._set_sub_class('player')
PlayerObjects._set_image_path('./Assets/PlayerSprites/mario/mario_32x32_idle_right.png')
PlayerObjects._set_image()
PlayerObjects._set_sprite_size(PlayerObjects.image)
PlayerObjects._set_rect(PlayerObjects.sprite_size)
PlayerObjects._set_hit_box(PlayerObjects.sprite_size,16)
PlayerObjects._set_mask()
GameObjects.append(PlayerObjects)

# Initialize Level Objects
levelObjects = list()

# Initialize Collision List
collisionList = list()
collisionList.extend(GameObjects)
collisionList.extend(levelObjects)

# Start clock
clock = pygame.time.Clock()

# simulation runtime variables
pygame_events = None
delta_t = 0
FPS = 30
		
# main game loop
running = True
while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame_events = pygame.event.get()

	# Inputs Engine | Update our inputs once a frame
	input_dict = IE.main_loop(GameObjects,delta_t,pygame_events)

	# Graphics Engine | Update our graphics once a frame
	GE.main_loop(GameObjects, levelObjects, LH,LB)

	# game and level objects are only updated in play mode
	if not LB.edit:

		# update all game and level objects once a frame
		for objects in GE.render_buffer:

			# Physics Engine | Maintain this order. Physics is always first. Collisions is always second.
			PE.main_loop(objects, delta_t, LH)

			# Collision Engine
			CE.main_loop(objects, GE, LH)

			# PlayerMechanics Engine
			PlE.main_loop(objects, delta_t, input_dict, CE, LH, GameObjects)

			# Enemy Engine
			EE.main_loop(GameObjects, PlE, GE,objects)
			
			# Animation System
			AS.main_loop(objects, GameObjects, levelObjects, input_dict, LH, delta_t, PlE, GE)

			# Block Engine
			BE.main_loop(GameObjects, levelObjects, PlE, delta_t,objects)

			# PowerUp Engine
			PUP.main_loop(GameObjects, LH, PlE,GE, objects)

			# Item Engine
			_ItemEngine.main_loop(objects,levelObjects, GameObjects, LH, PlE)

		# Level Handler
		LH.main_loop(LH, GameObjects, levelObjects, collisionList, GE.screen, PlE, LB, EE)

		if LH.edit_mode:
			LB.edit = True
			LH.edit_mode = False
			AS.reset_animations = True
			
	# Level Builder
	LB.main_loop(input_dict, GE.screen, levelObjects, collisionList, LH, PlE, GameObjects,GE)

	delta_t = clock.tick(FPS)/1000

pygame.quit()
