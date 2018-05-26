# this file has to be placed in airflow dags folder

import pickle
import glob

from airflow.models import DAG

pickled_dags = glob.glob('*.pkl')

for index, pickled_dag in enumerate(pickled_dags):
	dag_tmp_name  = ''.join(['dag_',pickled_dag,str(index)])
	
	print(index,pickled_dag)
	
	with open(pickled_dag, 'rb') as f:
		tmp_object = pickle.load(f)
		
	if isinstance(tmp_object,DAG):
			globals()[dag_tmp_name] = tmp_object
			del tmp_object


