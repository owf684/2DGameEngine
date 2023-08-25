import sys
import os
import pygame
sys.path.append('./GraphicsEngine')
import GraphicsEngine
import GraphicsEngineData

#initialize engine variables
GED = GraphicsEngineData._GraphicsEngineData
GraphicsEngine._initWindow(GED)

PSD = GraphicsEngineData._PlayerSpriteData()
PSD.set_image_path("./Assets/PlayerSprites/mario.png")
PSD.set_image(PSD.get_image_path())

#main loop
running = True
while running:

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False


		GraphicsEngine._updateGraphics(GED,PSD)


pygame.quit()