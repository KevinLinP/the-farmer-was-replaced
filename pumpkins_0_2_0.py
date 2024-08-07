def pumpkins_0_2_0():
	WIDTH = get_world_size()
	HEIGHT = WIDTH
	DEBUG = False
	TANK_CAPACITY = 0.25
	BUY_PUMPKINS_SEED_BATCH = 100
	EMPTY_TANK_WOOD_COST = 5

	def plant_pumpkin():
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

		return queue

	def error():
		while True:
			do_a_flip()

	def plant_and_harvest_field():
		queue = initialize_queue()

		while len(queue) > 0:
			task = queue.pop(0)
			move_to(task['position'][0], task['position'][1])
			action = task['action']

			if action == 'plant':
				check_ground_type()
				plant_pumpkin()
				queue.append({'position': task['position'], 'action': 'check'})
			elif action == 'check':
				if get_entity_type() == None:
					plant_pumpkin()
					queue.append({'position': task['position'], 'action': 'check'})
				elif get_entity_type() == Entities.Pumpkin:
					if not can_harvest():
						water_if_needed()
						queue.append({'position': task['position'], 'action': 'check'})
				else:
					error()

		harvest()
	
	clear()
	while True:
		plant_and_harvest_field()

pumpkins_0_2_0()