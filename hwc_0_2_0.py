def hay_wood_carrots_0_2_0():
	WIDTH = get_world_size()
	HEIGHT = WIDTH
	DEBUG = False
	TANK_CAPACITY = 0.25
	EMPTY_TANK_WOOD_COST = 5
	DEFAULT_PLANT = Entities.Grass
	BUY_CARROT_SEEDS_BATCH = 100

	def check_ground_type():
		if get_ground_type() != Grounds.Soil:
			till()
		
	def water_if_needed():
		water_level = get_water()
		num_times = (1.0 - water_level) // TANK_CAPACITY

		if num_times == 0:
			return
		
		if num_items(Items.Water_Tank) > num_times:
			for i in range(num_times):
				use_item(Items.Water_Tank)
			if DEBUG:
				quick_print(x, " ", y, " ", num_times, " ", water_level)
		else:
			if num_items(Items.Wood) >= EMPTY_TANK_WOOD_COST:
				trade(Items.Empty_Tank)

	def move_to_x(target):
		current = get_pos_x()

		if target > current:
			west_distance = current + WIDTH - target
			east_distance = target - current
		elif target < current:
			west_distance = current - target
			east_distance = WIDTH - current + target
		else:
			return

		if west_distance > east_distance:
			for _ in range(east_distance):
				move(East)
		else:
			for _ in range(west_distance):
				move(West)

		# origin is south west corner
	def move_to_y(target):
		current = get_pos_y()
		if target > current:
			north_distance = target - current
			south_distance = current + HEIGHT - target
		elif target < current:
			north_distance = HEIGHT - current + target
			south_distance = current - target
		else:
			return
	
		if north_distance > south_distance:
			for _ in range(south_distance):
				move(South)
		else:
			for _ in range(north_distance):
				move(North)

	def move_to(target_x, target_y):
		move_to_x(target_x)
		move_to_y(target_y)

	def initialize_array():
		array = []
		for _ in range(HEIGHT):
			row = []
			for _ in range(WIDTH):
				row.append(False)
			array.append(row)
		return array

	def plant_entity(entity):
		check_ground_type()
		water_if_needed()
		if num_items(Items.Carrot_Seed) == 0:
			trade(Items.Carrot_Seed, BUY_CARROT_SEEDS_BATCH)
		plant(entity)

	def plant_cycles():
		queue = [{'position': (4, 4), 'action': 'plant', 'entity': DEFAULT_PLANT}]
		planted = initialize_array()
		cycle_complete = False

		while len(queue) > 0:
			task = queue.pop(0)
			action = task['action']
			position = task['position']
			x = position[0]
			y = position[1]

			move_to(x, y)

			if task['action'] == 'plant':
				plant_entity(task['entity'])
				planted[y][x] = True
				companion = get_companion()
				if not planted[companion[2]][companion[1]]:
					queue.insert(0, {'position': (companion[1], companion[2]), 'action': 'plant', 'entity': companion[0]})
				# else:
				# 	quick_print("cycle complete ", companion[2], " ", companion[2])
				queue.append({'position': task['position'], 'action': 'harvest', 'entity': task['entity']})
			elif task['action'] == 'harvest':
				while not can_harvest():
					water_if_needed()

				harvest()
				# quick_print("harvested ", x, " ", y)
				planted[y][x] = False
			
			if len(queue) == 0:
				queue = [{'position': (x, y), 'action': 'plant', 'entity': DEFAULT_PLANT}]

	clear()
	plant_cycles()

hay_wood_carrots_0_2_0()