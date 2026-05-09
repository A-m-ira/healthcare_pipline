from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="HEALTHCARE_ETL_PIPELINE",
    start_date=datetime(2024, 6, 1),
    schedule=None,
    catchup=False
) as dag:

    # -------------------------
    # 1. EXTRACT (Spark -> Bronze)
    # -------------------------
    task1 = BashOperator(
        task_id="extract_healthcare_data",
        bash_command=(
            "docker exec spark-jupyter spark-submit "
            "/home/jovyan/work/bronze_ingestion.py"
        )
    )

    # -------------------------
    # 2. ARCHIVE RAW DATA (local JSONs - optional)
    # -------------------------
    task2 = BashOperator(
        task_id="archive_raw_data",
        bash_command=(
            "docker exec spark-jupyter sh -c "
            "'mv /home/jovyan/work/data/raw_healthcare_pings/*.json "
            "/home/jovyan/work/data/processed_healthcare_pings/ || true'"
        )
    )

    # -------------------------
    # 3. TRANSFORMATION (Bronze -> Gold Star Schema)
    # -------------------------
    task3 = BashOperator(
        task_id="transform_star_schema",
        bash_command=(
            "docker exec spark-jupyter spark-submit "
            "/home/jovyan/work/gold_transform.py"
        )
    )

    # -------------------------
    # 4. ARCHIVE HDFS BRONZE DATA
    # -------------------------
    task4 = BashOperator(
        task_id="archive_hdfs_data",
        bash_command=(
            "docker exec hadoop-namenode sh -c "
            "'hdfs dfs -mkdir -p /user/root/datalake/bronze/archive && "
            "hdfs dfs -mv /user/root/datalake/bronze/healthcare/*.parquet "
            "/user/root/datalake/bronze/archive/ || true'"
        )
    )

    # -------------------------
    # 5. LOAD TO SNOWFLAKE
    # -------------------------
    task5 = BashOperator(
        task_id="load_to_snowflake",
        bash_command=(
            "docker exec spark-jupyter spark-submit "
            "--packages net.snowflake:snowflake-jdbc:3.13.22,"
            "net.snowflake:spark-snowflake_2.12:2.12.0-spark_3.3 "
            "/home/jovyan/work/snowflake_loader.py"
        )
    )

    # -------------------------
    # PIPELINE ORDER
    # -------------------------
    task1 >> task2 >> task3 >> task4 >> task5