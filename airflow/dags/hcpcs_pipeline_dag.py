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


@dag(
    dag_id="hcpcs_pipeline",
    schedule="@daily",
    start_date=pendulum.datetime(2026, 10, 1, tz="UTC"),
    catchup=False,
    tags=["hcpcs", "data-engineering"],
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
        print("HCPCS pipeline completed successfully.")
        print("Extract -> Transform -> Load -> Validate -> Notify")

    extract_task = extract()
    transform_task = transform()
    load_task = load()
    validate_task = validate()
    notify_task = notify()

    extract_task >> transform_task >> load_task >> validate_task >> notify_task


hcpcs_pipeline()
