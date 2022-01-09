import numpy as np
import math
import sys
import os
import time
import pickle
import matplotlib.pyplot as plt
from utils import print_iter_msg
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection


# ----------------------------------------------------------------
# Generate and display the hex, from a previously generated room
# ----------------------------------------------------------------
def generate_and_display_hex(p):

  # Log the progress
  t_ini = time.time()
  iterx = 0
  print_iter_msg('Hex', iterx, p.N, t_ini, t_ini)

  # Load the previously generated room
  with open(os.path.join(p.RESULTS_PATH, 'room.pkl'), 'rb') as fid:
    room = pickle.load(fid)

  # Get the specified color theme
  color_edges, color_top, color_lft, color_rgt = get_color_theme(p.COLOR_THEME)

  # Define the translation shift between two neighbor lozenges
  di = 1
  dj = math.tan(math.pi / 6)
  two_dj = 2 * dj

  # Create figure
  fig = plt.figure()
  axx = fig.add_subplot(1, 1, 1)

  # Background color
  if p.DARK_BACKGROUND:
    plt.style.use('dark_background')

  # Control the ordering that is used to display each plotted object
  zorder = 0

  # Handle the floor and the walls
  if p.DRAW_FLOOR_AND_WALLS:

    # Convert room coordinates (x, y) into a set of four 2D coordinates for the corresponding lozenge tile vertices
    top, _, _, _ = convert_xy_to_lozenge(0, 0, di, dj)
    _, bot, _, _ = convert_xy_to_lozenge(p.N-1, p.N-1, di, dj)
    _, _, lft, _ = convert_xy_to_lozenge(p.N-1, 0, di, dj)
    _, _, _, rgt = convert_xy_to_lozenge(0, p.N-1, di, dj)

    # Seven vertices to define the floor (b-e-a-c), the left wall (b-g-d-c), and the right wall (b-g-f-e)
    vertex_a = [bot[0], bot[1]]
    vertex_b = [top[0], top[1]]
    vertex_c = [rgt[0], rgt[1]]
    vertex_d = [rgt[0], rgt[1] + p.N*two_dj]
    vertex_e = [lft[0], lft[1]]
    vertex_f = [lft[0], lft[1] + p.N*two_dj]
    vertex_g = [top[0], top[1] + p.N*two_dj]

    # Draw the floor, the left wall, and the right wall
    zorder = add_ploygon(vertex_b, vertex_e, vertex_a, vertex_c, zorder, axx, color_top)
    zorder = add_ploygon(vertex_b, vertex_g, vertex_d, vertex_c, zorder, axx, color_lft)
    zorder = add_ploygon(vertex_b, vertex_g, vertex_f, vertex_e, zorder, axx, color_rgt)

    # Draw the grid on the floor
    for x in range(p.N+1):
      top, _, _, _ = convert_xy_to_lozenge(x, 0, di, dj)
      plt.plot([top[0], top[0] + p.N*di], [top[1], top[1] - p.N*dj], color=color_edges, zorder=zorder)
    for y in range(p.N+1):
      top, _, _, _ = convert_xy_to_lozenge(0, y, di, dj)
      plt.plot([top[0], top[0] - p.N*di], [top[1], top[1] - p.N*dj], color=color_edges, zorder=zorder)

    # Draw the grid on the left wall
    for y in range(p.N+1):
      top, _, _, _ = convert_xy_to_lozenge(0, y, di, dj)
      plt.plot([top[0], top[0]], [top[1], top[1] + p.N*two_dj], color=color_edges, zorder=zorder)
    top, _, _, _ = convert_xy_to_lozenge(0, 0, di, dj)
    _, _, _, rgt = convert_xy_to_lozenge(0, p.N-1, di, dj)
    for k in range(1, p.N+1): # (start from 1 because has already been traced as part of the floor)
      plt.plot([top[0], rgt[0]], [top[1] + k*two_dj, rgt[1] + k*two_dj], color=color_edges, zorder=zorder)

    # Draw the grid on the right wall
    for x in range(1, p.N+1): # (start from 1 because has already been traced as part of the left wall)
      top, _, _, _ = convert_xy_to_lozenge(x, 0, di, dj)
      plt.plot([top[0], top[0]], [top[1], top[1] + p.N*two_dj], color=color_edges, zorder=zorder)
    top, _, _, _ = convert_xy_to_lozenge(0, 0, di, dj)
    _, _, lft, _ = convert_xy_to_lozenge(p.N-1, 0, di, dj)
    for k in range(1, p.N+1): # (start from 1 because has already been traced as part of the floor)
      plt.plot([top[0], lft[0]], [top[1] + k*two_dj, lft[1] + k*two_dj], color=color_edges, zorder=zorder)

    # Increase the layer count
    zorder += 1

  # Draw the visible part of each stack, starting from the background, and progressively advancing to the foreground
  for x in range(p.N):
    for y in range(p.N):

      # Convert room coordinates (x, y) into a set of four 2D coordinates for the corresponding lozenge tile vertices
      top, bot, lft, rgt = convert_xy_to_lozenge(x, y, di, dj)

      # Get the stack height of the cube at coordinates (x, y)
      stack_height = room[y, x]

      # The floor was already handled
      if stack_height > 0:

        # Get the height of the next stack to the left, at coordinates (x+1, y)
        if x+1 < p.N:
          stack_height_next_lft = room[y, x+1]
        else:
          stack_height_next_lft = 0

        # Get the height of the next stack to the right, at coordinates (x, y+1)
        if y+1 < p.N:
          stack_height_next_rgt = room[y+1, x]
        else:
          stack_height_next_rgt = 0

        # Seven vertices to define the top (b-d-g-f), the left face (b-a-c-d), and the right face (b-a-e-f) of the stack
        vertex_a = [bot[0], bot[1]]
        vertex_b = [bot[0], bot[1]+stack_height*two_dj]
        vertex_c = [lft[0], lft[1]]
        vertex_d = [lft[0], lft[1]+stack_height*two_dj]
        vertex_e = [rgt[0], rgt[1]]
        vertex_f = [rgt[0], rgt[1]+stack_height*two_dj]
        vertex_g = [top[0], top[1]+stack_height*two_dj]

        # Draw own left face and left edge, if self is taller than the next stack to the left
        if stack_height > stack_height_next_lft:
          zorder = add_ploygon(vertex_b, vertex_a, vertex_c, vertex_d, zorder, axx, color_lft)
          plt.plot([lft[0], lft[0]], [lft[1], lft[1]+stack_height*two_dj], color=color_edges, zorder=zorder)
          zorder += 1

        # Draw own right face and right edge, if self is taller than the next stack to the right
        if stack_height > stack_height_next_rgt:
          zorder = add_ploygon(vertex_b, vertex_a, vertex_e, vertex_f, zorder, axx, color_rgt)
          plt.plot([rgt[0], rgt[0]], [rgt[1], rgt[1]+stack_height*two_dj], color=color_edges, zorder=zorder)
          zorder += 1

        # Draw own frontal edge, if self is taller than the next stacks both to the left and to the right
        if stack_height > stack_height_next_lft and stack_height > stack_height_next_rgt:
          plt.plot([bot[0], bot[0]], [bot[1], bot[1]+stack_height*two_dj], color=color_edges, zorder=zorder)
          zorder += 1

        # Draw own horizontal edges, if self is taller than the next stacks either to the left or to the right
        for k in range(min(stack_height_next_lft, stack_height_next_rgt), stack_height):
          plt.plot(
            [lft[0], bot[0], rgt[0]],
            [lft[1]+k*two_dj, bot[1]+k*two_dj, rgt[1]+k*two_dj], color=color_edges, zorder=zorder)
        zorder += 1

        # Draw the top face of the stack
        zorder = add_ploygon(vertex_b, vertex_d, vertex_g, vertex_f, zorder, axx, color_top)
        plt.plot(
          [vertex_b[0], vertex_d[0], vertex_g[0], vertex_f[0], vertex_b[0]],
          [vertex_b[1], vertex_d[1], vertex_g[1], vertex_f[1], vertex_b[1]], color=color_edges, zorder=zorder)
        zorder += 1

      # Log the progress
      t_now = time.time()
      print_iter_msg('Hex', x+1, p.N, t_now, t_ini)

  plt.axis('off')
  axx.axis('equal')
  fig.set_size_inches(30, 30, forward = True)
  fig.savefig(os.path.join(p.RESULTS_PATH, p.FILENAME + '.png'), bbox_inches='tight', dpi=100)
  plt.close('all')


