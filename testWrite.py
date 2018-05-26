"""
Code that goes along with the Airflow tutorial located at:
https://github.com/apache/incubator-airflow/blob/master/airflow/example_dags/tutorial.py
"""

import os
import pickle



text =""" 
    import pickle
    from airflow.models import DAG
    
    with open({}, 'rb') as f:
        tmp_object = pickle.load(f)
        
    if isinstance(tmp_object,DAG):
            globals()[dag_tmp_name] = tmp_object
    del tmp_object
"""
print(text.format('Eg01.pkl'))
