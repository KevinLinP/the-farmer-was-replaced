def check_ground_type():
	if get_ground_type() != Grounds.Soil:
		till()

def water_if_needed():
	TANK_CAPACITY = 0.25
	EMPTY_TANK_WOOD_COST = get_cost(Items.Empty_Tank)[Items.Wood]

	num_times = (1.0 - get_water()) // TANK_CAPACITY

	if num_times == 0:
		return
	
	if num_items(Items.Water_Tank) > num_times:
		for i in range(num_times):
			use_item(Items.Water_Tank)
	else:
		if num_items(Items.Wood) >= EMPTY_TANK_WOOD_COST:
			trade(Items.Empty_Tank)

def cultivate(entity):
	BUY_CARROT_SEEDS_BATCH = 100
	BUY_CACTUS_SEEDS_BATCH = 100
	BUY_EGGS_BATCH = 100

	if entity != Entities.Grass and entity != Entities.Dinosaur:
		check_ground_type()

	if entity != Entities.Cactus and entity != Entities.Dinosaur:
		water_if_needed()

	if entity == Entities.Carrots and num_items(Items.Carrot_Seed) == 0:
		if not trade(Items.Carrot_Seed, BUY_CARROT_SEEDS_BATCH):
			error()
		
	if entity == Entities.Cactus and num_items(Items.Cactus_Seed) == 0:
		if not trade(Items.Cactus_Seed, BUY_CACTUS_SEEDS_BATCH):
			quick_print(get_cost(Items.Cactus_Seed))
			error()

	if entity == Entities.Dinosaur and num_items(Items.Egg) == 0:
		if not trade(Items.Egg, BUY_EGGS_BATCH):
			error()

	if entity != Entities.Dinosaur:
		plant(entity)
	else:
		use_item(Items.Egg)