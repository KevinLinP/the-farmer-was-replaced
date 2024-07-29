def dinosaurs():
	WIDTH = get_world_size()
	HEIGHT = WIDTH
	NUM_SORTS_BEFORE_HARVEST = 3

	def fill_field(dino_types, dino_counts):
		move_to(0, 0)

		while True:
			x = get_pos_x()
			y = get_pos_y()
			check_ground_type()
			cultivate(Entities.Dinosaur)
			type = measure()
			dino_counts[y][x] = type
			dino_counts[type] += 1

			move_next()
			x = get_pos_x()
			y = get_pos_y()

			if x == 0 and y == 0:
				break

	def bubble_sort_x(dino_types, y):
		dino_types_row = dino_types[y]
		for target_index in range(WIDTH - 1, -1, -1):
			largest_num = -1
			largest_index = 0

			for x in range(target_index + 1):
				# >= makes this stable
				if dino_types[y][x] >= largest_num:
					largest_num = dino_types_row[x]
					largest_index = x
				# quick_print(target_index, x, cactus_sizes_row[x], largest_index, largest_num)			

			if largest_index == target_index:
				continue

			move_to(largest_index, y)
			for _ in range(target_index - largest_index):
				swap(East)
				x = get_pos_x()
				moved = dino_types_row[x]
				dino_types_row[x] = dino_types_row[x + 1]
				dino_types_row[x + 1] = moved
				move(East) # technically not needed on last iteration

	clear()
	dino_types = initialize_array(None)
	dino_counts = [0, 0, 0, 0]
	fill_field(dino_types, dino_counts)

	for _ in range(NUM_SORTS_BEFORE_HARVEST):
		for y in range(HEIGHT):
			bubble_sort_x(dino_types, y)

	move_to(0, 0)
	for _ in range(WIDTH):
		if can_harvest():
			harvest()
		move_next()
    
dinosaurs()