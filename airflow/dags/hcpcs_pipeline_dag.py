import subprocess

import pendulum
from airflow.sdk import dag, task


PROJECT_DIR = "/opt/airflow/project"


def run_script(script_name):
    script_path = f"{PROJECT_DIR}/src/{script_name}"

    subprocess.run(
        ["python", script_path],
        cwd=PROJECT_DIR,
        check=True,
    )


def pipeline_failure_alert(context):
    """
    Called automatically when an Airflow task fails.
    """
    task_instance = context.get("task_instance")

    print("========================================")
    print("HCPCS PIPELINE FAILURE ALERT")
    print("========================================")

    if task_instance:
        print(f"Failed task: {task_instance.task_id}")
        print(f"DAG: {task_instance.dag_id}")
        print(f"Run ID: {task_instance.run_id}")

    print("Please check the Airflow task logs for details.")
    print("========================================")


@dag(
    dag_id="hcpcs_pipeline",
    schedule="@daily",
    start_date=pendulum.datetime(2026, 10, 1, tz="UTC"),
    catchup=False,
    tags=["hcpcs", "data-engineering"],
    on_failure_callback=pipeline_failure_alert,
)
def hcpcs_pipeline():

    @task
    def extract():
        print("Starting HCPCS extraction...")
        run_script("extract.py")
        print("HCPCS extraction completed.")

    @task
    def transform():
        print("Starting HCPCS transformation...")
        run_script("transform.py")
        print("HCPCS transformation completed.")

    @task
    def load():
        print("Starting HCPCS load...")
        run_script("load.py")
        print("HCPCS load completed.")

    @task
    def validate():
        print("Starting HCPCS data validation...")
        run_script("validate.py")
        print("HCPCS validation completed.")

    @task
    def notify():
        print("========================================")
        print("HCPCS PIPELINE COMPLETED SUCCESSFULLY")
        print("========================================")

        print("Extract -> Transform -> Load -> Validate -> Notify")

        print("Pipeline monitoring metrics:")
        print("- Rows loaded: tracked in pipeline_metrics")
        print("- Last successful timestamp: tracked in pipeline_metrics")
        print("- DQ failures: tracked in pipeline_metrics")

    extract_task = extract()
    transform_task = transform()
    load_task = load()
    validate_task = validate()
    notify_task = notify()

    extract_task >> transform_task >> load_task >> validate_task >> notify_task


hcpcs_pipeline()
