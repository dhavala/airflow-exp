__airflow__ expects you to declare your DAG objects via .py files in a particular folder. __airflow__ scans and loads the .py files and looks for any DAG objects available in the global scope, and then adds them to its DagBag. Its schedulers will scan DagBag and trigger any jobs that need to be run.

However, in some cases, you might have created DAG objects programmatically, not declaratively (in python) as airflow expects. That means that, you have a valid DAG object already created but in order for that DAG object to be made availbale, you have to inject them via py code.

Since we already have a valid DAG object, we can simply pickle them, place those pickled DAG objects in the default folder, and a have colocated .py script that can load the picked DAG objects into memory. Basically, pickled DAG objects have to made available to __airflow__ via a .py file.

### Approach - 1

1. Have this helper function [in Eg1.py](https://github.com/dhavala/airflow-exp/blob/master/Eg1.py) to save/push your DAG object to the default DAG folder. It will save a pickle file along with reader script. The script will be picked up by airflow when it scans new DAGs in that folder
```python
def register_pickled_dag(dag,dag_folder_path=''):
    
    """
    registers (pushes) an airflow dag object to its dag folder, along with python script that
    can load the pickled dag into memory. name of the pickled dag and its reader py script will
    have have the dag as its name with a "auto_"

    Inputs:
    dag: an airflow dag object
    dag_folder_path='': If empty, pickled dag objects will be saved into
    airflow's default dag folder
    """

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
            globals()['{}'] = tmp_object
    del tmp_object
    """
    pyscript = pyscript.format(''.join([dag_name,'.pkl']),dag_name)
    dedented_pyscript = textwrap.dedent(pyscript).strip()

    with open(dag_pyfile_name,'w') as f:
        f.write(dedented_pyscript)
```

2. pickle and save your dag
```python
register_pickled_dag(dag)
```


### Approach - 2


1. Have this helper function to save/push your DAG object to the default DAG folder
```python
def push_pickled_dag_to_folder(dag,dag_folder_path=''):
    
    if not dag_folder_path:
        dag_folder_path = ''.join([os.environ['AIRFLOW_HOME'],'/dags/'])
    
    dag_pkl_name = ''.join([dag_folder_path,dag.dag_id,'.pkl'])
    
    with open(dag_pkl_name,'wb') as f:
        pickle.dump(dag,f,pickle.HIGHEST_PROTOCOL)

```
2. pickle and save your dag
```python
push_pickled_dag_to_folder(dag)
```
3. place __LoadPickledDags.py__ in defualt dag folder
```python
# this file has to be placed in airflow dags folder

import pickle
import glob

from airflow.models import DAG

pickled_dags = glob.glob('*.pkl')

for pickled_dag in pickled_dags:
	
  dag_tmp_name  = ''.join(['dag_',pickled_dag,str(index)])
	
  with open(pickled_dag, 'rb') as f:
    tmp_object = pickle.load(f)
		
  if isinstance(tmp_object,DAG):
      globals()[dag_tmp_name] = tmp_object
  del tmp_object
```

You are set. Now the saved DAGs will be available to the DagBag. It is not cleanest way, but at least, we dont've to generate py code with exec and eval staements and re-creating the DAG logic again. 

Known Issue:
Notice however, that these DAGs will not show up proper in Web UI. They appear under DAG/Task Runs but not clicable (under Approach 1). But code view is not available. 

It would have been nicer, if were we able to directly push DAG objects into the DB without having to the hacky-way.