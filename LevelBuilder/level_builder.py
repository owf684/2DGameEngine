import pygame
import sys
sys.path.append('./GameObjects')
sys.path.append('./UIEngine')

import item_container
import game_object
import block_object
import player_object
import copy
import glob
import os
import xml.etree.ElementTree as ET

class LevelBuilder:


	def __init__(self):
		# basic variables 
		self.mouse_position = [0,0]
		self.scan_block_size = 32
		self.screen_width = 1280
		self.screen_height = 720
		self.block_color = (255,255,255)
		self.grid_size = 32
		self.placement_coords = [0,0]
		self.snap_position = [0,0]
		self.scroll_offset_magnitude = 1
		self.spawn_point = [0,0]

		# Level Builder Flags
		self.reset_animations = False 
		self.block_select_key = False
		self.can_place_block = True
		self.create_level_select = False
		self.load_level_select = False
		self.patch_level_select = False
		self.edit = False
		self.edit_latch = True
		self.category_select_key = False

		# ui variables 
		self.level_save_ui = list()
		self.initialize_level_save_ui()
		self.level_save_button_state = 0 # 1 = yes 2 = no
		self.save_state = ''	
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
		self.selected_block_index = 0 
		self.last_selected_index = 0
		self.category_selection_index = 0 

		self.category_container = list()
		self.category_container.append(self.building_blocks)
		self.category_container.append(self.enemy_sprites)
		self.category_container.append(self.environment_sprites)
		self.category_container.append(self.power_up_sprites)
		self.category_container.append(self.item_sprites)

		self.initiliaze_builder_ui()

	def initialize_level_save_ui(self):
		level_save_ui_elements = glob.glob("./Assets/UI/level_save_ui/*.png")
		for uie in level_save_ui_elements:
			o_item_container = item_container.ItemContainer()
			o_item_container.set_active_image(uie)
			o_item_container.set_inactive_image(uie)
			o_item_container.active_image = o_item_container.item_inactive_image
			self.level_save_ui.append(o_item_container)
				
	def initiliaze_builder_ui(self):
		self.ui_elements.clear()
		y_position = 32
		self.limit_selection_index()
		x_position = (self.screen_width/2) - len(self.category_container[self.category_selection_index])*64/2
		for items in self.category_container[self.category_selection_index]:
			o_item_container = item_container.ItemContainer()

			# set images
			o_item_container.set_active_image("./Assets/UI/ItemContainer_selected.png")
			o_item_container.set_inactive_image('./Assets/UI/ItemContainer.png')
			o_item_container.active_image = o_item_container.item_inactive_image
			
			# set position
			o_item_container.position = [x_position,y_position] 

			#get items image scaled dimensions
			x_scale_factor = items.image.get_width()/36
			y_scale_factor = items.image.get_height()/36

			if x_scale_factor > y_scale_factor:
				scale_factor = x_scale_factor
			else:
				scale_factor = y_scale_factor

			o_item_container.item_image = pygame.transform.scale(items.image, (items.image.get_width()/scale_factor, items.image.get_height()/scale_factor))
			o_item_container.item_image_path = items.imagePath
			o_item_container.item_position = [x_position + o_item_container.active_image.get_width()/4,y_position + o_item_container.active_image.get_height()/4]

			#increment x by adding size of width
			x_position += 64
			o_item_container.set_rect()

			self.ui_elements.append(o_item_container)

	def initialize_all_sprites(self):

		self.initialize_sprites("./Assets/Items/*.png","BlockObject",'item',self.item_sprites)

		self.initialize_sprites("./Assets/Platforms/*.png",'BlockObject','platform',self.building_blocks)
	
		self.initialize_sprites("./Assets/EnemySprites/Goomba/*.png",'GameObject','enemy',self.enemy_sprites)
	
		self.initialize_sprites("./Assets/EnemySprites/KoopaTroopa/*.png",'GameObject','enemy',self.enemy_sprites)

		self.initialize_sprites("./Assets/EnvironmentSprites/*.png", 'GameObject','environment',self.environment_sprites)

		self.initialize_sprites('./Assets/PowerUps/*.png', 'GameObject','powerup',self.power_up_sprites)
		
	def initialize_sprites(self,sprites_path, object_type, sub_class, sprite_list):
		png_list = glob.glob(sprites_path)
		print (png_list)
		for sprite_path in png_list:

			if object_type == 'GameObject':
				new_sprite = game_object.GameObject()
			if object_type == 'BlockObject':
				new_sprite = block_object.BlockObject()
			new_sprite._set_sub_class(sub_class)
			new_sprite._set_image_path(sprite_path)
			new_sprite._set_image()
			new_sprite._set_sprite_size(new_sprite.image)
			new_sprite._set_rect(new_sprite.sprite_size)
			sprite_list.append(new_sprite)

	def main_loop(self,d_inputs,screen,l_level_objects,l_collision_objects,o_level_handler,o_player_engine,l_game_objects,o_graphics_engine):
		if d_inputs['edit'] == '1' and not self.edit_latch and not o_level_handler.trigger_death_animation and not self.level_save_button_state == -1:
			if self.edit:
				self.patch_level(l_level_objects,l_game_objects)
			if not self.edit:
				self.load_after_edit(l_game_objects,l_level_objects,l_collision_objects,'level_1',screen,o_level_handler)
			self.edit = not self.edit
			self.edit_latch = True
			o_level_handler.clear_render_buffer = True
		if d_inputs['edit'] == '0' and self.edit_latch:
			self.edit_latch = False

		if self.edit:
			self.poll_mouse(d_inputs,screen,l_level_objects,l_collision_objects,o_level_handler,l_game_objects)
			self.handle_user_input(d_inputs,l_level_objects,l_collision_objects,l_game_objects,screen,o_level_handler)
			self.ui(d_inputs,screen,l_level_objects,l_collision_objects,o_level_handler,o_graphics_engine)
			self.handle_ui(d_inputs,l_level_objects,l_collision_objects,l_game_objects,screen,o_level_handler)

	def poll_mouse(self,d_inputs,screen,l_level_objects,l_collision_objects,o_level_handler,l_game_objects):

		#add block
		if d_inputs['left-click'] == '1':

			self.mouse_position = pygame.mouse.get_pos()
			
			self.get_snap_values(d_inputs,screen,l_level_objects,o_level_handler,l_game_objects)

			if self.can_place_block:

				self.place_block(d_inputs,screen,l_level_objects,l_collision_objects,o_level_handler,l_game_objects)
		#remove block
		if d_inputs['right-click'] == '1':
			self.mouse_position = pygame.mouse.get_pos()
			for objects in l_game_objects:
				if objects.subClass != 'player':
					if objects.rect.collidepoint(self.mouse_position):

						l_game_objects.remove(objects)
						o_level_handler.clear_render_buffer = True
						break
			for objects in l_level_objects:
				if objects.subClass == 'platform' or objects.subClass == 'environment' or objects.subClass == 'item':
					if objects.rect.collidepoint(self.mouse_position):
						l_level_objects.remove(objects)
						o_level_handler.clear_render_buffer = True

	def get_snap_values(self,d_inputs,screen,l_level_objects,o_level_handler,l_game_objects):

		self.can_place_block = True
		#get x snap value
		if o_level_handler.scroll_offset != 0:
			self.scroll_offset_magnitude = o_level_handler.scroll_offset/o_level_handler.scroll_offset
		else:
			self.scroll_offset_magnitude = 1
		self.snap_position[0] = int((self.mouse_position[0] - abs(o_level_handler.scroll_delta))/self.grid_size)*self.grid_size + abs(o_level_handler.scroll_delta)
		#get y snap value
		self.snap_position[1] = int(self.mouse_position[1]/self.grid_size)*self.grid_size
		#draw the placement sqaure
		square_rect = pygame.Rect(self.snap_position[0], self.snap_position[1], self.scan_block_size, self.scan_block_size)
		
		#check if block already exists
		for objects in l_game_objects:
			if objects.rect.collidepoint(self.snap_position):
				self.can_place_block = False
		for objects in l_level_objects:
			if objects.rect.collidepoint(self.snap_position) and self.category_selection_index != 3 and self.category_selection_index != 4:
				self.can_place_block = False
		for objects in self.ui_elements:
			if objects.rect.collidepoint(self.snap_position):
				self.can_place_block = False
				if 'no' in objects.selected_image_path:
					self.level_save_button_state = 2
				elif 'yes' in objects.selected_image_path:
					self.level_save_button_state = 1

		pygame.draw.rect(screen, self.block_color, square_rect)
		#update the screen
		pygame.display.flip()

	def create_object(self, l_objects,object_type,s_selected_block,o_level_handler,l_collision_objects,i_direction):
			if object_type == 'GameObject':
				l_objects.append(game_object.GameObject())
			elif object_type == 'BlockObject':
				l_objects.append(block_object.BlockObject())

			l_objects[-1]._set_sub_class(s_selected_block.subClass)
			l_objects[-1]._set_image_path(s_selected_block._get_image_path())
			l_objects[-1]._set_image()
			l_objects[-1]._set_mask()
			l_objects[-1].position = copy.deepcopy(self.snap_position)
			l_objects[-1].x_direction = i_direction
			l_objects[-1].initial_position = copy.deepcopy((self.snap_position[0]+o_level_handler.scroll_offset,self.snap_position[1]))
			l_objects[-1]._set_sprite_size(l_objects[-1].image)
			l_objects[-1]._set_rect(l_objects[-1].sprite_size)
			l_collision_objects.append(l_objects[-1])				

	def place_block(self,d_inputs,screen,l_level_objects,l_collision_objects,o_level_handler,l_game_objects):
		selected_block = self.category_container[self.category_selection_index][self.selected_block_index]

		if selected_block._get_sub_class() == 'platform':
			self.create_object(l_level_objects,'BlockObject',selected_block,o_level_handler,l_collision_objects,0)
	
		if selected_block._get_sub_class() == 'enemy':
			self.create_object(l_game_objects,"GameObject",selected_block,o_level_handler,l_collision_objects,-1)
	
		if selected_block._get_sub_class() == 'environment':
			self.create_object(l_level_objects,'GameObject',selected_block,o_level_handler,l_collision_objects,0)
		
		if selected_block._get_sub_class() == 'powerup':
			self.create_object(l_game_objects, 'BlockObject',selected_block,o_level_handler,l_collision_objects,1)
			self.add_to_object(l_level_objects,l_game_objects,l_collision_objects)
				
		if  selected_block._get_sub_class() == 'item':
			self.create_object(l_level_objects,'BlockObject',selected_block,o_level_handler,l_collision_objects,0)
			self.add_to_object(l_level_objects,l_level_objects,l_collision_objects)
			
	def add_to_object(self,l_level_objects,l_objects,l_collision_objects):
		for objects in l_level_objects:
			if isinstance(objects,block_object.BlockObject):
				if objects.rect.collidepoint(self.snap_position):
					objects.item = l_objects[-1]
					l_objects.pop()
					l_collision_objects.pop()

	def ui(self,d_inputs,screen,l_level_objects,l_collision_objects,o_level_handler,o_graphics_engine):
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
	def handle_ui(self,d_inputs,l_level_objects,l_collision_objects,l_game_objects,screen,o_level_handler):
		if self.level_save_button_state == 1: # poll for user input
			if self.save_state == 'create':
				self.save_level(l_level_objects,l_game_objects)
				self.save_state = ''
				self.level_save_button_state = 0
				self.initiliaze_builder_ui()

			elif self.save_state == 'patch':
				self.patch_level(l_level_objects,l_game_objects)	
				self.save_state = ''
				self.level_save_button_state = 0
				self.initiliaze_builder_ui()
			elif self.save_state == 'reload':
				self.load_level(l_game_objects,l_level_objects,l_collision_objects,"level_1",screen,o_level_handler)
				self.save_state = ''
				self.level_save_button_state = 0
				self.initiliaze_builder_ui()
		elif self.level_save_button_state == 2:
			self.level_save_button_state = 0
			self.initiliaze_builder_ui()

	def handle_user_input(self,d_inputs,l_level_objects,l_collision_objects,l_game_objects,screen,o_level_handler):

		#handles block selection 
		if d_inputs["arrow_vert"] == "1" and not self.block_select_key:
			self.block_select_key = True
			self.selected_block_index += 1
		elif d_inputs["arrow_vert"] == "-1" and not self.block_select_key:
			self.block_select_key = True
			self.selected_block_index -= 1
		elif d_inputs["arrow_vert"] == "0":
			self.block_select_key = False

		#write category selection here
		if d_inputs['arrow_hori'] == '1' and not self.category_select_key:
			self.category_select_key = True
			self.category_selection_index += 1
			self.initiliaze_builder_ui()
		elif d_inputs['arrow_hori'] == '-1' and not self.category_select_key:
			self.category_select_key = True
			self.category_selection_index -= 1
			self.initiliaze_builder_ui()
		elif d_inputs['arrow_hori'] == '0':
			self.category_select_key = False

		if self.block_select_key or self.category_select_key:
			o_level_handler.clear_render_buffer = True

		#handles save data
		if d_inputs["create-level"] == "1" and not self.create_level_select and self.level_save_button_state == 0:
			self.create_level_select = True
			self.level_save_button_state = -1
			self.load_level_save_ui("create")
		
		elif d_inputs["create-level"] == "0":
			self.create_level_select = False

		if d_inputs["patch-level"] == "1" and not self.patch_level_select and self.level_save_button_state == 0:
			
			self.patch_level_select = True
			self.level_save_button_state = -1
			self.load_level_save_ui("patch")

		elif d_inputs["patch-level"] == "0":
			
			self.patch_level_select = False
		
		#handle load data
		if (d_inputs["load-level"] == "1" and not self.load_level_select) and self.level_save_button_state == 0:
			self.load_level_select = True
			self.level_save_button_state = -1
			self.load_level_save_ui("reload")

			#self.load_level(GameObjects,levelObjects,collisionList,"level_1",screen,levelHandler)
		elif d_inputs["load-level"] == "0":
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

	def patch_level(self,l_level_objects,o_game_objects):
		selected_level = 1
		level_string = "level_" + str(selected_level)
		self.save_level_objects(l_level_objects,level_string)
		self.save_game_objects(o_game_objects,level_string)

	def save_level(self,l_level_objects,l_game_objects):
		new_level = len(glob.glob("./WorldData/level*")) + 1
		level_string = "level_" + str(new_level)
		os.mkdir("./WorldData/" + level_string)

		self.save_level_objects(l_level_objects,level_string)
		self.save_game_objects(l_game_objects,level_string)

	def save_level_objects(self,l_level_objects,level_string):

		#get level number
		root = ET.Element("objects")
		obj = list()
		for objects in l_level_objects:
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

			if isinstance(objects, block_object.BlockObject):

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

	def generate_item(self,object_elem, o_level_handler):
		try:
			item = game_object.GameObject()
			item.subClass = object_elem.find("itemSubClass").text
			item.imagePath = object_elem.find("itemImagePath").text
			x_position = float(object_elem.find("item_position_x").text)
			y_position = float(object_elem.find("item_position_y").text)
			item.position[0] = x_position - o_level_handler.scroll_offset 
			item.position[1] = y_position
			item.initial_position = copy.deepcopy([x_position,y_position])
			
			item._set_image_path(item._get_image_path())
			item._set_image()
			item._set_sprite_size(item.image)
			item._set_rect(item.sprite_size)
			return item
		except:

			return None

	def save_game_objects(self,l_game_objects,level_string):

		root = ET.Element("objects")
		obj = list()
		for objects in l_game_objects:
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

	def load_after_edit(self, l_game_objects,l_level_objects,l_collision_objects,level_string,screen,o_level_handler):
		o_level_handler.clear_render_buffer = True
		screen.fill((0,0,0))
		player_position = self.spawn_point
		for objects in l_game_objects:
			if objects.subClass == 'player':
				player_position = copy.deepcopy(objects.position)
		self.load_level_objects(l_level_objects,l_collision_objects,level_string,o_level_handler)
		self.load_game_objects(l_game_objects,l_collision_objects,level_string,o_level_handler)

		for objects in l_game_objects:
			if objects.subClass == 'player':
				objects.position = player_position

	def load_level(self,l_game_objects,l_level_objects,l_collision_objects,level_string,screen,o_level_handler):
		self.spawn_point_loaded = False
		o_level_handler.scroll_offset = 0
		o_level_handler.clear_render_buffer =True
		screen.fill((0,0,0))
		self.load_level_objects(l_level_objects,l_collision_objects,level_string,o_level_handler)
		self.load_game_objects(l_game_objects,l_collision_objects,level_string,o_level_handler)
		self.load_player_spawn_point(l_level_objects,l_game_objects)

	def create_loaded_objects(self,l_objects,object_elem, o_level_handler):
		l_objects[-1].subClass = object_elem.find("subClass").text
		l_objects[-1].imagePath = object_elem.find("imagePath").text
		x_position = float(object_elem.find("position_x").text)
		y_position = float(object_elem.find("position_y").text)
		l_objects[-1].position[0] = x_position
		l_objects[-1].position[1] = y_position
		l_objects[-1].x_direction = 0
		l_objects[-1].initial_position = copy.deepcopy(l_objects[-1].position) # always save the inisital position for offsetting the x coordinate
		l_objects[-1].position[0] = x_position - o_level_handler.scroll_offset

		l_objects[-1]._set_image_path(l_objects[-1]._get_image_path())
		l_objects[-1]._set_image()		
		l_objects[-1]._set_sprite_size(l_objects[-1].image)
		l_objects[-1]._set_rect(l_objects[-1].sprite_size)
		l_objects[-1]._set_mask()	

	def load_player_spawn_point(self,l_level_objects,l_game_objects):
		spawn_point_exists = False
		spawn_point_object = None
		for objects in l_level_objects:
			if objects.subClass == 'environment':
				if 'spawn_point' in objects.imagePath:
					spawn_point_exists = True
					spawn_point_object = objects				
		if spawn_point_exists:
			self.spawn_point = copy.deepcopy(spawn_point_object.initial_position)
		else:
			self.spawn_point = [0,0]

		for objects in l_game_objects:
			if objects.subClass == 'player':
				objects.initial_position = copy.deepcopy(self.spawn_point)
				objects.position = copy.deepcopy(self.spawn_point)

	def load_level_objects(self,l_level_objects,l_collision_objects,level_string,o_level_handler):
		l_level_objects.clear()
		l_collision_objects.clear()
		o_level_handler.question_blocks.clear()
		tree = ET.parse("./WorldData/" + level_string +"/levelObjects.xml")
		root = tree.getroot()

		for object_elem in root.findall("object"):
			if  "Question" or "break" in object_elem.find("imagePath"):
				l_level_objects.append(block_object.BlockObject())
			else:
				l_level_objects.append(game_object.GameObject())
			self.create_loaded_objects(l_level_objects,object_elem,o_level_handler)
	
			if object_elem.find('itemImagePath').text != 'None':
				l_level_objects[-1].item = self.generate_item(object_elem, o_level_handler)

			l_collision_objects.append(l_level_objects[-1])
			
			if 'Question' in l_level_objects[-1].imagePath:
				o_level_handler.question_blocks.append(l_level_objects[-1])

	def load_game_objects(self,l_game_objects,l_collision_objects,level_string, o_level_handler):
		l_game_objects.clear()
		l_game_objects.clear()	
		tree = ET.parse("./WorldData/"+level_string+"/GameObjects.xml")
		root = tree.getroot()

		for object_elem in root.findall("object"):
			temp_subClass = object_elem.find("subClass").text
			if temp_subClass == 'player':
				l_game_objects.append(player_object.PlayerObject())			
			else:
				l_game_objects.append(game_object.GameObject())		
			self.create_loaded_objects(l_game_objects,object_elem, o_level_handler)
			l_game_objects[-1]._set_hit_box(l_game_objects[-1].sprite_size,8)

			if l_game_objects[-1].subClass == 'player':
				l_game_objects[-1]._set_kill_box(l_game_objects[-1].sprite_size,32)
			l_collision_objects.append(l_game_objects[-1])
			if l_game_objects[-1].subClass == 'enemy':
				l_game_objects[-1].x_direction = -1

	def load_level_save_ui(self,message):
		self.save_state = message
		for uie in self.level_save_ui:
			if 'menu' in uie.selected_image_path:
				uie.position[0] = self.screen_width/2 - uie.item_selected_image.get_width()/2
				uie.position[1] = self.screen_height/2 -uie.item_selected_image.get_height()/2
				uie.set_rect()
				self.ui_elements.append(uie)

			if message in uie.selected_image_path:
				uie.position[0] = self.screen_width/2 - uie.item_selected_image.get_width()/2 
				uie.position[1] = self.screen_height/2 - uie.item_selected_image.get_height()/2 - 64
				uie.set_rect()
				self.ui_elements.append(uie)

			if 'yes' in uie.selected_image_path:
				uie.position[0] = self.screen_width/2 - uie.item_selected_image.get_width()/2 - 64
				uie.position[1] = self.screen_height/2 - uie.item_selected_image.get_height()/2 + 64
				uie.set_rect()
				self.ui_elements.append(uie)

			if 'no' in uie.selected_image_path:
				uie.position[0] = self.screen_width/2 - uie.item_selected_image.get_width()/2 + 64
				uie.position[1] = self.screen_height/2 - uie.item_selected_image.get_height()/2 + 64
				uie.set_rect()
				self.ui_elements.append(uie)
		
