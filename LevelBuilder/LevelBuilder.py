import pygame
import sys
sys.path.append('./GameObjects')
import GameObject
import copy
import glob
import os
import xml.etree.ElementTree as ET
class _LevelBuilder:


	def __init__(self):

		self.mouse_position = [0,0]
		self.scan_block_position = [0,0]
		self.scan_block_size = 32
		self.screen_width = 1280
		self.screen_height = 720
		self.block_color = (255,255,255)
		self.grid_size = 32
		self.grid_color = (255,255,255)
		self.placement_coords = [0,0]
		self.snap_position = [0,0]
		self.can_place_block = True
		self.list_of_placed_objects = list()
		self.scroll_offset_magnitude = 1
		self.scroll_offset_fudge = 0.5
		self.building_blocks = list()

		self.block_select_key = False
		self.selected_block_index = 0
		self.last_selected_index = 0
		self.create_level_select = False

		self.load_level_select = False

		self.patch_level_select = False

		self.initialize_building_blocks()

	def initialize_building_blocks(self):
		block_list = glob.glob('./Assets/Platforms/*.png')

		for blocks in block_list:
			new_block = GameObject._GameObject()
			new_block._set_sub_class('platform')
			new_block._set_image_path(blocks)
			new_block._set_image()
			new_block.position = [self.screen_width/2,self.screen_height/20]
			new_block._set_sprite_size(new_block.image)
			new_block._set_rect(new_block.sprite_size)

			self.building_blocks.append(new_block)
	

	

	def main_loop(self,input_dict,screen,levelObjects,collisionList,levelHandler,PlayerEngine,GameObjects,GraphicsEngine):
		
		self.poll_mouse(input_dict,screen,levelObjects,collisionList,levelHandler)
		self.handle_user_input(input_dict,levelObjects,collisionList,GameObjects,screen,levelHandler)
		self.ui(input_dict,screen,levelObjects,collisionList,levelHandler,GraphicsEngine)
				
	def poll_mouse(self,input_dict,screen,levelObjects,collisionList,levelHandler):

		#add block
		if input_dict['left-click'] == '1':

			self.mouse_position = pygame.mouse.get_pos()
			
			self.get_snap_values(input_dict,screen,levelObjects,levelHandler)

			if self.can_place_block:

				self.place_block(input_dict,screen,levelObjects,collisionList,levelHandler)
		#remove block
		if input_dict['right-click'] == '1':
			self.mouse_position = pygame.mouse.get_pos()
			print(self.mouse_position)
			for objects in levelObjects:

				if objects.rect.collidepoint(self.mouse_position):
					for points in self.list_of_placed_objects:
						if objects.rect.collidepoint(points):
							self.list_of_placed_objects.remove(points)

					levelObjects.remove(objects)
					levelHandler.clear_render_buffer = True
					

	def get_snap_values(self,input_dict,screen,levelObjects,levelHandler):

		self.can_place_block = True
		#get x snap value
		if levelHandler.scroll_offset != 0:
			self.scroll_offset_magnitude = levelHandler.scroll_offset/levelHandler.scroll_offset
		else:
			self.scroll_offset_magnitude = 1
			self.scroll_offset_fudge = 0


		self.snap_position[0] = int((self.mouse_position[0]) /self.grid_size)*self.grid_size-(levelHandler.scroll_delta*self.scroll_offset_magnitude) 
		#print(self.snap_position[0])
		#get y snap value
		self.snap_position[1] = int(self.mouse_position[1]/self.grid_size)*self.grid_size

		#draw the placement sqaure
		square_rect = pygame.Rect(self.snap_position[0], self.snap_position[1], self.scan_block_size, self.scan_block_size)
		
		#check if block already exists
		if self.snap_position in self.list_of_placed_objects:
			self.can_place_block = False

		pygame.draw.rect(screen, self.block_color, square_rect)
		#update the screen
		pygame.display.flip()

		
	def place_block(self,input_dict,screen,levelObjects,collisionList,levelHandler):

		#add first platform
		levelObjects.append(GameObject._GameObject())
		levelObjects[-1]._set_sub_class('platform')
		levelObjects[-1]._set_image_path(self.building_blocks[self.selected_block_index]._get_image_path())
		levelObjects[-1]._set_image()
		levelObjects[-1].position = copy.deepcopy(self.snap_position)
		levelObjects[-1].initial_position = copy.deepcopy((self.snap_position[0]+levelHandler.scroll_offset,self.snap_position[1]))
		self.list_of_placed_objects.append(copy.deepcopy(self.snap_position))
		levelObjects[-1]._set_sprite_size(levelObjects[-1].image)
		levelObjects[-1]._set_rect(levelObjects[-1].sprite_size)
		collisionList.append(levelObjects[-1])
		print(levelObjects[-1].initial_position)


	def ui(self,input_dict,screen,levelObjects,collisionList,levelHandler,GraphicsEngine):
			

		self.limit_selection_index()

		if self.building_blocks[self.selected_block_index] in GraphicsEngine.render_buffer and self.selected_block_index != self.last_selected_index:
			GraphicsEngine.render_buffer.remove(self.building_blocks[self.selected_block_index])
			print("removing from buffer 2 | selected_block_index: " + str(self.selected_block_index) + " | last_selected_index: " + str(self.last_selected_index))
		
			
		if self.building_blocks[self.selected_block_index] not in GraphicsEngine.render_buffer:

			GraphicsEngine.render_buffer.append(self.building_blocks[self.selected_block_index])
			self.last_selected_index = self.selected_block_index
			print("adding to buffer 1 | selected_block_index: " + str(self.selected_block_index) + " | last_selected_index: " + str(self.last_selected_index) )


	def handle_user_input(self,input_dict,levelObjects,collisionList,GameObjects,screen,levelHandler):

		#handles block selection 
		if input_dict["arrow_vert"] == "1" and not self.block_select_key:
			self.block_select_key = True
			self.selected_block_index += 1
		elif input_dict["arrow_vert"] == "-1" and not self.block_select_key:
			self.block_select_key = True
			self.selected_block_index -= 1
		elif input_dict["arrow_vert"] == "0":
			self.block_select_key = False	
		#write category selection here

		#handles save data
		if input_dict["create-level"] == "1" and not self.create_level_select:
			self.create_level_select = True

			self.save_level(levelObjects,GameObjects)
		
		elif input_dict["create-level"] == "0":
			self.create_level_select = False

		if input_dict["patch-level"] == "1" and not self.patch_level_select:
			
			self.patch_level_select = True
			self.patch_level(levelObjects,GameObjects)

		elif input_dict["patch-level"] == "0":
			
			self.patch_level_select = False
		
		#handle load data
		if input_dict["load-level"] == "1" and not self.load_level_select:
			self.load_level_select = True
			self.load_level(GameObjects,levelObjects,collisionList,"level_1",screen,levelHandler)
		elif input_dict["load-level"] == "0":
			self.load_level_select = False

	def limit_selection_index(self):

		if self.selected_block_index < 0:
			self.selected_block_index = 0

		elif self.selected_block_index >= len(self.building_blocks):
			self.selected_block_index = len(self.building_blocks)-1	

		#print(self.selected_block_index)

	def patch_level(self,levelObjects,GameObjects):
		selected_level = 1
		level_string = "level_" + str(selected_level)
		self.save_level_objects(levelObjects,level_string)
		self.save_game_objects(GameObjects,level_string)

	def save_level(self,levelObjects,GameObjects):
		new_level = len(glob.glob("./WorldData/level*")) + 1
		level_string = "level_" + str(new_level)
		os.mkdir("./WorldData/" + level_string)

		self.save_level_objects(levelObjects,level_string)
		self.save_game_objects(GameObjects,level_string)

	def save_level_objects(self,levelObjects,level_string):

		#get level number

		root = ET.Element("objects")
		obj = list()
		for objects in levelObjects:
			obj.append(ET.SubElement(root,"object"))

			sub_class = ET.SubElement(obj[-1],"subClass")
			sub_class.text = objects.subClass

			image_path = ET.SubElement(obj[-1],"imagePath")
			image_path.text = objects.imagePath

			position_x = ET.SubElement(obj[-1],"position_x")
			position_x.text = str(objects.initial_position[0])

			position_y = ET.SubElement(obj[-1],"position_y")
			position_y.text = str(objects.initial_position[1])


		tree = ET.ElementTree(root)
		
		tree.write("./WorldData/"+level_string+"/levelObjects.xml" )

	def save_game_objects(slef,GameObjects,level_string):

		root = ET.Element("objects")
		obj = list()
		for objects in GameObjects:
			obj.append(ET.SubElement(root,"object"))
			sub_class = ET.SubElement(obj[-1],"subClass")
			sub_class.text = objects.subClass 

			image_path = ET.SubElement(obj[-1],"imagePath")
			image_path.text = objects.imagePath

			position_x = ET.SubElement(obj[-1],"position_x")
			position_x.text = str(objects.initial_position[0])

			position_y = ET.SubElement(obj[-1],"position_y")
			position_y.text = str(objects.initial_position[1])

			accelerationX = ET.SubElement(obj[-1],"accelerationX")
			accelerationX.text = str(objects.accelerationX)

			jump_velocity = ET.SubElement(obj[-1],"jump_velocity")
			jump_velocity.text = str(objects.jump_velocity)

			jump_decelleration = ET.SubElement(obj[-1],"jump_decelleration")
			jump_decelleration.text = str(objects.jump_decelleration)

			mass = ET.SubElement(obj[-1],"mass")
			mass.text = str(objects.mass)


		tree = ET.ElementTree(root)
		tree.write("./WorldData/"+level_string+"/GameObjects.xml")

	def load_level(self,GameObjects,levelObjects,collisionList,level_string,screen,levelHandler):
		levelHandler.scroll_offset = 0
		levelHandler.clear_render_buffer =True
		screen.fill((0,0,0))
	

		self.load_level_objects(levelObjects,collisionList,level_string)
		self.load_game_objects(GameObjects,collisionList,level_string)

	def load_level_objects(self,levelObjects,collisionList,level_string):
		levelObjects.clear()
		collisionList.clear()
		print("loading level objects...")

		#clear levelObjects list
		#levelObjects = list()
		tree = ET.parse("./WorldData/" + level_string +"/levelObjects.xml")
		root = tree.getroot()

		for object_elem in root.findall("object"):
			levelObjects.append(GameObject._GameObject())
			levelObjects[-1].subClass = object_elem.find("subClass").text
			levelObjects[-1].imagePath = object_elem.find("imagePath").text
			x_position = float(object_elem.find("position_x").text)
			y_position = float(object_elem.find("position_y").text)
			levelObjects[-1].position[0] = x_position
			levelObjects[-1].position[1] = y_position
			levelObjects[-1].initial_position = copy.deepcopy(levelObjects[-1].position)
			levelObjects[-1]._set_image_path(levelObjects[-1]._get_image_path())
			levelObjects[-1]._set_image()		
			self.list_of_placed_objects.append(copy.deepcopy(levelObjects[-1].initial_position))
			levelObjects[-1]._set_sprite_size(levelObjects[-1].image)
			levelObjects[-1]._set_rect(levelObjects[-1].sprite_size)
			collisionList.append(levelObjects[-1])
		

	def load_game_objects(self,GameObjects,collisionList,level_string):
		GameObjects.clear()

		print("loading GameObjects...")
		GameObjects.clear()
		#clear levelObjects list
		#levelObjects = list()
		tree = ET.parse("./WorldData/"+level_string+"/GameObjects.xml")
		root = tree.getroot()

		for object_elem in root.findall("object"):
			GameObjects.append(GameObject._GameObject())
			GameObjects[-1].subClass = object_elem.find("subClass").text
			GameObjects[-1].imagePath = object_elem.find("imagePath").text
			x_position = float(object_elem.find("position_x").text)
			y_position = float(object_elem.find("position_y").text)
			GameObjects[-1].position[0] = x_position
			GameObjects[-1].position[1] = y_position
			GameObjects[-1].initial_position = copy.deepcopy(GameObjects[-1].position)
			GameObjects[-1]._set_image_path(GameObjects[-1]._get_image_path())
			GameObjects[-1]._set_image()		
			GameObjects[-1]._set_sprite_size(GameObjects[-1].image)
			GameObjects[-1]._set_rect(GameObjects[-1].sprite_size)

			GameObjects[-1].jump_velocity = float(object_elem.find("jump_velocity").text)
			GameObjects[-1].jump_decelleration = float(object_elem.find('jump_decelleration').text)
			GameObjects[-1].accelerationX = float(object_elem.find("accelerationX").text)
			GameObjects[-1].mass = float(object_elem.find("mass").text)

			collisionList.append(GameObjects[-1])
	
