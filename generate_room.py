import sys
import os
import numpy as np
import random
import time
import pickle
import fitness
from display_room import display_room
import fitness
from utils import print_iter_msg
from utils import stopwatch


# ----------------------------------------------------------------
# Generate the room, from the specified parameters
# ----------------------------------------------------------------
def generate_room(p):

  # Log the progress
  t_ini = time.time()
  t_now = t_ini
  iterx = 0
  print_iter_msg('Room', iterx, p.NB_ITER_TOTAL, t_now, t_ini)

  # Room initialization
  room, lookup_add, lookup_rmv = room_initialization(p.INI_PATTERN, p.N)

  # Get a "fitness class" (he he he)
  f = fitness.Fitness()

  # Initial display
  if p.SHOW_INTERIM and iterx == 0:
    f.assess_room_fitness(room, p.N)
    display_room(room, lookup_add, lookup_rmv, t_now, t_ini, p, f, iterx=0, x=0, y=0, flip_sign=0)

  # Iterative flips: cubes are randomly added or removed in the room, legal actions are tracked by the "lookup_" maps
  for iterx in range(p.NB_ITER_TOTAL):

    # Iteration number after the iteration zero
    iterx_plus_one = iterx +1

    # Log the progress
    if iterx_plus_one % p.INTERIM_LOG_ITERX == 0:
      t_now = time.time()
      print_iter_msg('Room', iterx_plus_one, p.NB_ITER_TOTAL, t_now, t_ini)

    # Randomly choose whether to add or remove a cube
    lookup_flip, flip_sign = randomly_choose_add_or_rmv(
      lookup_add, lookup_rmv, iterx, p.NB_ITER_INIT, p.INI_PATTERN)

    # Randomly select a cube to flip, and retrieve its [x, y] coordinates
    x, y = randomly_choose_cube(lookup_flip)

    # Alter the cube in the room
    room[y, x] += flip_sign

    # Update the possible actions
    lookup_add = update_lookup_add(lookup_add, room, x, y, p.N)
    lookup_rmv = update_lookup_rmv(lookup_rmv, room, x, y, p.N)

    # Intermediate display(s)
    if p.SHOW_INTERIM and iterx_plus_one % p.INTERIM_PRINT_ITERX == 0:
      f.assess_room_fitness(room, p.N)
      display_room(room, lookup_add, lookup_rmv, t_now, t_ini, p, f, iterx_plus_one, x, y, flip_sign)

  # Save the room
  with open(os.path.join(p.RESULTS_PATH, p.ROOM_NAME), 'wb') as fid:
    pickle.dump(room, fid)

  # Final display
  if p.NB_ITER_TOTAL > 0:
    t_now = time.time()
    print_iter_msg('Room', p.NB_ITER_TOTAL, p.NB_ITER_TOTAL, t_now, t_ini)
    f.assess_room_fitness(room, p.N)
    display_room(room, lookup_add, lookup_rmv, t_now, t_ini, p, f, p.NB_ITER_TOTAL, x=0, y=0, flip_sign=0)

  # Print the fitness metrics in the console
  print('Fitness\t| Monotony: {}, Filling: {}, Poles: ({}, {}), ({}, {}), ({}, {})'.format(
    f.monotony,
    f.filling,
    f.x_full,
    f.x_empty,
    f.y_full,
    f.y_empty,
    f.z_full,
    f.z_empty))


# ----------------------------------------------------------------
# Room initialization
# ----------------------------------------------------------------
def room_initialization(INI_PATTERN, N):

  if INI_PATTERN == 'empty':
    # Empty room: only the cube tucked in the corner (0,0) can be added, no cube can be removed
    room = np.zeros((N, N), dtype = np.int32)
    lookup_add = np.zeros((N, N), dtype = bool)
    lookup_add[0, 0] = True
    lookup_rmv = np.zeros((N, N), dtype = bool)

  elif INI_PATTERN == 'full' or INI_PATTERN == 'random_half':
    # Full room: only the outermost cube (N,N) can be removed, no cube can be added
    room = N * np.ones((N, N), dtype = np.int32)
    lookup_add = np.zeros((N, N), dtype = bool)
    lookup_rmv = np.zeros((N, N), dtype = bool)
    lookup_rmv[N-1, N-1] = True

  elif INI_PATTERN == 'poles_2_6_10':
    # Fill the room up to the plane defined by the three hex vertices that are the closest to the corner (0,0)
    thresh = N
    offset = 0
    room, lookup_add, lookup_rmv = generate_poles(N, thresh, offset)

  elif INI_PATTERN == 'poles_4_8_12':
    # Fill the room up to the plane defined by the three hex vertices that are the farthest from the corner (0,0)
    thresh = 2 * N
    offset = 2
    room, lookup_add, lookup_rmv = generate_poles(N, thresh, offset)

  elif INI_PATTERN == 'arctic_circle':
    # Generate a perfect arctic circle (if N is even), with 2-4-6-8-10-12 o'clock frozen poles, and a chaotic center
    thresh = int(np.ceil(1.5 * N))
    offset = 1
    room, lookup_add, lookup_rmv = generate_poles(N, thresh, offset)

  else:
    # Non valid input
    print('ERROR: Invalid value for parameter "INI_PATTERN": ' + str(INI_PATTERN))
    sys.exit()

  return room, lookup_add, lookup_rmv


