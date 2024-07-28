
# TODO
# [ ] keep track of harvestable pumpkins
# [ ] target moving w/ distance/time estimation
# [ ] task queue
# [x] water multiple times
# [x] batch buy
# [x] pumpkin mode

def run_0_3_1():
	# constants
	WIDTH = get_world_size()
	HEIGHT = WIDTH
	TANK_CAPACITY = 0.25
	MAX_GROUND_WATER = 1.0
	EMPTY_TANK_WOOD_COST = 5
	DEBUG = False

	# parameters
	target_hay = 50000
	target_wood = 20000
	target_carrots = 20000
	buy_carrot_seeds_batch = 100

	grow_pumpkins = False
	buy_pumpkin_seeds_batch = 100

	def move_next(x, y, grow_pumpkins):
		move(East)
		x = (x + 1) % WIDTH
		if grow_pumpkins and x == 0:
			move(South)
			y = (y + 1) % HEIGHT
		
		return (x, y)

	def plant_next(x, y):
		water_if_needed(x, y)

		if num_items(Items.Wood) <= target_wood and odd_tile(x, y):
			plant(Entities.Tree)
		elif num_items(Items.Hay) <= target_hay:
			plant(Entities.Grass)
		elif num_items(Items.Carrot) <= target_carrots:
			if num_items(Items.Carrot_Seed) == 0:
				trade(Items.Carrot_Seed, buy_carrot_seeds_batch)
			plant(Entities.Carrots)
		else:
			if num_items(Items.Pumpkin_Seed) == 0:
				trade(Items.Pumpkin_Seed, buy_pumpkin_seeds_batch)
			plant(Entities.Pumpkin)

	def odd_tile(current_x, current_y):
		return ((current_x % 2) + (current_y % 2)) == 1

	def waiting_for_harvest():
		return get_entity_type() and not can_harvest()

	def check_ground_type():
		if get_ground_type() != Grounds.Soil:
			till()
		
	def water_if_needed(x, y):
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


	def run():
		x = get_pos_x()
		y = get_pos_y()
		ready_pumpkins = 0

		while True:
			x, y = move_next(x, y, grow_pumpkins)
			
			check_ground_type()
			entity = get_entity_type()
			harvestable = can_harvest()
			
			if not entity:
				plant_next(x, y)
				continue
			
			if not harvestable:
				water_if_needed(x, y)
				continue

			if grow_pumpkins and entity == Entities.Pumpkin:
				ready_pumpkins = ready_pumpkins + 1
				if ready_pumpkins == WIDTH * HEIGHT:
					harvest()
					plant_next(x, y)
			else:
				harvest()
				plant_next(x, y)
				
			if x == 0 and y == 0:
				ready_pumpkins = 0
	
	run()

run_0_3_1()