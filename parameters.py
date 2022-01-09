import os


class Parameters:

  def __init__(
    self,
    N,
    GENERATE_ROOM,
    GENERATE_HEX,
    INI_PATTERN,
    NB_ITER_FLIP,
    SHOW_DETAILED_ROOM,
    DARK_BACKGROUND,
    COLOR_THEME,
    DRAW_FLOOR_AND_WALLS,
    USE_RANDOM_SEED,
    VAL_RANDOM_SEED,
    SHOW_INTERIM,
    INTERIM_LOG_ITERX,
    INTERIM_PRINT_ITERX
    ):

    self.N = N
    self.GENERATE_HEX = GENERATE_HEX
    self.GENERATE_ROOM = GENERATE_ROOM
    self.INI_PATTERN = INI_PATTERN
    self.SHOW_DETAILED_ROOM = SHOW_DETAILED_ROOM
    self.DARK_BACKGROUND = DARK_BACKGROUND
    self.COLOR_THEME = COLOR_THEME
    self.DRAW_FLOOR_AND_WALLS = DRAW_FLOOR_AND_WALLS
    self.SHOW_INTERIM = SHOW_INTERIM
    self.INTERIM_LOG_ITERX = INTERIM_LOG_ITERX
    self.INTERIM_PRINT_ITERX = INTERIM_PRINT_ITERX

    # Determine the half number of cubes that can fit in the room
    TOTAL_ROOM_VOLUME = N ** 3
    HALF_TOTAL_ROOM_VOLUME = int(TOTAL_ROOM_VOLUME / 2)

    # Determine the number of initial iterations
    if self.INI_PATTERN == 'random_half':
      self.NB_ITER_INIT = HALF_TOTAL_ROOM_VOLUME
    else:
      self.NB_ITER_INIT = 0

    # Determine the number of flip iterations
    if NB_ITER_FLIP < 0:
      self.NB_ITER_FLIP = TOTAL_ROOM_VOLUME
    else:
      self.NB_ITER_FLIP = NB_ITER_FLIP

    # Determine the number of total iterations
    self.NB_ITER_TOTAL = self.NB_ITER_INIT + self.NB_ITER_FLIP

    # Number of leading zeroes to display iterations during room population
    self.ZFILL = len(str(self.NB_ITER_TOTAL))

    # Plant the random seed for reproducibility
    if USE_RANDOM_SEED:
      random.seed(VAL_RANDOM_SEED)

    # Create the folder to print and save the results, and delete all pre-existing PNG images of room iterations
    self.RESULTS_PATH = 'results'
    if not os.path.exists(self.RESULTS_PATH):
      os.makedirs(self.RESULTS_PATH)
    list_of_pngs = os.listdir(self.RESULTS_PATH)
    for item in list_of_pngs:
      if item.startswith('room_iterx_') and item.endswith('.png'):
        os.remove(os.path.join(self.RESULTS_PATH, item))

    # If the room does not exist, it will be generated
    self.ROOM_NAME = 'room.pkl'
    self.GENERATE_ROOM = GENERATE_ROOM or not os.path.isfile(os.path.join(self.RESULTS_PATH, self.ROOM_NAME))

    # Determine the filename that will be used to save the final hexagon image
    self.FILENAME = 'Hex.Size={}.Init={}.NbFlips={}.FloorsAndWall={}.Color={}'.format(
      self.N, self.INI_PATTERN, self.NB_ITER_FLIP, self.DRAW_FLOOR_AND_WALLS, self.COLOR_THEME)

    # Print all parameters in the console
    print('\n'.join("%s: %s" % item for item in sorted(vars(self).items())))
    print('{:-<64}'.format(''))
