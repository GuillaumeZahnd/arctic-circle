import numpy as np


class Fitness:

  def __init__(
    self,
    ):

    self.monotony = None
    self.filling = None
    self.x_full  = None
    self.x_empty = None
    self.y_full  = None
    self.y_empty = None
    self.z_full  = None
    self.z_empty = None


  # ----------------------------------------------------------------
  # Assess the room fitness via several patterns and mechanisms
  # ----------------------------------------------------------------
  def assess_room_fitness(self, room, N):

    # Verify whether the monotony condition is respected
    monotony_x = not np.any(np.diff(room, axis=1) > 0)
    monotony_y = not np.any(np.diff(room, axis=0) > 0)
    self.monotony = monotony_x and monotony_y

    # A perfect arctic-circle corresponds to a room that is exactly half-full (or half-empty?), when N is even
    self.filling = np.sum(room) / N**3

    # Measure the area of the six "poles" of the hex: in case of a perfect arctic circle, all poles have the same area
    self.x_full  = np.sum(room[:, N-1])
    self.x_empty = N**2 - np.sum(room[:, 0])
    self.y_full  = np.sum(room[N-1, :])
    self.y_empty = N**2 - np.sum(room[0, :])
    self.z_full  = np.sum(room == N)
    self.z_empty = np.sum(room == 0)
