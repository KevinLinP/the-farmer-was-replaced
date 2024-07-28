def hay_wood_carrots_0_2_0():
	WIDTH = get_world_size()
	HEIGHT = WIDTH
	DEFAULT_PLANT = Entities.Grass

	def initialize_array():
		array = []
		for _ in range(HEIGHT):
			row = []
			for _ in range(WIDTH):
				row.append(False)
			array.append(row)
		return array

	def plant_cycles():
		queue = [{'position': (4, 4), 'action': 'plant', 'entity': DEFAULT_PLANT}]
		planted = initialize_array()
		cycle_complete = False

		while len(queue) > 0:
			task = queue.pop(0)
			action = task['action']
			position = task['position']
			x = position[0]
			y = position[1]

			move_to(x, y)

			if task['action'] == 'plant':
				cultivate(task['entity'])
				planted[y][x] = True
				companion = get_companion()
				if not planted[companion[2]][companion[1]]:
					queue.insert(0, {'position': (companion[1], companion[2]), 'action': 'plant', 'entity': companion[0]})
				# else:
				# 	quick_print("cycle complete ", companion[2], " ", companion[2])
				queue.append({'position': task['position'], 'action': 'harvest', 'entity': task['entity']})
			elif task['action'] == 'harvest':
				while not can_harvest():
					water_if_needed()

				harvest()
				# quick_print("harvested ", x, " ", y)
				planted[y][x] = False
			
			if len(queue) == 0:
				queue = [{'position': (x, y), 'action': 'plant', 'entity': DEFAULT_PLANT}]

	clear()
	plant_cycles()

hay_wood_carrots_0_2_0()