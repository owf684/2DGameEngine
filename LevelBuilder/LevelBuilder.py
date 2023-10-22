import pygame
import sys
sys.path.append('./GameObjects')
sys.path.append('./UIEngine')

import ItemContainer
import GameObject
import BlockObject
import PlayerObject
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
		self.scroll_offset_magnitude = 1
		self.scroll_offset_fudge = 0.5

		self.block_select_key = False
		self.selected_block_index = 0
		self.last_selected_index = 0

		# level editing save, load, and patch bools
		self.create_level_select = False
		self.load_level_select = False
		self.patch_level_select = False

		self.edit = False
		self.edit_latch = True
		self.category_selection_index = 0
		self.category_select_key = False
		self.spawn_point = (0,0)
		self.spawn_point_loaded = False

		self.ui_elements = list()

		'''
		Create and initialize levelBuilder sprites 
		0 = Basic Platform Blocks
		1 = Enemies
		2 = Environment 
		3 = Powerups
		4 = Items
		'''
		self.building_blocks = list()
		self.enemy_sprites = list()			# 1
		self.environment_sprites = list()	# 2
		self.power_up_sprites = list()		# 3
		self.item_sprites = list()			# 4
		self.initialize_all_sprites()		

		'''Add LevelBuilder sprites to category Container'''
		self.category_container = list()
		self.category_container.append(self.building_blocks)
		self.category_container.append(self.enemy_sprites)
		self.category_container.append(self.environment_sprites)
		self.category_container.append(self.power_up_sprites)
		self.category_container.append(self.item_sprites)

		self.initiliaze_builder_ui()

	def initiliaze_builder_ui(self):
		self.ui_elements.clear()
		y_position = 32
		self.limit_selection_index()
		x_position = (self.screen_width/2) - len(self.category_container[self.category_selection_index])*64/2
		for items in self.category_container[self.category_selection_index]:
			item_container = ItemContainer._ItemContainer()

			# set images
			item_container.set_active_image("./Assets/UI/ItemContainer_selected.png")
			item_container.set_inactive_image('./Assets/UI/ItemContainer.png')
			item_container.active_image = item_container.item_inactive_image
			
			# set position
			item_container.position = [x_position,y_position] 

			#get items image scaled dimensions
			x_scale_factor = items.image.get_width()/36
			y_scale_factor = items.image.get_height()/36

			if x_scale_factor > y_scale_factor:
				scale_factor = x_scale_factor
			else:
				scale_factor = y_scale_factor

			item_container.item_image = pygame.transform.scale(items.image, (items.image.get_width()/scale_factor, items.image.get_height()/scale_factor))
			item_container.item_image_path = items.imagePath
			item_container.item_position = [x_position + item_container.active_image.get_width()/4,y_position + item_container.active_image.get_height()/4]

			#increment x by adding size of width
			x_position += 64

			self.ui_elements.append(item_container)

	def initialize_all_sprites(self):

		self.initialize_sprites("./Assets/Items/*.png","BlockObject",'item',self.item_sprites)

		self.initialize_sprites("./Assets/Platforms/*.png",'BlockObject','platform',self.building_blocks)
	
		self.initialize_sprites("./Assets/EnemySprites/Goomba/*.png",'GameObject','enemy',self.enemy_sprites)
	
		self.initialize_sprites("./Assets/EnvironmentSprites/*.png", 'GameObject','environment',self.environment_sprites)

		self.initialize_sprites('./Assets/PowerUps/*.png', 'GameObject','powerup',self.power_up_sprites)
		
	def initialize_sprites(self,sprites_path, object_type, sub_class, sprite_list):
		png_list = glob.glob(sprites_path)
		print (png_list)
		for sprite_path in png_list:

			if object_type == 'GameObject':
				new_sprite = GameObject._GameObject()
			if object_type == 'BlockObject':
				new_sprite = BlockObject._BlockObject()
			new_sprite._set_sub_class(sub_class)
			new_sprite._set_image_path(sprite_path)
			new_sprite._set_image()
			new_sprite._set_sprite_size(new_sprite.image)
			new_sprite._set_rect(new_sprite.sprite_size)
			sprite_list.append(new_sprite)

	def main_loop(self,input_dict,screen,levelObjects,collisionList,levelHandler,PlayerEngine,GameObjects,GraphicsEngine):
		if input_dict['edit'] == '1' and not self.edit_latch:
			self.edit = not self.edit
			self.edit_latch = True
			levelHandler.clear_render_buffer = True
		if input_dict['edit'] == '0' and self.edit_latch:
			self.edit_latch = False

		if self.edit:
			self.poll_mouse(input_dict,screen,levelObjects,collisionList,levelHandler,GameObjects)
			self.handle_user_input(input_dict,levelObjects,collisionList,GameObjects,screen,levelHandler)
			self.ui(input_dict,screen,levelObjects,collisionList,levelHandler,GraphicsEngine)

	def poll_mouse(self,input_dict,screen,levelObjects,collisionList,levelHandler,GameObjects):

		#add block
		if input_dict['left-click'] == '1':

			self.mouse_position = pygame.mouse.get_pos()
			
			self.get_snap_values(input_dict,screen,levelObjects,levelHandler,GameObjects)

			if self.can_place_block:

				self.place_block(input_dict,screen,levelObjects,collisionList,levelHandler,GameObjects)
		#remove block
		if input_dict['right-click'] == '1':
			self.mouse_position = pygame.mouse.get_pos()
			for objects in GameObjects:
				if objects.subClass != 'player':
					if objects.rect.collidepoint(self.mouse_position):

						GameObjects.remove(objects)
						levelHandler.clear_render_buffer = True
						break
			for objects in levelObjects:
				if objects.subClass == 'platform' or objects.subClass == 'environment' or objects.subClass == 'item':
					if objects.rect.collidepoint(self.mouse_position):
						levelObjects.remove(objects)
						levelHandler.clear_render_buffer = True

	def get_snap_values(self,input_dict,screen,levelObjects,levelHandler,GameObjects):

		self.can_place_block = True
		#get x snap value
		if levelHandler.scroll_offset != 0:
			self.scroll_offset_magnitude = levelHandler.scroll_offset/levelHandler.scroll_offset
		else:
			self.scroll_offset_magnitude = 1
		self.snap_position[0] = int((self.mouse_position[0] - abs(levelHandler.scroll_delta))/self.grid_size)*self.grid_size + abs(levelHandler.scroll_delta)
		#get y snap value
		self.snap_position[1] = int(self.mouse_position[1]/self.grid_size)*self.grid_size
		#draw the placement sqaure
		square_rect = pygame.Rect(self.snap_position[0], self.snap_position[1], self.scan_block_size, self.scan_block_size)
		
		#check if block already exists
		for objects in GameObjects:
			if objects.rect.collidepoint(self.snap_position):
				self.can_place_block = False
		for objects in levelObjects:
			if objects.rect.collidepoint(self.snap_position) and self.category_selection_index != 3 and self.category_selection_index != 4:
				self.can_place_block = False

		pygame.draw.rect(screen, self.block_color, square_rect)
		#update the screen
		pygame.display.flip()

	def create_object(self, objectsList,objectType,selectedBlock,levelHandler,collisionList,direction):
			if objectType == 'GameObject':
				objectsList.append(GameObject._GameObject())
			elif objectType == 'BlockObject':
				objectsList.append(BlockObject._BlockObject())

			objectsList[-1]._set_sub_class(selectedBlock.subClass)
			objectsList[-1]._set_image_path(selectedBlock._get_image_path())
			objectsList[-1]._set_image()
			objectsList[-1]._set_mask()
			objectsList[-1].position = copy.deepcopy(self.snap_position)
			objectsList[-1].x_direction = direction
			objectsList[-1].initial_position = copy.deepcopy((self.snap_position[0]+levelHandler.scroll_offset,self.snap_position[1]))
			objectsList[-1]._set_sprite_size(objectsList[-1].image)
			objectsList[-1]._set_rect(objectsList[-1].sprite_size)
			collisionList.append(objectsList[-1])				

	def place_block(self,input_dict,screen,levelObjects,collisionList,levelHandler,GameObjects):
		selected_block = self.category_container[self.category_selection_index][self.selected_block_index]

		if selected_block._get_sub_class() == 'platform':
			self.create_object(levelObjects,'BlockObject',selected_block,levelHandler,collisionList,0)
	
		if selected_block._get_sub_class() == 'enemy':
			self.create_object(GameObjects,"GameObject",selected_block,levelHandler,collisionList,-1)
	
		if selected_block._get_sub_class() == 'environment':
			self.create_object(levelObjects,'GameObject',selected_block,levelHandler,collisionList,0)
		
		if selected_block._get_sub_class() == 'powerup':
			self.create_object(GameObjects, 'BlockObject',selected_block,levelHandler,collisionList,1)
			self.add_to_object(levelObjects,GameObjects,collisionList)
				
		if  selected_block._get_sub_class() == 'item':
			self.create_object(levelObjects,'BlockObject',selected_block,levelHandler,collisionList,0)
			self.add_to_object(levelObjects,levelObjects,collisionList)
			
	def add_to_object(self,levelObjects,objectsList,collisionList):
		for objects in levelObjects:
			if isinstance(objects,BlockObject._BlockObject):
				if objects.rect.collidepoint(self.snap_position):
					objects.item = objectsList[-1]
					objectsList.pop()
					collisionList.pop()


	def ui(self,input_dict,screen,levelObjects,collisionList,levelHandler,GraphicsEngine):
		self.limit_selection_index()
		selected_category = self.category_container[self.category_selection_index]
		for uie in self.ui_elements:
			if uie.item_image_path == selected_category[self.selected_block_index].imagePath:
				uie.isActive = True
			else:
				uie.isActive = False
			if uie.isActive:
				uie.active_image = uie.item_selected_image
			else:
				uie.active_image = uie.item_inactive_image

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
		if input_dict['arrow_hori'] == '1' and not self.category_select_key:
			self.category_select_key = True
			self.category_selection_index += 1
			self.initiliaze_builder_ui()
		elif input_dict['arrow_hori'] == '-1' and not self.category_select_key:
			self.category_select_key = True
			self.category_selection_index -= 1
			self.initiliaze_builder_ui()
		elif input_dict['arrow_hori'] == '0':
			self.category_select_key = False


		if self.block_select_key or self.category_select_key:
			levelHandler.clear_render_buffer = True

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
		if (input_dict["load-level"] == "1" and not self.load_level_select):
			self.load_level_select = True
			self.load_level(GameObjects,levelObjects,collisionList,"level_1",screen,levelHandler)
		elif input_dict["load-level"] == "0":
			self.load_level_select = False

	def limit_selection_index(self):
		if self.category_selection_index < 0:
			self.category_selection_index = 0
		elif self.category_selection_index >= len(self.category_container):
			self.category_selection_index = len(self.category_container) - 1

		if self.selected_block_index < 0:
			self.selected_block_index = 0

		elif self.selected_block_index >= len(self.category_container[self.category_selection_index]):
			self.selected_block_index = len(self.category_container[self.category_selection_index])-1	

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

			item_image_path = ET.SubElement(obj[-1],"itemImagePath")
			item_sub_class = ET.SubElement(obj[-1],"itemSubClass")
			item_position_x = ET.SubElement(obj[-1],"item_position_x")
			item_position_y = ET.SubElement(obj[-1],"item_position_y")

			if isinstance(objects, BlockObject._BlockObject):

				if objects.item is not None:
					item_image_path.text = objects.item.imagePath
					item_sub_class.text = objects.item.subClass
					item_position_x.text = str(objects.item.initial_position[0])
					item_position_y.text = str(objects.item.initial_position[1])
				else:
					item_image_path.text = 'None'
					item_sub_class.text  = 'None'
					item_position_x.text = 'None'
					item_position_y.text = 'None'
			else:
				item_image_path.text = 'None'
				item_sub_class.text = 'None'
				item_position_x.text = 'None'
				item_position_y.text = 'None'

		tree = ET.ElementTree(root)
		
		tree.write("./WorldData/"+level_string+"/levelObjects.xml" )
	def generate_item(self,object_elem):
		try:
			item = GameObject._GameObject()
			item.subClass = object_elem.find("itemSubClass").text
			item.imagePath = object_elem.find("itemImagePath").text
			x_position = float(object_elem.find("item_position_x").text)
			y_position = float(object_elem.find("item_position_y").text)
			item.position[0] = x_position
			item.position[1] = y_position
			item.initial_position = copy.deepcopy(item.position)
			item._set_image_path(item._get_image_path())
			item._set_image()
			item._set_sprite_size(item.image)
			item._set_rect(item.sprite_size)
			return item
		except:

			return None


	def save_game_objects(self,GameObjects,level_string):

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



		tree = ET.ElementTree(root)
		tree.write("./WorldData/"+level_string+"/GameObjects.xml")

	def load_level(self,GameObjects,levelObjects,collisionList,level_string,screen,levelHandler):
		self.spawn_point_loaded = False
		levelHandler.scroll_offset = 0
		levelHandler.clear_render_buffer =True
		screen.fill((0,0,0))
	

		self.load_level_objects(levelObjects,collisionList,level_string,levelHandler)
		self.load_game_objects(GameObjects,collisionList,level_string)

	def load_level_objects(self,levelObjects,collisionList,level_string,levelHandler):
		levelObjects.clear()
		collisionList.clear()
		levelHandler.question_blocks.clear()

		print("loading level objects...")

		tree = ET.parse("./WorldData/" + level_string +"/levelObjects.xml")
		root = tree.getroot()

		for object_elem in root.findall("object"):
			tmp_img_path = object_elem.find("imagePath")
			if  "Question" or "break" in tmp_img_path:
				levelObjects.append(BlockObject._BlockObject())
			else:
				levelObjects.append(GameObject._GameObject())

			levelObjects[-1].subClass = object_elem.find("subClass").text
			levelObjects[-1].imagePath = object_elem.find("imagePath").text
			x_position = float(object_elem.find("position_x").text)
			y_position = float(object_elem.find("position_y").text)
			levelObjects[-1].position[0] = x_position
			levelObjects[-1].position[1] = y_position
			levelObjects[-1].x_direction = 0
			levelObjects[-1].initial_position = copy.deepcopy(levelObjects[-1].position)
			levelObjects[-1]._set_image_path(levelObjects[-1]._get_image_path())
			levelObjects[-1]._set_image()		
			levelObjects[-1]._set_sprite_size(levelObjects[-1].image)
			levelObjects[-1]._set_rect(levelObjects[-1].sprite_size)
			levelObjects[-1]._set_mask()

			if object_elem.find('itemImagePath').text != 'None':
				levelObjects[-1].item = self.generate_item(object_elem)

			collisionList.append(levelObjects[-1])
			if levelObjects[-1].subClass == 'environment':
				if 'spawn_point' in levelObjects[-1].imagePath:
					self.spawn_point = copy.deepcopy(levelObjects[-1].initial_position)
					self.spawn_point_loaded = True
				elif not self.spawn_point_loaded:
					self.spawn_point = (0,0)

			if 'Question' in levelObjects[-1].imagePath:
				levelHandler.question_blocks.append(levelObjects[-1])

	def load_game_objects(self,GameObjects,collisionList,level_string):
		GameObjects.clear()

		print("loading GameObjects...")
		GameObjects.clear()
	
		tree = ET.parse("./WorldData/"+level_string+"/GameObjects.xml")
		root = tree.getroot()

		for object_elem in root.findall("object"):
			temp_subClass = object_elem.find("subClass").text
			if temp_subClass == 'player':

				GameObjects.append(PlayerObject._PlayerObject())
				
			else:
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
			GameObjects[-1]._set_mask()
			GameObjects[-1]._set_hit_box(GameObjects[-1].sprite_size,8)
			if GameObjects[-1].subClass == 'player':
				GameObjects[-1].initial_position = copy.deepcopy(self.spawn_point)
				GameObjects[-1].position = copy.deepcopy(self.spawn_point)
				GameObjects[-1]._set_kill_box(GameObjects[-1].sprite_size,32)
			collisionList.append(GameObjects[-1])
			if GameObjects[-1].subClass == 'enemy':
				GameObjects[-1].x_direction = -1


		
