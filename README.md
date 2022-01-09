# README

## Problem

### Definition

Let us consider a regular ```NxNxN``` hexagon and its inner unit triangular lattice. The objective is to populate the entire hexagon surface with elementary blocks. The blocks are drawn uniformly at random from the collection composed the three types of lozenges that can be obtained by the union of two adjacent triangles of the lattice.

### Arctic circle theorem

> The random tiling of a large hexagon tends to be frozen in regions near the poles.

This can be explained by the fact that the hexagon vertices, which define the outer borders of the lattice, impose a strong tiling condition that reduces the number of possible configurations in the outermost regions. It follows that the outermost ring of lozenges propagate such tiling condition inwards, and so on and so forth. Therefore, there are statistically less ways to tile regions near the poles than ways to tile regions near the center. In other words, two randomly generated hexagons are likely to be similar in frozen (i.e., ordered) regions near the poles, and likely to differ in liquid (i.e., disordered) regions near the center.

## Problem

### Room generation

Let us consider a ```NxN``` room. The room is populated by stacking unit cubes. A legal room configuration is a particular arrangement of stacks that can loosely be defined as follows:

> An ant standing atop the stack tucked in the background corner of the room will never be able to climb up to a higher stack when traveling afar from the background corner.

From any legal room configuration, the rules to alter the stack of height ```z``` at position ```(x, y)``` are described hereafter.

A cube can be added to the stack if the two following conditions are met:

1. The stack contains strictly less than ```N``` cubes (namely, ```z<N```).
2. The two stacks adjacent in the background ```(x-1, y)``` and ```(x, y-1)``` each contain strictly more than ```z``` cubes.

A cube can be removed from the stack if the two following conditions are met:

1. The stack contains strictly more than ```0``` cubes (namely, ```z>0```).
2. The two stacks adjacent in the foreground ```(x+1, y)``` and ```(x, y+1)``` each contain strictly less than ```z``` cubes.

Two Boolean lookup tables are used to keep track of the coordinates where adding and/or removing a cube is legal. A flip operation, which can either lead to the addition or removal of a cube, is determined uniformly at random by drawing from the union of the two lookup tables. This process is iteratively repeated to randomly populate the room.

### Hexagon generation

The hexagon tiling is entirely determined by the room layout. Each lozenge corresponds to the projection of a visible cube face from the 3D room domain ```(x, y, z)``` to the 2D hexagon domain ```(i, j)```.

### Supporting illustration

![room_algorithm.jpg](../readme_images/room_algorithm.jpg?raw=true)

## Default configuration

### Parameters

```sh
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
```

### Expected console output
```sh
Room	| 3048/3048 (100.0%) 00:15:211
Fitness	| Monotony: True, Filling: 0.50732421875, Poles: (28, 47), (11, 38), (10, 35)
Hex	| 16/16 (100.0%) 00:01:512
```

### Expected hex and room patterns

![default_run.jpg](../readme_images/default_run.jpg?raw=true)

## Modules

- ```main.py```: Main script, used to define the parameters and run the experiment
- ```generate_room.py```: Routines to generate the room
- ```display_room.py```: Routines to display the room
- ```generate_and_display_hex.py```: Routines to generate and display the hex
- ```parameters.py```: Class that handles the parameters
- ```fitness.py```: Class that handles mechanisms to assess the room fitness
- ```utils.py```: Helper functions

## Experiments | Basics

### Initialization patterns

![initialization_patterns.jpg](../readme_images/initialization_patterns.jpg?raw=true)

```sh
N            = 8     # Room size
INI_PATTERN  = <...> # Indicate how the room shall be initialized, before random flips are applied
NB_ITER_FLIP = 0     # Number of random flips (if negative, will be reset to the total room volume)
```

### Five different runs: 12&times;12 room, one million random flips

![five_random_runs.jpg](../readme_images/five_random_runs.jpg?raw=true)

```sh
N            = 12            # Room size
INI_PATTERN  = 'random_half' # Indicate how the room shall be initialized, before random flips are applied
NB_ITER_FLIP = 10**6         # Number of random flips (if negative, will be reset to the total room volume)
```
## Experiments | Chasing the arctic circle

### Deterministic 84&times;84&times;84 arctic circle

![deterministic_arctic_circle.jpg](../readme_images/deterministic_arctic_circle.jpg?raw=true)

```sh
N            = 84              # Room size
INI_PATTERN  = 'arctic_circle' # Indicate how the room shall be initialized, before random flips are applied
NB_ITER_FLIP = 0               # Number of random flips (if negative, will be reset to the total room volume)
```

```sh
Fitness	| Monotony: True, Filling: 0.5, Poles: (903, 903), (903, 903), (903, 903)
```

### Three different runs: 128&times;128 room, 2,097,152 random flips

![three_random_runs.jpg](../readme_images/three_random_runs.jpg?raw=true)

```sh
N            = 128           # Room size
INI_PATTERN  = 'random_half' # Indicate how the room shall be initialized, before random flips are applied
NB_ITER_FLIP = -1            # Number of random flips (if negative, will be reset to the total room volume)
```

> It can be observed that all these three runs afford a sub-optimal arctic circle: despite the fact that the room filling is nearly 50%, there seems to be a systematic and marked imbalance between each pairs of opposed poles. It is currently hypothesized that the room state that is reached after the initialization phase parametrized by ```random_half``` prevents the subsequent alteration phase to afford a proper arctic circle pattern, even after applying more than two million random flips. A workaround is to initialize the room via the parameter value ```arctic_circle``` prior to the random alteration, but this would be a self-fulfilling prophecy.

## Experiments | For fun and giggles

### Initial pattern ```empty``` or ```full```, 128&times;128 room, one million random flips

![empty_or_full_then_one_million_random_flips.jpg](../readme_images/empty_or_full_then_one_million_random_flips.jpg?raw=true)

```sh
N            = 128           # Room size
INI_PATTERN  = 'random_half' # Indicate how the room shall be initialized, before random flips are applied
NB_ITER_FLIP = -1            # Number of random flips (if negative, will be reset to the total room volume)
```

### Iterative growth in an arbitrarily large room without floor and walls

![roomless_iterations.jpg](../readme_images/roomless_iterations.jpg?raw=true)

```sh
N                    = 150     # Room size
INI_PATTERN          = 'empty' # Indicate how the room shall be initialized, before random flips are applied
NB_ITER_FLIP         = <...>   # Number of random flips (if negative, will be reset to the total room volume)
DRAW_FLOOR_AND_WALLS = False   # Draw the floor and both walls of the room
```

### Color themes

![color_themes.jpg](../readme_images/color_themes.jpg?raw=true)

```sh
COLOR_THEME = <...> # Color theme
```
