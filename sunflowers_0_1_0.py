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

	def initialize_context():
		return {
			'num_petals': [],
			'sunflower_positions_by_num_petals': {}
		}

	def insert_reverse_sorted_list(list, num):
		for i in range(len(list)):
			if list[i] < num:
				list.insert(i, num)
				return
		list.append(num)

	def track_sunflower(context, num_petals):
		if num_petals in context['sunflower_positions_by_num_petals']:
			positions = context['sunflower_positions_by_num_petals'][num_petals]
			if len(positions) == 0:
				insert_reverse_sorted_list(context['num_petals'], num_petals)
			positions.append((get_pos_x(), get_pos_y()))
		else:
			insert_reverse_sorted_list(context['num_petals'], num_petals)
			context['sunflower_positions_by_num_petals'][num_petals] = [(get_pos_x(), get_pos_y())]

	def pop_largest_sunflower(context):
		num_petals = context['num_petals'][0]
		positions = context['sunflower_positions_by_num_petals'][num_petals]
		position = positions.pop(0)
		if len(positions) == 0:
			context['num_petals'].pop(0)
		return position

	def run():
		context = initialize_context()

		while True:
			num_petals = plant_sunflower()
			track_sunflower(context, num_petals)
			move_next()
			if get_pos_x() == 0 and get_pos_y() == 0:
				break

		while len(context['num_petals']) > 0:
			position = pop_largest_sunflower(context)
			move_to(position[0], position[1])
			while not can_harvest():
				water_if_needed()
			harvest()
			# num_petals = plant_sunflower()
			# track_sunflower(context, num_petals)

	clear()
	while True:
		run()
		move_to(0, 0)

sunflowers_0_1_0()