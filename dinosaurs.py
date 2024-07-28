def dinosaurs():
	def fill_field(cactus_sizes):
		move_to(0, 0)

		while True:
			x = get_pos_x()
			y = get_pos_y()
			check_ground_type()
			cultivate(Entities.Dinosaur)
			cactus_sizes[y][x] = measure()

			move_next()
			x = get_pos_x()
			y = get_pos_y()

			if x == 0 and y == 0:
				break

	clear()
	dino_types = initialize_array(None)
	fill_field(dino_types)
    
dinosaurs()