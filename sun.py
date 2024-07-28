def sunflowers_0_1_0():
	WIDTH = get_world_size()
	HEIGHT = WIDTH
	DEBUG = False
	TANK_CAPACITY = 0.25
	BUY_SUNFLOWER_SEEDS_BATCH = 100

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
			if num_items(Items.Wood) >= get_cost(Items.Empty_Tank):
				trade(Items.Empty_Tank)

	def plant_sunflower():
		check_ground_type()
		water_if_needed()
		if num_items(Items.Sunflower_Seed) == 0:
			trade(Items.Sunflower_Seed, BUY_SUNFLOWER_SEEDS_BATCH)
		plant(Entities.Sunflower)
		return measure()

	def move_next():
		move(East)
		if get_pos_x() == 0:
			move(North)

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

	def run():
		max_petals = 0
		max_x = None
		max_y = None

		while True:
			current_petals = plant_sunflower()
			if current_petals > max_petals:
				max_petals = current_petals
				max_x = get_pos_x()
				max_y = get_pos_y()
			move_next()
			if get_pos_x() == 0 and get_pos_y() == 0:
				break
		
		move_to(max_x, max_y)
		harvest()

	run()

sunflowers_0_1_0()