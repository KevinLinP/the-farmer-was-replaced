def move_to(target_x, target_y):
  WIDTH = get_world_size()
  HEIGHT = WIDTH

  def move_to_x(target):
    current = get_pos_x()

    if target > current:
      west_distance = current + WIDTH - target
      east_distance = target - current
    elif target < current:
      west_distance = current - target
      east_distance = WIDTH - current + target
    else:
      return

    if west_distance > east_distance:
      for _ in range(east_distance):
        move(East)
    else:
      for _ in range(west_distance):
        move(West)

    # origin is south west corner
  def move_to_y(target):
    current = get_pos_y()
    if target > current:
      north_distance = target - current
      south_distance = current + HEIGHT - target
    elif target < current:
      north_distance = HEIGHT - current + target
      south_distance = current - target
    else:
      return

    if north_distance > south_distance:
      for _ in range(south_distance):
        move(South)
    else:
      for _ in range(north_distance):
        move(North)

  move_to_x(target_x)
  move_to_y(target_y)