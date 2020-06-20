#!/bin/bash
cd $(dirname $0)
cd ./dags
zip -r $HOME/airflow/dags/morning_ai_bot *
cd $(dirname $0)
