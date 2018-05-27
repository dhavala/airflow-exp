import pickle
from airflow.models import DAG

with open('./auto_EgPickedDag_01.pkl', 'rb') as f:
    tmp_object = pickle.load(f)

if isinstance(tmp_object,DAG):
    tmp_object.fileloc = tmp_object._full_filepath
    globals()['auto_EgPickedDag_01'] = tmp_object
del tmp_object