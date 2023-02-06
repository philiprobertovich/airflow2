# Import necessary libraries
import os
import datetime
import pandas as pd
from collections import Counter
from airflow import DAG
from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor
from airflow.hooks.filesystem import FSHook

# Global variable for votes file
VOTES_FILE = "votes.csv"

# list of flavors
flavor_choices = ["lemon", "vanilla", "chocolate", "pistachio", "strawberry", "confetti", "caramel", "pumpkin", "rose"]

@task
def read_file() -> None:
  """
  Read the votes CSV file
  """
  # get the data_fs filesystem root path
  data_fs = FSHook(conn_id='data_fs')
  # get the airflow connection for data_fs
  data_dir = data_fs.get_path()
  print(f"data_fs root path: {data_dir}")

  # create the full path to votes file
  file_path = os.path.join(data_dir, VOTES_FILE)

  # Use pandas to read to CSV
  df = pd.read_csv(file_path, header=1)
  return df

@task
def parse_records(df) -> list:
  """
  This function will go through each value of the votes file, see if it is within the flavor_choices list, and if so, it will append it to a new valid_votes list and return it
  """
  valid_votes = []
  for record in df['votes']:
    for flavor in flavor_choices:
      if record == flavor:
        valid_votes.append(record)
  return valid_votes

@task
def count_votes(valid_votes):
  votes_dict = Counter(valid_votes)
  max_value = max(votes_dict.values())
  max_key = max(votes_dict, key=votes_dict.get)
  print(f"{max_key} - {max_value}")


