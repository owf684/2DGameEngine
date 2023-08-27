import sys
import os
import pygame
import time
import math
sys.path.append('./GraphicsEngine')
sys.path.append('./InputsEngine')
sys.path.append('./UIEngine')
sys.path.append('./PhysicsEngine')
sys.path.append('./MechanicsEngine/PlayerEngine')
sys.path.append('./MechanicsEngine/PlatformsEngine')
sys.path.append('./GameObjects')

import GraphicsEngine
import GraphicsEngineData
import InputsEngine
import UIEngine
import PhysicsEngine
import PlayerEngine
import PlatformsEngine
import GameObject

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
GE._setScreenSize(800,800)

#This will have to change
#Initialize GameObjects
GameObjects = list()
PlayerObject = GameObject._GameObject()
PlayerObject._set_sub_class('player')
PlayerObject._set_image_path('./Assets/PlayerSprites/LJ.png')
PlayerObject._set_image()
GameObjects.append(PlayerObject)

#simulation runtime variables
delta1 = 0
delta2 = 0
delta = 0

#main loop
running = True
while running:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False

		delta1 = time.time()

		#Inputs Engine
		IE.main_loop(GameObjects,delta)

		#UI Engine
		UIE.main_loop()

		#Physics Engine
		PE.main_loop()

		#PlayerMechanics Engine
		PlE.main_loop()

		#PlatformMechanics Engine
		PfE.main_loop()

		#Graphics Engine
		GE.main_loop(GameObjects)

		#limit game to 60 fps
		time.sleep(0.016)

		delta2 = time.time()

		delta = abs(delta2-delta1)


pygame.quit()
