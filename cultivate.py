def water_if_needed():
	water_level = get_water()
	num_times = (1.0 - water_level) // TANK_CAPACITY

	if num_times == 0:
		return
	
	if num_items(Items.Water_Tank) > num_times:
		for i in range(num_times):
			use_item(Items.Water_Tank)
	else:
		if num_items(Items.Wood) >= EMPTY_TANK_WOOD_COST:
			trade(Items.Empty_Tank)

def cultivate(entity):
	TANK_CAPACITY = 0.25
	EMPTY_TANK_WOOD_COST = get_cost(Items.Empty_Tank)[Items.Wood]
	BUY_CARROT_SEEDS_BATCH = 100

	def check_ground_type():
		if get_ground_type() != Grounds.Soil:
			till()


	# TODO: move to initialization?
	check_ground_type()
	water_if_needed()

	if entity == Entities.Carrots and num_items(Items.Carrot_Seed) == 0:
		trade(Items.Carrot_Seed, BUY_CARROT_SEEDS_BATCH)

	plant(entity)