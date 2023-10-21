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
sys.path.append("./AudioEngine")
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
import AudioEngine

# Initialize Inputs engine
_InputsEngine = InputsEngine._InputsEngine()

# Initialize UI Engine
_UIEngine = UIEngine._UIEngine()

# Initialize Physics Engine
_PhysicsEngine = PhysicsEngine._PhysicsEngine()

# Initialize Player Engine
_PlayerEngine = PlayerEngine._PlayerEngine()

# Initialize Enemy Engine
_EnemyEngine = EnemyEngine._EnemyEngine()

# Initialize Platforms Engine
_PlatformsEngine = PlatformsEngine._PlatformsEngine()

# Initialize Graphics Engine
_GraphicsEngine = GraphicsEngine._GraphicsEngine()
_GraphicsEngine._setScreenSize(1280,720)

# Initialize Collision Engine
_CollisionEngine = CollisionEngine._CollisionEngine()

# Initialize Level Builder
_LevelBuilder = LevelBuilder._LevelBuilder()

# Initialize Level Handler
_LevelHandler = LevelHandler._LevelHandler()

# Initialize Animation System
_AnimationSystem = AnimationSystem._AnimationSystem()

# Initialize Block Engine
_BlockEngine = BlockEngine._BlockEngine()

# Initialize PowerUpEngine
_PowerUpEngine = PowerUpEngine._PowerUpEngine()

# Initialize ItemEngine
_ItemEngine = ItemEngine._ItemEngine()

# initialize AudioEngine
_AudioEngine = AudioEngine._AudioEngine()

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
	input_dict = _InputsEngine.main_loop(GameObjects,delta_t,pygame_events)

	# Graphics Engine | Update our graphics once a frame
	_GraphicsEngine.main_loop(GameObjects, levelObjects, _LevelHandler,_LevelBuilder)

	# game and level objects are only updated in play mode
	if not _LevelBuilder.edit:

		# update all game and level objects once a frame
		for objects in _GraphicsEngine.render_buffer:

			# Physics Engine | Maintain this order. Physics is always first. Collisions is always second.
			_PhysicsEngine.main_loop(objects, delta_t, _LevelHandler)

			# Collision Engine
			_CollisionEngine.main_loop(objects, _GraphicsEngine, _LevelHandler)

			# Audio Engine
			_AudioEngine.main_loop(objects,_LevelHandler,_PlayerEngine, _EnemyEngine)

			# PlayerMechanics Engine
			_PlayerEngine.main_loop(objects, delta_t, input_dict, _CollisionEngine, _LevelHandler, GameObjects)

			# Enemy Engine
			_EnemyEngine.main_loop(GameObjects, _PlayerEngine, _GraphicsEngine,objects)
			
			# Animation System
			_AnimationSystem.main_loop(objects, GameObjects, levelObjects, input_dict, _LevelHandler, delta_t, _PlayerEngine, _GraphicsEngine, _EnemyEngine)

			# Block Engine
			_BlockEngine.main_loop(GameObjects, levelObjects, _PlayerEngine, delta_t,objects)

			# PowerUp Engine
			_PowerUpEngine.main_loop(GameObjects, _LevelHandler, _PlayerEngine,_GraphicsEngine, objects)

			# Item Engine
			_ItemEngine.main_loop(objects,levelObjects, GameObjects, _LevelHandler, _PlayerEngine)

		# Level Handler
		_LevelHandler.main_loop(_LevelHandler, GameObjects, levelObjects, collisionList, _GraphicsEngine.screen, _PlayerEngine, _LevelBuilder, _EnemyEngine)


		if _LevelHandler.edit_mode:
	
			_LevelBuilder.edit = True
			_LevelHandler.edit_mode = False
			_AnimationSystem.reset_animations = True
			
	# Level Builder
	_LevelBuilder.main_loop(input_dict, _GraphicsEngine.screen, levelObjects, collisionList, _LevelHandler, _PlayerEngine, GameObjects,_GraphicsEngine)
	if _LevelBuilder.edit:
		_AudioEngine.stop_over_world_music()

	delta_t = clock.tick(FPS)/1000

pygame.quit()