# ----------------------------------------------------------------
# Plot a polygon surface and specify its rank as a displayed layer
# ----------------------------------------------------------------
def add_ploygon(vertex_a, vertex_b, vertex_c, vertex_d, zorder, axx, color):
  poly = []
  poly.append(Polygon([vertex_a, vertex_b, vertex_c, vertex_d]))
  collection = PatchCollection(poly, color=color, zorder=zorder)
  axx.add_collection(collection)
  zorder += 1
  return zorder


# ----------------------------------------------------------------
# Convert room coordinates (x, y) into a set of four 2D coordinates for the corresponding lozenge tile vertices
# ----------------------------------------------------------------
def convert_xy_to_lozenge(x, y, di, dj):
  i = (-x + y) * di
  j = -(x + y) * dj
  top = [i, j + dj]
  bot = [i, j - dj]
  lft = [i - di, j]
  rgt = [i + di, j]
  return top, bot, lft, rgt


# ----------------------------------------------------------------
# Set the color theme
# ----------------------------------------------------------------
def get_color_theme(COLOR_THEME):

  if COLOR_THEME == 'rgb':
    color_edges = 'black'
    color_top = 'orangered'
    color_lft = 'yellowgreen'
    color_rgt = 'steelblue'

  elif COLOR_THEME == 'cmy':
    color_edges = 'dimgray'
    color_top = 'lightcyan'
    color_lft = 'thistle'
    color_rgt = 'khaki'

  elif COLOR_THEME == 'strawberry_explosion':
    color_edges = 'darkred'
    color_top = 'linen'
    color_lft = 'crimson'
    color_rgt = 'lightpink'

  elif COLOR_THEME == 'alien_vomit':
    color_edges = 'darkolivegreen'
    color_top = 'palegreen'
    color_lft = 'darkseagreen'
    color_rgt = 'chartreuse'

  elif COLOR_THEME == 'frozen_tango':
    color_edges = 'darkslategray'
    color_top = 'paleturquoise'
    color_lft = 'steelblue'
    color_rgt = 'skyblue'

  elif COLOR_THEME == 'cosmic_penguin':
    color_edges = 'darkcyan'
    color_top = 'lightcyan'
    color_lft = 'darkturquoise'
    color_rgt = 'cyan'

  elif COLOR_THEME == 'magic_apocalypse':
    color_edges = 'purple'
    color_top = 'lavenderblush'
    color_lft = 'orchid'
    color_rgt = 'plum'

  elif COLOR_THEME == 'eldorado_craze':
    color_edges = 'saddlebrown'
    color_top = 'lemonchiffon'
    color_lft = 'darkgoldenrod'
    color_rgt = 'gold'

  elif COLOR_THEME == 'noir_joke':
    color_edges = 'black'
    color_top = 'whitesmoke'
    color_lft = 'dimgray'
    color_rgt = 'silver'

  else:
    print('ERROR: Invalid value for parameter "COLOR_THEME": ' + str(COLOR_THEME))
    sys.exit()

  return color_edges, color_top, color_lft, color_rgt
