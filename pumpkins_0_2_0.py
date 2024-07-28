def pumpkins_0_2_0():
	WIDTH = get_world_size()
	HEIGHT = WIDTH
	DEBUG = False
	TANK_CAPACITY = 0.25
	BUY_PUMPKINS_SEED_BATCH = 100
	EMPTY_TANK_WOOD_COST = 5

	def plant(x, y):
		water_if_needed()

		# TODO: add error check

		if num_items(Items.Pumpkin_Seed) == 0:
			trade(Items.Pumpkin_Seed, BUY_PUMPKINS_SEED_BATCH)
		plant(Entities.Pumpkin)

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

	def initialize_queue():
		queue = []

		for y in range(HEIGHT):
			for x in range(WIDTH):
				queue.append({'position': (x, y), 'action': 'plant'})

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

	def error():
		while True:
			do_a_flip()

	def run():
		queue = initialize_queue()

		while len(queue) > 0:
			task = queue.pop(0)
			move_to(task['position'][0], task['position'][1])
			action = task['action']

			if action == 'plant':
				check_ground_type()
				plant()
				queue.append({'position': task['position'], 'action': 'check'})
			elif action == 'check':
				if get_entity_type() == None:
					plant()
					queue.append({'position': task['position'], 'action': 'check'})
				elif get_entity_type() == Entities.Pumpkin:
					if not can_harvest():
						water_if_needed()
						queue.append({'position': task['position'], 'action': 'check'})
				else:
					error()

		harvest()
	
	run()

pumpkins_0_2_0()