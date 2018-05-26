
import imp
from airflow.models import DAG


m = imp.load_source('crap', 'LoadPickledDags.py')

for index,dag in enumerate(list(m.__dict__.values())):
	if isinstance(dag, DAG):
		print(index,dag)