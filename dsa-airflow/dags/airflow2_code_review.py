# Import necessary libraries
import os
import datetime
import pandas as pd
from airflow import DAG
from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor
from airflow.hooks.filesystem import FSHook

flavor_choices = ["lemon", "vanilla", "chocolate", "pistachio", "strawberry", "confetti", "caramel", "pumpkin", "rose"]