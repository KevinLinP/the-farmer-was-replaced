def initialize_array(initial_value):
  WORLD_SIZE = get_world_size()
  array = []

  for _ in range(WORLD_SIZE):
    row = []
    for _ in range(WORLD_SIZE):
      row.append(initial_value)
    array.append(row)

  return array