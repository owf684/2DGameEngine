
import pygame



def _initWindow(GED):


	pygame.init()

	GED.screen_width = 800 
	GED.screen_height = 600
	GED.screen = pygame.display.set_mode((GED.screen_width,GED.screen_height))
	pygame.display.set_caption("My Pygame Graphics")




def _updateGraphics(GED,PSD):
	
	#clear the screen
	GED.screen.fill((0,0,0))

	#Update your graphics Here
	GED.screen.blit(PSD.get_image(),(0,0))
	#Update the display
	pygame.display.flip()

	