# Import necessary libraries
import os
from datetime import datetime
import pandas as pd
from collections import Counter
# from airflow import DAG
from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor
from airflow.hooks.filesystem import FSHook

# # get the data_fs filesystem root path
# data_fs = FSHook(conn_id='data_fs')
# # get the airflow connection for data_fs
# data_dir = data_fs.get_path()
# # print(f"data_fs root path: {data_dir}")

# # create the full path to votes file
# VOTES_FILE = os.path.join(data_dir, 'votes.csv')

# Global variable for votes file
VOTES_FILE = "votes.csv"

# list of flavors
flavor_choices = ["lemon", "vanilla", "chocolate", "pistachio", "strawberry", "confetti", "caramel", "pumpkin", "rose"]

@task
def read_file():
  """
  Read the votes CSV file
  """
  # get the data_fs filesystem root path
  data_fs = FSHook(conn_id='data_fs')
  # get the airflow connection for data_fs
  data_dir = data_fs.get_path()
  print(f"data_fs root path: {data_dir}")

  # # create the full path to votes file
  file_path = os.path.join(data_dir, VOTES_FILE)

  # Use pandas to read to CSV
  df = pd.read_csv(file_path, header=1)
  return df

@task
def parse_records(df):
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

@dag(
  schedule_interval="@once",
  start_date=datetime.utcnow(),
  catchup=False,
  default_view='graph',
  is_paused_upon_creation=True
)
def read_file_count_votes():
  """
  Putting all the task together to read the votes CSV and count the votes
  """ 

  # Waits for votes file to be the data_fs filesystem connection
  wait_for_file = FileSensor(
    task_id="wait_for_file",
    poke_interval=15,
    timeout=(30 * 60),
    mode="poke",
    filepath=VOTES_FILE,
    fs_conn_id="data_fs"
  )

  # Set tasks
  read_file_task = read_file()

  parse_recs_task = parse_records(read_file_task)

  count_votes_task = count_votes(parse_recs_task)

  # Task order 
  wait_for_file >> read_file_task >> parse_recs_task >> count_votes_task

# create dag
dag =  read_file_count_votes()