def run_0_4_0():
	DEBUG = False
	FERTILIZER_BATCH_BUY = 10

	WIDTH = get_world_size()
	HEIGHT = WIDTH
	DIRECTIONS = [North, East, South, West]

	def grow_hedges():
		if get_entity_type() == Entities.Hedge:
			return

		plant(Entities.Bush)

		while get_entity_type() != Entities.Bush:
			print("waiting for hedge")

		while get_entity_type() != Entities.Hedge:
			if num_items(Items.Fertilizer) == 0:
				trade(Items.Fertilizer, FERTILIZER_BATCH_BUY)
			use_item(Items.Fertilizer)

	def error():
		while True:
			do_a_flip()

	def neighbor_position(position, direction):
		x = position[0]
		y = position[1]

		if direction == North:
			y = (y + 1) % HEIGHT
		elif direction == East:
			x = (x + 1) % WIDTH
		elif direction == South:
			y = (y - 1) % HEIGHT
		elif direction == West:
			x = (x - 1) % WIDTH
		else:
			error()
		
		return (x, y)

	def initialize_walls():
		walls = []

		for _ in range(HEIGHT):
			row = []
			for _ in range(WIDTH):
				# [N, E, S, W]
				row.append([None, None, None, None])
			walls.append(row)

		for x in range(WIDTH):
			walls[0][x][2] = True
			walls[HEIGHT - 1][x][0] = True

		for y in range(HEIGHT):
			walls[y][0][3] = True
			walls[y][WIDTH - 1][1] = True

		return walls

	def directions(previous_direction):
		if previous_direction == None:
			return DIRECTIONS
		elif previous_direction == North:
			return [West, North, East, South]
		elif previous_direction == East:
			return [North, East, South, West]
		elif previous_direction == South:
			return [East, South, West, North]
		elif previous_direction == West:
			return [South, West, North, East]
		else:
			error()

	def direction_index(direction):
		if direction == North:
			return 0
		elif direction == East:
			return 1
		elif direction == South:
			return 2
		elif direction == West:
			return 3
		else:
			error()

	def can_go(position, direction, walls):
		current_wall = walls[position[1]][position[0]][direction_index(direction)]
		# quick_print(position[0], " ", position[1], " ", current_wall)
		# quick_print(walls)
		if current_wall:
			return False

		# TODO: set both on write instead
		target_position = neighbor_position(position, direction)
		opposite_wall = walls[target_position[1]][target_position[0]][(direction_index(direction) + 2) % 4]

		if opposite_wall:
			return False

		return target_position

	def go(current_position, previous_direction, walls):
		for direction in directions(previous_direction):
			# quick_print(current_position, " ", directions, " trying direction: ", direction)
			target_position = can_go(current_position, direction, walls)

			if target_position != False:
				moved = move(direction)

				if moved:
					if get_entity_type() == Entities.Treasure:
						harvest()
						return True
					# not necessary ATM
					# walls[current_position[1]][current_position[0]][direction_index(direction)] = False
					found = go(target_position, direction, walls)
					if found:
						return True
				else:
					walls[current_position[1]][current_position[0]][direction_index(direction)] = True

	def solve_maze():
		# visited = initialize_array(False)
		# visited[current_position[1]][current_position[0]] = True

		while True:
			current_position = (get_pos_x(), get_pos_y())
			walls = initialize_walls()
			grow_hedges()
			go(current_position, None, walls)
	
	solve_maze()

run_0_4_0()