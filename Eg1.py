"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/incubator-airflow/blob/master/airflow/example_dags/tutorial.py
"""
from datetime import datetime, timedelta, date
import os
import pickle
import textwrap

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

# depreciated
def push_pickled_dag_to_folder(dag,dag_folder_path=''):
    
    if not dag_folder_path:
        dag_folder_path = ''.join([os.environ['AIRFLOW_HOME'],'/dags/'])
    
    dag_pkl_name = ''.join([dag_folder_path,dag.dag_id,'.pkl'])
    
    with open(dag_pkl_name,'wb') as f:
        pickle.dump(dag,f,pickle.HIGHEST_PROTOCOL)


def register_pickled_dag(dag,dag_folder_path=''):
    
    """
    Registers (pushes) an airflow dag object to its dag folder, along with python script that
    can load the pickled dag into memory. Name of the pickled dag and its reader py script will
    have the 'dag' as its name with the prefix "auto_"

    Inputs:
    dag: an airflow dag object
    dag_folder_path='': If empty, pickled dag objects will be saved into
    airflow's default dag folder
    """

    # set fileloc so that WebUi shows the pickle reader
    dag.fileloc = dag._full_filepath
    dag.sync_to_db()

    dag_name = ''.join(['auto_',dag.dag_id])
    
    if not dag_folder_path:
        dag_folder_path = ''.join([os.environ['AIRFLOW_HOME'],'/dags/'])
    
    dag_pkl_name = ''.join([dag_folder_path,dag_name,'.pkl'])
    dag_pyfile_name = ''.join([dag_folder_path,dag_name,'.py'])
    
    with open(dag_pkl_name,'wb') as f:
        pickle.dump(dag,f,pickle.HIGHEST_PROTOCOL)

    pyscript = """
    import pickle
    from airflow.models import DAG
    
    with open('{}', 'rb') as f:
        tmp_object = pickle.load(f)
        
    if isinstance(tmp_object,DAG):
        tmp_object.fileloc = tmp_object._full_filepath
        globals()['{}'] = tmp_object
    del tmp_object
    """
    pyscript = pyscript.format(dag_pkl_name,dag_name)
    dedented_pyscript = textwrap.dedent(pyscript).strip()

    with open(dag_pyfile_name,'w') as f:
        f.write(dedented_pyscript)



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

#push_pickled_dag_to_folder(dag)
register_pickled_dag(dag)