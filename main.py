import sys
import os
import pygame
import time
import math
import cProfile
sys.path.append('./GraphicsEngine')
sys.path.append('./InputsEngine')
sys.path.append('./UIEngine')
sys.path.append('./PhysicsEngine')
sys.path.append('./MechanicsEngine/PlayerEngine')
sys.path.append('./MechanicsEngine/PlatformsEngine')
sys.path.append('./GameObjects')
sys.path.append('./CollisionEngine')
sys.path.append('./LevelBuilder')
sys.path.append('./LevelHandler')

import GraphicsEngine
import GraphicsEngineData
import InputsEngine
import UIEngine
import PhysicsEngine
import PlayerEngine
import PlatformsEngine
import GameObject
import CollisionEngine
import LevelBuilder
import LevelHandler

#Initialize Inputs engine
IE = InputsEngine._InputsEngine()
#Initialize UI Engine
UIE = UIEngine._UIEngine()

#Initialize Physics Engine
PE = PhysicsEngine._PhysicsEngine()

#Initialize Player Engine
PlE  = PlayerEngine._PlayerEngine()

#Initialize Platforms Engine
PfE  = PlatformsEngine._PlatformsEngine()

#Initialize Graphics Engine
GE = GraphicsEngine._GraphicsEngine()
GE._setScreenSize(1280,720)

#Initialize Collision Engine
CE = CollisionEngine._CollisionEngine()

#Initialize Level Builder
LB = LevelBuilder._LevelBuilder()

#Intialize Level Handler
LH = LevelHandler._LevelHandler()

#This will have to change
#Initialize GameObjects
GameObjects = list()
PlayerObject = GameObject._GameObject()
PlayerObject._set_sub_class('player')
PlayerObject._set_image_path('./Assets/PlayerSprites/LJ.png')
PlayerObject._set_image()
PlayerObject._set_sprite_size(PlayerObject.image)
PlayerObject._set_rect(PlayerObject.sprite_size)
GameObjects.append(PlayerObject)



levelObjects = list()
#add first platform
PlatformObject = GameObject._GameObject()
PlatformObject._set_sub_class('platform')
PlatformObject._set_image_path('./Assets/Platforms/large_platform.png')
PlatformObject._set_image()
PlatformObject.position = [400,450]
PlatformObject._set_sprite_size(PlatformObject.image)
PlatformObject._set_rect(PlatformObject.sprite_size)
levelObjects.append(PlatformObject)

#add first platform
PlatformObject2 = GameObject._GameObject()
PlatformObject2._set_sub_class('platform')
PlatformObject2._set_image_path('./Assets/Platforms/large_platform.png')
PlatformObject2._set_image()
PlatformObject2.position = [200,200]
PlatformObject2._set_sprite_size(PlatformObject.image)
PlatformObject2._set_rect(PlatformObject.sprite_size)
levelObjects.append(PlatformObject2)
clock = pygame.time.Clock()

collisionList = list()
collisionList.extend(GameObjects)
collisionList.extend(levelObjects)

#simulation runtime variables
delta_t = 0
FPS = 60

#main loop
running = True
while running:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False


	#Inputs Engine
	#cProfile.run('IE.main_loop(GameObjects,delta_t)',sort='cumulative')
	input_dict = IE.main_loop(GameObjects,delta_t)
	#UI Engine
	#UIE.main_loop()

	#Physics Engine
	PE.main_loop(GameObjects,delta_t)

	#Collision Engine
	CE.main_loop(collisionList)

	#PlayerMechanics Engine
	PlE.main_loop(GameObjects,delta_t)

	#PlatformMechanics Engine
	#PfE.main_loop()

	#Graphics Engine
	#cProfile.run('GE.main_loop(GameObjects,levelObjects)',sort='cumulative')

	screen = GE.main_loop(GameObjects,levelObjects,LH)

	#Level Builer
	LB.main_loop(input_dict,screen,levelObjects,collisionList,LH,PlE)

	LH.main_loop(levelObjects,PlE)

	#limit game to 60 fps
	#time.sleep(0.0033)

	
	clock.tick(FPS)

	delta_t = clock.tick(FPS)/1000

pygame.quit()
