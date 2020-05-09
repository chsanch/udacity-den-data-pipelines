# Data Pipelines (Udacity Nanodegree Project)

## Introduction

A music streaming company, Sparkify, has decided that it is time to introduce
more automation and monitoring to their data warehouse ETL pipelines and come to
the conclusion that the best tool to achieve this is Apache Airflow.

## Project

### Requirements
- Create Redshift cluster in AWS
- Create the tables in the databese using: create_tables.py
- Open the Airflow UI and add your connection details (aws_credentials,
  redshift)

### Pipeline execution

The following task will be executed:
- Load data from S3 to Redshift (stage_events_to_redshift,
  stage_songs_to_redshift)
- Load data from staging tables to fact table (load_songplays_table)
- Load data from fact table to dimension tables (load_song_dimension_table,
  load_user_dimension_table, load_artist_dimension_table,
  load_time_dimension_table,)
- Execute a task to check quality of data (run_quality_checks)



