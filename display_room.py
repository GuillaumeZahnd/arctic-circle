import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from utils import stopwatch


# ----------------------------------------------------------------
# Display the room
# ----------------------------------------------------------------
def display_room(room, lookup_add, lookup_rmv, t_now, t_ini, p, f, iterx=0, x=0, y=0, flip_sign=0):

  # Determine if the current iteration belongs to the "initialization" phase or to the "flip" phase
  if p.INI_PATTERN == 'random_half':
    iterx_init = min(iterx, p.NB_ITER_INIT)
    iterx_flip = iterx - iterx_init
    iter_msg = 'Iteration: {}/{} (Init: {}/{}, Flip: {}/{})'.format(
      iterx, p.NB_ITER_TOTAL, iterx_init, p.NB_ITER_INIT, iterx_flip, p.NB_ITER_FLIP)
  else:
    iter_msg = 'Iteration: {}/{}'.format(iterx, p.NB_ITER_TOTAL)

  # Prepare text information to be displayed as the figure title
  room_msg = r'Room ({} $\times$ {} $\times$ {})'.format(p.N, p.N, p.N)
  time_msg = 'Elapsed time: {}'.format(stopwatch(t_now, t_ini))
  monotony_msg = 'Monotony: {}'.format(f.monotony)
  filling_msg = 'Filling: {}'.format(f.filling)
  poles_msg = 'Poles: (2, 8)=({}, {}), (4, 10)=({}, {}), (6, 12)=({}, {})'.format(
    f.x_empty, f.x_full, f.y_empty, f.y_full, f.z_empty, f.z_full)

  # Colors to indicate where cubes can potentially be added and/or removed
  color_neutral = 'white'
  color_add = 'orchid'
  color_rmv = 'darkorange'

  # Colorbar range
  vmin = 0
  vmax = p.N

  # Create figure
  fig = plt.figure()

  # Panel
  if p.SHOW_DETAILED_ROOM:
    axx = fig.add_subplot(2, 3, 1)
    mark_cubes(axx, room, flip_sign, x, y, p.N, color_add, color_rmv, color_neutral)
  else:
    axx = fig.add_subplot(2, 2, 1)
  fig.sca(axx)
  im = plt.imshow(room, vmin=vmin, vmax=vmax)
  plt.xlabel('x-axis')
  plt.ylabel('y-axis')
  plt.title(
    room_msg + ' | ' + time_msg + '\n' + iter_msg + '\n' + monotony_msg + ' | ' + filling_msg + ' | ' + poles_msg)
  nice_colorbar(im, axx)

  # Panel
  if p.SHOW_DETAILED_ROOM:
    axx = fig.add_subplot(2, 3, 4, projection='3d')
  else:
    axx = fig.add_subplot(2, 2, 2, projection='3d')
  fig.sca(axx)
  X = np.arange(p.N)
  Y = np.arange(p.N)
  X, Y = np.meshgrid(X, Y)
  im = axx.plot_surface(
    X, Y, room, linewidth=1, antialiased=True, edgecolor='white', rstride=1, cstride=1, vmin=vmin, vmax=vmax,
    cmap='viridis')
  axx.set_xlabel('x-axis')
  axx.set_ylabel('y-axis')
  axx.set_zlabel('Number of stacked cubes')
  axx.set_xlim(0, max(1, p.N-1))
  axx.set_ylim(0, max(1, p.N-1))
  axx.set_zlim(0, p.N)
  axx.azim = 45

  # Panel
  if p.SHOW_DETAILED_ROOM:
    axx = fig.add_subplot(2, 3, 2)
  else:
    axx = fig.add_subplot(2, 2, 3)
  fig.sca(axx)
  im = plt.imshow(lookup_add, cmap='gray', vmin=0, vmax=1)
  plt.xlabel('x-axis')
  plt.ylabel('y-axis')
  plt.title('Cubes that can be added')

  # Panel
  if p.SHOW_DETAILED_ROOM:
    axx = fig.add_subplot(2, 3, 3)
  else:
    axx = fig.add_subplot(2, 2, 4)
  fig.sca(axx)
  im = plt.imshow(lookup_rmv, cmap='gray', vmin=0, vmax=1)
  plt.xlabel('x-axis')
  plt.ylabel('y-axis')
  plt.title('Cubes that can be removed')

  # Panel
  if p.SHOW_DETAILED_ROOM:
    axx = fig.add_subplot(2, 3, 5)
    fig.sca(axx)
    im = plt.imshow(room, vmin=0, vmax=p.N)
    mark_potential_add(axx, room, lookup_add, flip_sign, x, y, p.N, color_add, color_neutral)
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.title(r'Cubes that can be added ($+$)')

  # Panel
  if p.SHOW_DETAILED_ROOM:
    axx = fig.add_subplot(2, 3, 6)
    fig.sca(axx)
    im = plt.imshow(room, vmin=0, vmax=p.N)
    mark_potential_rmv(axx, room, lookup_rmv, flip_sign, x, y, p.N, color_rmv, color_neutral)
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    plt.title(r'Cubes that can be removed ($-$)')

  # Save the figure
  if p.SHOW_DETAILED_ROOM:
    fig.set_size_inches(40, 30, forward = True)
  else:
    fig.set_size_inches(30, 30, forward = True)
  fig.savefig(
    os.path.join(p.RESULTS_PATH, 'room_iterx_' + str(iterx).zfill(p.ZFILL) + '.png'), bbox_inches='tight', dpi=100)
  plt.close('all')


