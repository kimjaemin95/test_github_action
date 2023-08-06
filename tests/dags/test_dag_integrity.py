"""Test integrity of DAGs."""

import glob
import importlib.util
import os

import pytest
from airflow.models import DAG
from airflow.utils.dag_cycle_tester import check_cycle


# ../../dags/**.py
DAG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dags/**.py")
# ['../../dags/bash_operator_no_command.py', '../../dags/test_dag_cycle.py', '../../dags/duplicate_task_ids.py', '../../dags/testme.py']
DAG_FILES = glob.glob(DAG_PATH)


@pytest.mark.parametrize("dag_file", DAG_FILES)
def test_dag_integrity(dag_file):
    """Import DAG files and check for DAG."""
    module_name, _ = os.path.splitext(dag_file)
    print(f"module_name: {module_name}")
    module_path = os.path.join(DAG_PATH, dag_file)
    print(f"module_path: {module_path}")
    mod_spec = importlib.util.spec_from_file_location(module_name, module_path)
    print(f"mod_spec: {module_name}")
    module = importlib.util.module_from_spec(mod_spec)
    print(f"module: {module}")
    mod_spec.loader.exec_module(module)

    dag_objects = [var for var in vars(module).values() if isinstance(var, DAG)]
    print(f"dag_objects: {dag_objects}")
    assert dag_objects

    for dag in dag_objects:
        # Test cycles
        # dag.test_cycle()
        check_cycle(dag)