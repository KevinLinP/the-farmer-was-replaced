# parameters
desired_water_level = 1.0
target_hay = 0
target_wood = 500

# constants
TANK_CAPACITY = 0.25
EMPTY_TANK_WOOD_COST = 5

while True:
	move(North)
	
	if get_ground_type() != Grounds.Soil:
		till()
	
	if get_entity_type() and not can_harvest():
		continue
		
	harvest()
		
	if get_water() <= (desired_water_level - TANK_CAPACITY):
		if num_items(Items.Water_Tank) > 0:
			use_item(Items.Water_Tank)
		else:
			if num_items(Items.Wood) >= EMPTY_TANK_WOOD_COST:
				trade(Items.Empty_Tank)
	
	if num_items(Items.Hay) <= target_hay:
		plant(Entities.Grass)
	elif num_items(Items.Wood) <= target_wood:
		plant(Entities.Bush)
	else:
		if num_items(Items.Carrot_Seed) == 0:
			trade(Items.Carrot_Seed)
		plant(Entities.Carrots)
			