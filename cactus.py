def cactus():
	WIDTH = get_world_size()
	HEIGHT = get_world_size()

	def move_next():
		move(East)
		if get_pos_x() == 0:
			move(North)

	def fill_field(cactus_sizes):
		while True:
			x = get_pos_x()
			y = get_pos_y()
			check_ground_type()
			cultivate(Entities.Cactus)
			cactus_sizes[y][x] = measure()

			move_next()

			if x == 0 and y == 0:
				break

	def bubble_sort_x(cactus_sizes, y):
		for target_index in range(0, WIDTH, -1):
			largest_num = -1
			largest_index = 0

			for x in range(target_index + 1):
				if cactus_sizes[y][x] > largest_num:
					largest_num = cactus_sizes[y][x]
					largest_index = x

			if largest_index == target_index:
				continue

			move_to(largest_index, y)
			for _ in range(largest_index - target_index):
				swap(East)
				move(East) # technically not needed on last iteration

	
	cactus_sizes = initialize_array(None)
	fill_field(cactus_sizes)
	bubble_sort_x(cactus_sizes, get_pos_y())

cactus()