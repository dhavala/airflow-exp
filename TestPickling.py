
import imp
from airflow.models import DAG




m = imp.load_source('crap', 'LoadPickledDags.py')

dag_bag = []
for index,dag in enumerate(list(m.__dict__.values())):
	if isinstance(dag, DAG):
		dag_bag.append(dag)

# we added atleast one example
assert len(dag_bag) >= 1


# at least one of them should have dag_id EgTrigger
ids = {dag.dag_id for dag in dag_bag if dag.dag_id == 'EgPickedDag_01'}
assert len(ids) == 1

# at least one of them should have have author soma
owner = {dag.owner for dag in dag_bag if dag.owner == 'soma'}
assert len(owner) == 1