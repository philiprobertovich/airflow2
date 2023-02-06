# Airflow Week 2

### By Philip Kendall

#### This project sets up a number of tasks using Airflow while utilizing key Airflow concepts such as Decorators, Xcoms, and Sensors.
## Technologies Used

* GIT
* Python 3.7
* Airflow 2.3.2
* Docker


## Description
The pipeline created for this project first uses a sensor task to check for a votes.csv file. After it is found, the next task is to read the file and turn it into a dataframe. The next task takes the dataframe and iterates through each record to see if the value of that record matches one with a list called flavor_choices. If there is a match, that value is appended to a new list called valid_votes, which is then what the task returns. The following task recieves the information of that returned list via Airflow's Xcoms and then counts the values and returns that value with the highest amount of votes.


## Setup/Installation Requirements

* Fork over the the repository to your own Github account.
* Clone your Github repo down to your local machine and into the directory you would like this project to be stored.
* Create a virtual environment:
  ```
  python3.7 -m venv venv
  ```

* Install the requirements.txt file:
  ```
  pip install -r requirements.txt
  ```

* Navigate to the dsa-airflow directory and use the curl command to download the latest docker-compose.yaml file
  ```
  cd dsa-airflow
  curl -LfO "https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml"
  ```
* Set the .env file
  ```
  echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
  ```
* Create directories for logs and plugins:
  ```
  mkdir ./logs ./plugins ./data
  ```
* Modify the docker-compose.yaml file under the volumes section so that it includes a mounted conneciton to the data/ folder. It should resemble what's bellow:
  ```
  volumes:
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins
    - ${AIRFLOW_PROJ_DIR:-.}/data:/data
  ```
* To get the votes.csv files, execute the following command:
  ```
  gsutil -m cp gs://data.datastack.acadaemy/airflow_cr_2/votes.csv ./data
  ```
* Initialize Airflow with the docker compose up command:
  ```
  docker-compose up airflow-init
  ```
* Once Airflow is initialized, docker compoese up to run Airflow.
  ```
  docker-compose up
  ```
* Navigate to localhost:8080/home in your browser and enter the Airflow credentials. Both username and password should be "airflow".
* A connection to the sensor must be established, and can be done so through the GUI. Navigate to Admins > Connections and create a new conneciton. 
* Find "airflow2_code_review" under the DAG column and unpause the DAG.
* After that, the DAG should run. Click on "airflow2_code_review" to see the different views of the DAG's execution.

## Known Bugs

N/A

## License

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The below copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Copyright (c) 2023 Philip Kendall