import sys
import os
import pygame
import time
import math
import cProfile
import pickle
import copy
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
#Custom Libraries Kinda
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

clock = pygame.time.Clock()

collisionList = list()
collisionList.extend(GameObjects)
collisionList.extend(levelObjects)


pygame_events = None
#simulation runtime variables
delta_t = 0
FPS = 60


		
#main loop
running = True
while running:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False

	pygame_events = pygame.event.get()

	#Inputs Engine
	input_dict = IE.main_loop(GameObjects,delta_t,pygame_events)

	#UI Engine
	#UIE.main_loop()

	#Physics Engine
	PE.main_loop(GameObjects,delta_t)

	#Collision Engine
	CE.main_loop(collisionList,GE)

	#PlayerMechanics Engine
	PlE.main_loop(GameObjects,delta_t,input_dict)

	#PlatformMechanics Engine
	#PfE.main_loop()

	#Graphics Engine
	screen = GE.main_loop(GameObjects,levelObjects,LH)

	#Level Builer
	LB.main_loop(input_dict,screen,levelObjects,collisionList,LH,PlE,GameObjects)

	LH.main_loop(levelObjects,PlE)

	#limit game to 60 fps
	#time.sleep(0.0033)
	
	
	clock.tick(FPS)

	delta_t = clock.tick(FPS)/1000


pygame.quit()
