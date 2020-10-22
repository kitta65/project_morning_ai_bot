import sys
from morning_ai_bot_package.morning_ai_bot_common import *
from morning_ai_bot_package.morning_ai_bot_config import *


dag = DAG(
    'morning_ai_bot_daily_BUILD_ID',
    default_args=common_args,
    description='call funtion mornin_ai_bot',
    schedule_interval="40 13 *  *  *",
)

task1 = PythonOperator(
    task_id='morning_ai_bot',
    python_callable=exec_functions,
    provide_context=True,
    op_kwargs={
        "url": "https://us-central1-{}.cloudfunctions.net/morning_ai_bot".format(GCP_PROJECT),
        "token": LINE_TOKEN
    },
    dag=dag,
)
task1 # >> task2
