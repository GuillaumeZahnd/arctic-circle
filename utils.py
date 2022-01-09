import math


# ----------------------------------------------------------------
# Express the elapsed time as a string detailing minutes, seconds, and microseconds
# ----------------------------------------------------------------
def stopwatch(time_now, time_ini):
  time_native = time_now - time_ini
  time_minutes = int(time_native // 60)
  time_seconds = int(time_native % 60)
  time_milliseconds = int(1000*(time_native - math.floor(time_native)))
  elapsed_time = str(time_minutes).zfill(2) + ':' + str(time_seconds).zfill(2) + ':' + str(time_milliseconds).zfill(3)
  return elapsed_time


# ----------------------------------------------------------------
# Print the progression in the console
# ----------------------------------------------------------------
def print_iter_msg(msg, iterx, nb_iter, time_now, time_ini):

  if iterx > 0:
    replace_previous_line = '\033[F\033[K' # (go up one line and clear until the end of the line)
  else:
    replace_previous_line = ''

  percentage = 100 * (iterx) / max(nb_iter, 1) # (enable cases with zero iterations)

  elapsed_time = stopwatch(time_now, time_ini)
  print('{}{}\t| {}/{} ({}%) {}'.format(
    replace_previous_line,
    msg,
    iterx,
    nb_iter,
    percentage,
    elapsed_time))
