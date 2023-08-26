import sys
import os
import pygame
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
PlayerObject._set_image_path('./Assets/PlayerSprites/idle.png')
PlayerObject._set_image()
GameObjects.append(PlayerObject)

#main loop
running = True
while running:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False

		#Inputs Engine
		IE.main_loop(GameObjects)

		#UI Engine
		UIE.main_loop()

		#Physics Engine
		PE.main_loop()

		#PlayerMechanics Engine
		PlE.main_loop()

		#PlatformMechanics Engine
		PfE.main_loop()

		GE.main_loop(GameObjects)

		#GraphicsEngine._updateGraphics(GED,PSD)


pygame.quit()
