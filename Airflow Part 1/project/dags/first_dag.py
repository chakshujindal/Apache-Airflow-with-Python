try:

    from datetime import timedelta
    from datetime import datetime
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    import pandas as pd
    print("All Dag modules are ok ......")

except Exception as e:
    print("Error {} ".format(e))

def zeroth_function_execute(*args, **kwargs):
    variable = kwargs.get("name", "Didn't get the key")
    print("zeroth_function_execute => Hello World :{}".format(variable))
    return "Hello World " + variable
def first_function_execute(**context):
    print("first_function_execute =>")
    context["ti"].xcom_push(key='mykey', value="first_function_execute says Hello")

def second_function_execute(**context):
    instance = context.get("ti").xcom_pull(key='mykey')
    data = [{"name": "Chakshu", "title": "Software Engineer"}, {"name": "Vanshika", "title": "Embedded Engineer"}]
    df = pd.DataFrame(data=data)
    print('@'*66)
    print(df.head())
    print('@'*66)

    print("second_function_execute => got value :{} from First Function".format(instance))

# */2 * * * * Execute every Two Minutes
with DAG(
        dag_id = "first_dag",#dag_is to be same as file name
        schedule_interval = "@daily",
        default_args={
            "owner": "airflow",
            "retries": 1,
            "retry_delay": timedelta(minutes=5),
            "start_date": datetime(2023, 5, 1)
        },
        catchup=False) as f:
    zeroth_function_execute = PythonOperator(
        task_id="zeroth_function_execute",
        python_callable=zeroth_function_execute,
        op_kwargs = {"name": "Chakshu Jindal"}
    )

    first_function_execute = PythonOperator(
        task_id="first_function_execute",
        python_callable=first_function_execute,
        provide_context=True,
        op_kwargs = {"name": "Chakshu Jindal"}
    )

    second_function_execute = PythonOperator(
        task_id="second_function_execute",
        python_callable=second_function_execute,
        provide_context=True
    )

first_function_execute >> second_function_execute