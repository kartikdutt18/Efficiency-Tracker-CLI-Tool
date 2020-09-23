#!/usr/bin/python3

import matplotlib.pyplot as plt
from datetime import date
import pandas as pd
import argparse
from cfg import *
from utils import *

def AddEfficiency(completed_tasks : int, total_tasks : int) :
  """
    Writes to cached file.
    Args :
    completed_tasks : Tasks completed.
    total_tasks : Total Tasks.
  """

  cached_csv = None
  if (os.path.exists(WRITE_PATH)):
    cached_csv = pd.read_csv(WRITE_PATH)
  else :
    cached_csv = pd.DataFrame(columns=[DATE_IDENTIFIER, COMPLETION_IDENTIFIER])

  if (len(cached_csv) > 0) :
    if (cached_csv[DATE_IDENTIFIER][len(cached_csv[DATE_IDENTIFIER]) - 1] == str(date.today())) :
      cached_csv.drop(cached_csv.tail(1).index, inplace = True)

  df = pd.DataFrame([[str(date.today()), 100 * (completed_tasks / total_tasks)]],
      columns = [DATE_IDENTIFIER, COMPLETION_IDENTIFIER])

  cached_csv = cached_csv.append(df)
  cached_csv.to_csv(WRITE_PATH, index = False)
  print(cached_csv)

def Plot(look_back : int) :
  if (not os.path.exists(WRITE_PATH)) :
    AddEfficiency(0, 1)

  cached_csv = pd.read_csv(WRITE_PATH)
  cached_csv = cached_csv.tail(look_back)
  cached_csv.plot(x = DATE_IDENTIFIER, y = COMPLETION_IDENTIFIER, kind = 'line')
  plt.show()


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Track your efficiency daily.')
  parser.add_argument("completed_tasks", type=int)
  parser.add_argument("--total_tasks", type=int, default=DEFAULT_TASKS)
  parser.add_argument("--look_back", type = int, default = 7)
  args = parser.parse_args()
  AddEfficiency(args.completed_tasks, args.total_tasks)
  Plot(args.look_back)


