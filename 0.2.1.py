# parameters
target_hay = 200
target_wood = 500
debug = False

# constants
WIDTH = get_world_size()
HEIGHT = WIDTH
TANK_CAPACITY = 0.25
MAX_GROUND_WATER = 1.0
EMPTY_TANK_WOOD_COST = 5

x = get_pos_x()
y = get_pos_y()

# TODO
# [ ] batch buy

while True:
	move(East)
	x = (x + 1) % WIDTH
	if x == 0:
		move(South)
		y = (y + 1) % HEIGHT
	quick_print(x, " ", y)
	
	check_ground_type()
	water_if_needed()
	
	if waiting_for_harvest():
		continue
		
	harvest()
	plant_next()
	

def plant_next():
	if num_items(Items.Hay) <= target_hay:
		plant(Entities.Grass)
	elif num_items(Items.Wood) <= target_wood:
		plant(Entities.Bush)
	else:
		if num_items(Items.Carrot_Seed) == 0:
			trade(Items.Carrot_Seed)
		plant(Entities.Carrots)

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
			