# ----------------------------------------------------------------
# Initialize the room with perfect frozen poles (either 2-6-10 o'clock, 4-8-12 o'clock, or 2-4-6-8-10-12 o'clock)
# ----------------------------------------------------------------
def generate_poles(N, thresh, offset):
  offset_rmv = offset +1
  offset_add = offset -1
  room = np.zeros((N, N), dtype = np.int32)
  lookup_add = np.zeros((N, N), dtype = bool)
  lookup_rmv = np.zeros((N, N), dtype = bool)
  for x in range(N):
    for y in range(N):
      room[y, x] = min(max(thresh - (x + y + offset), 0), N)
      neighbor = min(max(thresh - (x + y + offset_add), 0), N)
      lookup_add[y, x] = room[y, x] - neighbor
      neighbor = min(max(thresh - (x + y + offset_rmv), 0), N)
      lookup_rmv[y, x] = neighbor - room[y, x]
  return room, lookup_add, lookup_rmv


# ----------------------------------------------------------------
# Randomly choose a cube that can be either added or removed (as specified by "lookup") and get its [x, y] coordinates
# ----------------------------------------------------------------
def randomly_choose_cube(lookup):
  idx = np.random.randint(low=0, high=lookup.sum())
  pos = np.argwhere(lookup)[idx]
  x = pos[1]
  y = pos[0]
  return x, y


# ----------------------------------------------------------------
# Randomly choose whether to add or remove a cube
# ----------------------------------------------------------------
def randomly_choose_add_or_rmv(lookup_add, lookup_rmv, iterx, NB_ITER_INIT, INI_PATTERN):

  if INI_PATTERN == 'random_half' and iterx < NB_ITER_INIT:
    # Cubes can only be removed, until a random configuration is reached where the room is half-full
    lookup_flip = lookup_rmv
    flip_sign = -1

  else:
    # Cubes can be added or removed
    weight_add = lookup_add.sum() / (lookup_add.sum() + lookup_rmv.sum())
    weight_rmv = 1.0 - weight_add
    add_or_rmv = random.choices(population = ['add', 'rmv'], weights = [weight_add, weight_rmv])[0]
    if add_or_rmv == 'add':
      lookup_flip = lookup_add
      flip_sign = +1
    else:
      lookup_flip = lookup_rmv
      flip_sign = -1

  return lookup_flip, flip_sign


# ----------------------------------------------------------------
# Update the Boolean lookup map that indicates where cubes could be added
# ----------------------------------------------------------------
def update_lookup_add(lookup_add, room, x, y, N):

  # Enable self, if own height became strictly smaller than the height of the x/y previous neighbor
  if x == 0 and y == 0:
    lookup_add[y, x] = True
  elif x > 0 and y == 0:
    if room[y, x] < room[y, x-1]:
      lookup_add[y, x] = True
  elif x == 0 and y > 0:
    if room[y, x] < room[y-1, x]:
      lookup_add[y, x] = True
  elif x > 0 and y > 0:
    if room[y, x] < room[y, x-1] and room[y, x] < room[y-1, x]:
      lookup_add[y, x] = True

  # Disable self, if own height became equal to the maximal height
  if room[y, x] == N:
    lookup_add[y, x] = False

  # Disable self, if own height became equal to the height of the x/y previous neighbor
  if x > 0:
    if room[y, x] == room[y, x-1]:
      lookup_add[y, x] = False
  if y > 0:
    if room[y, x] == room[y-1, x]:
      lookup_add[y, x] = False

  # Disable the x/y next neighbor, if own height became equal to the height of the x/y next neighbor
  if x < N-1:
    if room[y, x] == room[y, x+1]:
      lookup_add[y, x+1] = False
  if y < N-1:
    if room[y, x] == room[y+1, x]:
      lookup_add[y+1, x] = False

  # Enable the x/y next neighbor, if own height became strictly larger than the height of the x/y previous neighbor
  if x < N-1:
    if room[y, x] > room[y, x+1]:
      if y == 0:
        lookup_add[y, x+1] = True
      else:
        if room[y-1, x+1] > room[y, x+1]:
          lookup_add[y, x+1] = True
  if y < N-1:
    if room[y, x] > room[y+1, x]:
      if x == 0:
        lookup_add[y+1, x] = True
      else:
        if room[y+1, x-1] > room[y+1, x]:
          lookup_add[y+1, x] = True

  return lookup_add


# ----------------------------------------------------------------
# Update the Boolean lookup map that indicates where cubes could be removed
# ----------------------------------------------------------------
def update_lookup_rmv(lookup_rmv, room, x, y, N):

  N_MINUS_ONE = N-1

  # Disable self, if own height became equal to the minimal height, otherwise enable self
  if room[y, x] == 0:
    lookup_rmv[y, x] = False
  else:
    lookup_rmv[y, x] = True

  # Disable self, if own height became equal to the height of the x/y next neighbor
  if x < N_MINUS_ONE:
    if room[y, x] == room[y, x+1]:
      lookup_rmv[y, x] = False
  if y < N_MINUS_ONE:
    if room[y, x] == room[y+1, x]:
      lookup_rmv[y, x] = False

  # Disable the x/y previous neighbor, if own height became equal to the height of the x/y previous neighbor
  if x > 0:
    if room[y, x] == room[y, x-1]:
      lookup_rmv[y, x-1] = False
  if y > 0:
    if room[y, x] == room[y-1, x]:
      lookup_rmv[y-1, x] = False

  # Enable the x/y previous neighbor, if own height became strictly smaller than the height of the x/y previous neighbor
  if x > 0:
    if room[y, x-1] > room[y, x]:
      if y == N_MINUS_ONE:
        lookup_rmv[y, x-1] = True
      else:
        if room[y, x-1] > room[y+1, x-1]:
          lookup_rmv[y, x-1] = True
  if y > 0:
    if room[y-1, x] > room[y, x]:
      if x == N_MINUS_ONE:
        lookup_rmv[y-1, x] = True
      else:
        if room[y-1, x] > room[y-1, x+1]:
          lookup_rmv[y-1, x] = True

  return lookup_rmv
