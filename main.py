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
import graphics_engine
import inputs_engine
import ui_engine
import physics_engine
import player_engine
import platforms_engine
import game_object
import collision_engine
import level_builder
import level_handler
import enemy_engine
import animation_system
import block_engine
import powerup_engine
import player_object
import item_engine 
import audio_engine

# Initialize Inputs engine
o_inputs_engine = inputs_engine.InputsEngine()

# Initialize UI Engine
o_ui_engine = ui_engine.UIEngine()

# Initialize Physics Engine
o_physics_engine = physics_engine.PhysicsEngine()

# Initialize Player Engine
o_player_engine = player_engine.PlayerEngine()

# Initialize Enemy Engine
o_enemy_engine = enemy_engine.EnemyEngine()

# Initialize Platforms Engine
o_platforms_engine = platforms_engine.PlatformsEngine()

# Initialize Graphics Engine
o_graphics_engine = graphics_engine.GraphicsEngine()
o_graphics_engine.set_screen_size(1280,720)

# Initialize Collision Engine
o_collision_engine = collision_engine.CollisionEngine()

# Initialize Level Builder
o_level_builder = level_builder.LevelBuilder()

# Initialize Level Handler
o_level_handler = level_handler.LevelHandler()

# Initialize Animation System
o_animation_system = animation_system.AnimationSystem()

# Initialize Block Engine
o_block_engine = block_engine.BlockEngine()

# Initialize PowerUpEngine
o_powerup_engine = powerup_engine.PowerupEngine()

# Initialize ItemEngine
o_item_engine = item_engine.ItemEngine()

# initialize AudioEngine
o_audio_engine = audio_engine.AudioEngine()

# Initialize GameObjects
l_game_objects = list()
o_player_object = player_object.PlayerObject()
o_player_object._set_sub_class('player')
o_player_object._set_image_path('./Assets/PlayerSprites/mario/mario_32x32_idle_right.png')
o_player_object._set_image()
o_player_object._set_sprite_size(o_player_object.image)
o_player_object._set_rect(o_player_object.sprite_size)
o_player_object._set_hit_box(o_player_object.sprite_size,16)
o_player_object._set_mask()
l_game_objects.append(o_player_object)

# Initialize Level Objects
l_level_objects = list()

# Initialize Collision List
l_collision_objects = list()
l_collision_objects.extend(l_game_objects)
l_collision_objects.extend(l_level_objects)

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
	d_inputs = o_inputs_engine.main_loop(l_game_objects)

	# Graphics Engine | Update our graphics once a frame
	o_graphics_engine.main_loop(l_game_objects, l_level_objects, o_level_handler,o_level_builder)

	# game and level objects are only updated in play mode
	if not o_level_builder.edit:

		# update all game and level objects once a frame
		for objects in o_graphics_engine.render_buffer:

			# Physics Engine | Maintain this order. Physics is always first. Collisions is always second.
			o_physics_engine.main_loop(objects, delta_t, o_level_handler)

			# Collision Engine
			o_collision_engine.main_loop(objects, o_graphics_engine, o_level_handler)

			# Audio Engine
			o_audio_engine.main_loop(objects,o_level_handler,o_player_engine, o_enemy_engine)

			# PlayerMechanics Engine
			o_player_engine.main_loop(objects, delta_t, d_inputs, o_collision_engine, o_level_handler, l_game_objects)

			# Enemy Engine
			o_enemy_engine.main_loop(l_game_objects, o_player_engine, o_graphics_engine,objects)
			
			# Animation System
			o_animation_system.main_loop(objects, l_game_objects, l_level_objects, d_inputs, o_level_handler, delta_t, o_player_engine, o_graphics_engine, o_enemy_engine)

			# Block Engine
			o_block_engine.main_loop(l_game_objects, l_level_objects, o_player_engine, delta_t,objects)

			# PowerUp Engine
			o_powerup_engine.main_loop(l_game_objects, o_level_handler, o_player_engine,o_graphics_engine, objects)

			# Item Engine
			o_item_engine.main_loop(objects,l_level_objects, l_game_objects, o_level_handler, o_player_engine)

		# Level Handler
		o_level_handler.main_loop(l_game_objects, l_level_objects, l_collision_objects, o_graphics_engine.screen, o_player_engine, o_level_builder, o_enemy_engine)


		if o_level_handler.edit_mode:
	
			o_level_builder.edit = True
			o_level_handler.edit_mode = False
			o_animation_system.reset_animations = True
			
	# Level Builder
	o_level_builder.main_loop(d_inputs, o_graphics_engine.screen, l_level_objects, l_collision_objects, o_level_handler, o_player_engine, l_game_objects,o_graphics_engine)
	if o_level_builder.edit:
		o_audio_engine.stop_over_world_music()

	delta_t = clock.tick(FPS)/1000

pygame.quit()
