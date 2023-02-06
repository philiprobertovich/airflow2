# Import necessary libraries
import os
import datetime
import pandas as pd
from airflow import DAG
from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor
from airflow.hooks.filesystem import FSHook

# Global variable for votes file
VOTES_FILE = "votes.csv"

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

  # create the full path to votes file
  file_path = os.path.join(data_dir, VOTES_FILE)

  # Use pandas to read to CSV
  df = pd.read_csv(file_path, header=1)


flavor_choices = ["lemon", "vanilla", "chocolate", "pistachio", "strawberry", "confetti", "caramel", "pumpkin", "rose"]