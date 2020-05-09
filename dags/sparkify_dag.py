from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (
    StageToRedshiftOperator,
    LoadFactOperator,
    LoadDimensionOperator,
    DataQualityOperator,
)
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

# Arguments to be used on the DAG
default_args = {
    "owner": "udacity",
    "start_date": datetime(2019, 1, 12),
    # "end_date": datetime(2019, 1, 2),
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "catchup": False,
    "email_on_retry": False,
}

# DAG instance
dag = DAG(
    "sparkify_dag",
    default_args=default_args,
    description="Load and transform data in Redshift with Airflow",
    schedule_interval="0 * * * *",
    # max_active_runs=2,
)

# First task to run, does nothing
start_operator = DummyOperator(task_id="Begin_execution", dag=dag)

# Tasks to load data from s3 to redshift

stage_events_to_redshift = StageToRedshiftOperator(
    task_id="Stage_events",
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_events",
    s3_bucket="udacity-dend",
    s3_key="log_data",
    json_path="s3://udacity-dend/log_json_path.json",
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id="Stage_songs",
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    table="staging_songs",
    s3_bucket="udacity-dend",
    s3_key="song_data",
    json_path="auto",
)

# Load data into fact table
load_songplays_table = LoadFactOperator(
    task_id="Load_songplays_fact_table",
    dag=dag,
    redshift_conn_id="redshift",
    fact_table="songplays",
    select_sql=SqlQueries.songplay_table_insert,
)

# Load data into dimension tables
load_user_dimension_table = LoadDimensionOperator(
    task_id="Load_user_dim_table",
    dag=dag,
    redshift_conn_id="redshift",
    dimension_table="users",
    select_sql=SqlQueries.user_table_insert,
    truncate=True,
)

load_song_dimension_table = LoadDimensionOperator(
    task_id="Load_song_dim_table",
    dag=dag,
    redshift_conn_id="redshift",
    dimension_table="songs",
    select_sql=SqlQueries.song_table_insert,
    truncate=True,
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id="Load_artist_dim_table",
    dag=dag,
    redshift_conn_id="redshift",
    dimension_table="artists",
    select_sql=SqlQueries.artist_table_insert,
    truncate=True,
)

load_time_dimension_table = LoadDimensionOperator(
    task_id="Load_time_dim_table",
    dag=dag,
    redshift_conn_id="redshift",
    dimension_table="time",
    select_sql=SqlQueries.time_table_insert,
    truncate=True,
)

#Execute tasks for quality checks

run_quality_checks = DataQualityOperator(
    task_id="Run_data_quality_checks",
    dag=dag,
    redshift_conn_id="redshift",
    tables=["songplays", "users", "songs", "artists", "time"],
)

# End of tasks execution
end_operator = DummyOperator(task_id="Stop_execution", dag=dag)

"""
    Execution order for tasks:
"""
start_operator >> stage_events_to_redshift
start_operator >> stage_songs_to_redshift

stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table

load_songplays_table >> [
    load_song_dimension_table,
    load_user_dimension_table,
    load_artist_dimension_table,
    load_time_dimension_table,
] >> run_quality_checks >> end_operator
