"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/incubator-airflow/blob/master/airflow/example_dags/tutorial.py
"""
from datetime import datetime, timedelta, date
import os
import pickle


from airflow.models import (DagModel, DagBag, TaskInstance,
                            DagPickle, DagRun, Variable, DagStat,
                            Connection, DAG)
from airflow.settings import Session
from airflow.utils.state import State

from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

from airflow import settings
#from airflow.bin.cli import get_num_ready_workers_running, run, get_dag
from airflow.models import TaskInstance
#from airflow.utils import timezone
from airflow.utils.state import State
from airflow.settings import Session
from airflow import models


def push_pickled_dag_to_folder(dag,dag_folder_path=''):
    
    if not dag_folder_path:
        dag_folder_path = ''.join([os.environ['AIRFLOW_HOME'],'/dags/'])
    
    dag_pkl_name = ''.join([dag_folder_path,dag.dag_id,'.pkl'])
    
    with open(dag_pkl_name,'wb') as f:
        pickle.dump(dag,f,pickle.HIGHEST_PROTOCOL)


now = date.today()
day_before = now - timedelta(2)

default_args = {
        'owner': 'soma',
        'depends_on_past': False,
        'start_date': datetime(day_before.year, day_before.month, day_before.day),
        #'start_date': datetime(2018,2,5)
    }

dag = DAG('EgPickedDag_01', default_args=default_args,schedule_interval='@once')

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command="date",
    dag=dag)

t2  = DummyOperator(task_id='task2', dag=dag)

t3  = DummyOperator(task_id='task3', dag=dag)

push_pickled_dag_to_folder(dag)