# ----------------------------------------------------------------
# Annotate the figure to indicate the height of each stack of cubes
# ----------------------------------------------------------------
def mark_cubes(axx, room, flip_sign, x, y, N, color_add, color_rmv, color_neutral):
  for idx in range(N):
    for idy in range(N):
      text = axx.text(idy, idx, room[idx, idy], ha='center', va='center', color=color_neutral)
  # On purpose, if "flip_sign == 0", no circle shall be drawn
  if flip_sign > 0:
    circle_flip = plt.Circle((x, y), 0.5, color=color_add, fill=False)
    axx.add_patch(circle_flip)
  elif flip_sign < 0:
    circle_flip = plt.Circle((x, y), 0.5, color=color_rmv, fill=False)
    axx.add_patch(circle_flip)


# ----------------------------------------------------------------
# Indicate locations where cubes can potentially be added
# ----------------------------------------------------------------
def mark_potential_add(axx, room, add_map, flip_sign, x, y, N, color_add, color_neutral):
  for idx in range(N):
    for idy in range(N):
      if add_map[idx, idy]:
        text = axx.text(idy, idx, str(room[idx, idy]) + r'$+$', ha='center', va='center', color=color_add)
      else:
        text = axx.text(idy, idx, room[idx, idy], ha='center', va='center', color=color_neutral)
  # On purpose, if "flip_sign == 0", no circle shall be drawn
  if flip_sign > 0:
    circle_flip = plt.Circle((x, y), 0.5, color=color_add, fill=False)
    axx.add_patch(circle_flip)
  elif flip_sign < 0:
    circle_flip = plt.Circle((x, y), 0.5, color=color_neutral, fill=False)
    axx.add_patch(circle_flip)


# ----------------------------------------------------------------
# Indicate locations where cubes can potentially be removed
# ----------------------------------------------------------------
def mark_potential_rmv(axx, room, rmv_map, flip_sign, x, y, N, color_rmv, color_neutral):
  for idx in range(N):
    for idy in range(N):
      if rmv_map[idx, idy]:
        text = axx.text(idy, idx, str(room[idx, idy]) + r'$-$', ha='center', va='center', color=color_rmv)
      else:
        text = axx.text(idy, idx, room[idx, idy], ha='center', va='center', color=color_neutral)
  # On purpose, if "flip_sign == 0", no circle shall be drawn
  if flip_sign < 0:
    circle_flip = plt.Circle((x, y), 0.5, color=color_rmv, fill=False)
    axx.add_patch(circle_flip)
  elif flip_sign > 0:
    circle_flip = plt.Circle((x, y), 0.5, color=color_neutral, fill=False)
    axx.add_patch(circle_flip)


# ----------------------------------------------------------------
# We deserve nice things
# ----------------------------------------------------------------
def nice_colorbar(im, axx):
  divider = make_axes_locatable(axx)
  cax = divider.append_axes('right', size='5%', pad=0.05)
  plt.colorbar(im, cax=cax)
