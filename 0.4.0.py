# TODO
# [ ] keep track of harvestable pumpkins
# [ ] target moving w/ distance/time estimation
# [ ] task queue
# [x] water multiple times
# [x] batch buy
# [x] pumpkin mode


def run_0_4_1():
    # constants
    WIDTH = get_world_size()
    HEIGHT = WIDTH
    TANK_CAPACITY = 0.25
    MAX_GROUND_WATER = 1.0
    EMPTY_TANK_WOOD_COST = 5

	# parameters
	target_hay = 3500
	target_wood = 3500
	target_carrots = 10000
	grow_pumpkins = False
	debug = False
	limit_rows = 1

	def move_next(x, y, grow_pumpkins):
		move(East)
		x = (x + 1) % WIDTH
		if grow_pumpkins and x == 0:
			move(South)
			y = (y + 1) % HEIGHT
		
		return (x, y)

	def plant_next(x, y):
		water_if_needed()

		if odd_tile(x, y) and num_items(Items.Wood) <= target_wood:
			plant(Entities.Tree)
		elif num_items(Items.Hay) <= target_hay:
			plant(Entities.Grass)
		elif num_items(Items.Carrot) <= target_carrots:
			if num_items(Items.Carrot_Seed) == 0:
				trade(Items.Carrot_Seed)
			plant(Entities.Carrots)
		else:
			if num_items(Items.Pumpkin_Seed) == 0:
				trade(Items.Pumpkin_Seed)
			plant(Entities.Pumpkin)

	def odd_tile(current_x, current_y):
		return ((current_x % 2) + (current_y % 2)) == 1

	def waiting_for_harvest():
		return get_entity_type() and not can_harvest()

	def check_ground_type():
		if get_ground_type() != Grounds.Soil:
			till()
		
	def water_if_needed():
		water_level = get_water()
		
		if debug:
			quick_print(x, " ", y, " ", water_level)
		
		if water_level <= (MAX_GROUND_WATER - TANK_CAPACITY):
			if num_items(Items.Water_Tank) > 0:
				use_item(Items.Water_Tank)
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
				water_if_needed()
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

run_0_4_0()