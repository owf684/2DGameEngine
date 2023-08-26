import sys
import os
import pygame
sys.path.append('./GraphicsEngine')
sys.path.append('./InputsEngine')
sys.path.append('./UIEngine')
sys.path.append('./PhysicsEngine')
sys.path.append('./MechanicsEngine/PlayerEngine')
sys.path.append('./MechanicsEngine/PlatformsEngine')

import GraphicsEngine
import GraphicsEngineData
import InputsEngine
import UIEngine
import PhysicsEngine
import PlayerEngine
import PlatformsEngine


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
#GE._setScreenTitle(('Hello World!'))
GE._addImage2Buffer('./Assets/PlayerSprites/mario.png')

#main loop
running = True
while running:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False

		#Inputs Engine
		IE.main_loop()
		#UI Engine
		UIE.main_loop()

		#Physics Engine
		PE.main_loop()

		#PlayerMechanics Engine
		PlE.main_loop()

		#PlatformMechanics Engine
		PfE.main_loop()

		GE.main_loop()

		#GraphicsEngine._updateGraphics(GED,PSD)


pygame.quit()
