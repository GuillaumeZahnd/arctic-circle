import parameters
from generate_room import generate_room
from generate_and_display_hex import generate_and_display_hex


# Possible options for "INI_PATTERN":
"""
'empty', 'full', 'random_half', 'poles_2_6_10', 'poles_4_8_12', 'arctic_circle'
"""


# Possible options for "COLOR_THEME":
"""
'rgb', 'cmy', 'noir_joke',
'strawberry_explosion', 'alien_vomit', 'frozen_tango',
'cosmic_penguin', 'magic_apocalypse', 'eldorado_craze'
"""


if __name__ == '__main__':

  # Set parameters
  p = parameters.Parameters(
    N                    = 16,            # Room size
    GENERATE_ROOM        = True,          # Indicate whether the room shall be generated
    GENERATE_HEX         = True,          # Indicate whether the hexagon shall be generated (prerequisite: room)
    INI_PATTERN          = 'random_half', # Indicate how the room shall be initialized, before random flips are applied
    NB_ITER_FLIP         = 10**3,         # Number of random flips (if negative, will be reset to the total room volume)
    SHOW_DETAILED_ROOM   = True,          # Indicate whether the room image shall show details about potential flips
    DARK_BACKGROUND      = False,         # Indicate whether to display the final hex with a dark background
    COLOR_THEME          = 'rgb',         # Color theme
    DRAW_FLOOR_AND_WALLS = True,          # Draw the floor and both walls of the room
    USE_RANDOM_SEED      = False,         # Indicate whether a random seed shall be planted for reproducibility
    VAL_RANDOM_SEED      = 3.14,          # Value of the random seed
    SHOW_INTERIM         = True,          # Indicate whether intermediate room states shall be printed as PNG images
    INTERIM_LOG_ITERX    = 10**2,         # Indicate the step size at which room iterations shall be printed in the console
    INTERIM_PRINT_ITERX  = 10**3          # Indicate the step size at which room iterations shall be saved as images
    )

  # Generate room
  if p.GENERATE_ROOM:
    generate_room(p)

  # Generate hex
  if p.GENERATE_HEX:
    generate_and_display_hex(p)
