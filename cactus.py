def cactus():
	WIDTH = get_world_size()
	HEIGHT = get_world_size()

	def move_next():
		move(East)
		# if get_pos_x() == 0:
		# 	move(North)

	def fill_field(cactus_sizes):
		while True:
			x = get_pos_x()
			y = get_pos_y()
			check_ground_type()
			cultivate(Entities.Cactus)
			cactus_sizes[y][x] = measure()

			move_next()
			x = get_pos_x()
			y = get_pos_y()

			if x == 0 and y == 0:
				break

	def bubble_sort_x(cactus_sizes, y):
		cactus_sizes_row = cactus_sizes[y]
		for target_index in range(WIDTH - 1, -1, -1):
			quick_print(cactus_sizes_row)
			largest_num = -1
			largest_index = 0

			for x in range(target_index + 1):
				if cactus_sizes[y][x] > largest_num:
					largest_num = cactus_sizes_row[x]
					largest_index = x
				quick_print(target_index, x, cactus_sizes_row[x], largest_index, largest_num)			

			if largest_index == target_index:
				continue

			move_to(largest_index, y)
			for _ in range(target_index - largest_index):
				swap(East)
				x = get_pos_x()
				moved = cactus_sizes_row[x]
				cactus_sizes_row[x] = cactus_sizes_row[x + 1]
				cactus_sizes_row[x + 1] = moved
				move(East) # technically not needed on last iteration

	
	clear()
	cactus_sizes = initialize_array(None)
	fill_field(cactus_sizes)
	bubble_sort_x(cactus_sizes, get_pos_y())

cactus()