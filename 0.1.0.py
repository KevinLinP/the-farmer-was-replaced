if num_items(Items.Empty_Tank) == 0:
	trade(Items.Empty_Tank)

target_hay = 0
target_wood = 500

while True:
	move(North)
	
	if get_ground_type() != Grounds.Soil:
		till()
		plant(Entities.Grass)
	
	if get_entity_type() and not can_harvest():
		continue
	
	harvest()
		
	if num_items(Items.Hay) <= target_hay:
		plant(Entities.Grass)
	elif num_items(Items.Wood) <= target_wood:
		plant(Entities.Bush)
	else:
		if num_items(Items.Carrot_Seed) == 0:
			trade(Items.Carrot_Seed)
		plant(Entities.Carrots)
	