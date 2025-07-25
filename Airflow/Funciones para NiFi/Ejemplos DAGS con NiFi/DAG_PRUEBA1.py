from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator
from airflow.hooks.base import BaseHook
from airflow.operators.python_operator import PythonOperator

from datetime import timedelta
from textwrap import dedent
import pendulum
import json
import logging

import davila_functions.nifi.principal as funciones_nifi


TAGS = ["prueba"]
DAG_ID = 'DAG_PRUEBA1'
DAG_DESCRIPTION = 'DAG prueba'

# que empiece a las 8,10,12,14,16 en horario UTC -3 (santiago de chile)
DAG_SCHEDULE =  None
START_VAR = pendulum.datetime(2025, 1, 27, tz="America/Santiago")

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Diego Avila',
    'depends_on_past': False,
    'email': ['davila@cramer.cl'],
    'email_on_failure': False,
    'email_on_retry': False, 
    'retries': 2, # 0 para que no reintente
    'catchup': False, # false para que no ejecute tareas anteriores
    'retry_delay': timedelta(minutes=1),
    'max_active_runs' : 1,
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
# [END default_args]


# [START instantiate_dag]


# Obtener el token de autenticación de nifi
def get_credentials():
    conn = BaseHook.get_connection('apache_nifi_linux')  # Obtener conexión
    extra = json.loads(conn.extra)  # Leer credenciales almacenadas
    return extra,extra.get("username"), extra.get("password")

extra,username, password = get_credentials()
url_nifi_api = "https://<IP SERVER>:8443/nifi-api/"  # e.g. retrieve via Airflow's `BaseHook` functionality

access_payload = {
"username": username,
"password": password,
    }

token = funciones_nifi.get_token(url_nifi_api, access_payload, verify=False)


# Definir funciones Python

def startup(id_processor):
    """ Inicia el flujo inicial de NiFi.   
    @DAVILA 24-07-2025
    Esta función inicia el procesador inicial y luego lo detiene,
    ya que no es necesario que siga corriendo una vez que se ha iniciado el flujo.
    Se utiliza para preparar el flujo de trabajo de NiFi antes de ejecutar otras tareas.
    :return: None
    """
    logging.info("Starting initial processor to trigger NiFi flow...")
    # 1. Iniciar el procesador inicial para que comience el flujo de NiFi
    running_processor = funciones_nifi.update_processor_status(id_processor, "RUNNING", token, url_nifi_api, verify=False)
    logging.info(f"{running_processor.status_code} - {running_processor.reason} Processor started")
    
    # Esperar 15 segundos para que el flujo se inicie
    # Esto es necesario para que el flujo de NiFi tenga tiempo de procesar la solicitud y generar los FlowFiles necesarios.
    funciones_nifi.pause(15)

    # 2. Detener el procesador inicial, ya que no es necesario que siga corriendo
    stopped_processor = funciones_nifi.update_processor_status(id_processor, "STOPPED", token, url_nifi_api)
    logging.info(f"{stopped_processor.status_code} - {stopped_processor.reason} Processor stopped")
        

def prepare_processor_state(id_processor,name_variable):
    """ Prepara los procesadores de NiFi para el flujo de trabajo.
    @DAVILA 24-07-2025
    Esta función detiene el procesador con la variable name_variable,
    limpia su estado y luego lo reinicia para que esté listo para el flujo de trabajo.
    :param id_processor: ID del procesador a preparar.
    :param name_variable: Nombre de la variable que se utilizará en el procesador.
    :return: None
    """
    # 1. Detener el procesador con la variable name_variable
    stopped_processor = funciones_nifi.update_processor_status(id_processor, "STOPPED", token, url_nifi_api)
    logging.info(f"{stopped_processor.status_code} - {stopped_processor.reason} Processor with variable {name_variable} stopped")
    # 2. Limpiar el estado del procesador para reiniciar la variable
    clear_processor = funciones_nifi.clear_processor_state(url_nifi_api, id_processor, token, verify=False)
    logging.info(f"{clear_processor.status_code} - {clear_processor.reason} Processor with variable {name_variable} state cleared")
    # 3. Iniciar el procesador con la variable name_variable
    running_processor = funciones_nifi.update_processor_status(id_processor, "RUNNING", token, url_nifi_api, verify=False)
    logging.info(f"{running_processor.status_code} - {running_processor.reason} Processor with variable {name_variable} started")

def prepare_counter(*id_counters, **kwargs):
    """ Prepara el contador de NiFi para el flujo de trabajo.
    @DAVILA 24-07-2025
    Esta función reinicia el contador con el ID id_counter para que esté listo para el flujo de trabajo.
    :param *id_counters: IDs de los contadores a preparar.
    :param **kwargs: Para compatibilidad con llamadas usando id_counters=
    :return: None
    """
    # Si se pasa como keyword argument
    if 'id_counters' in kwargs:
        if isinstance(kwargs['id_counters'], list):
            counters_to_process = kwargs['id_counters']
        else:
            counters_to_process = [kwargs['id_counters']]
    else:
        counters_to_process = id_counters
    
    for id_counter in counters_to_process:
        # 1. Reiniciar el contador con el ID id_counter
        reset_counter = funciones_nifi.reset_counter(url_nifi_api, id_counter, token, verify=False)
        logging.info(f"{reset_counter.status_code} - {reset_counter.reason} Counter with ID {id_counter} reset")


def wait_for_update_state_processor(id_processor,name_variable):
    """ Espera hasta que el procesador con la variable name_variable cumpla las condiciones de UpdateAttribute.
    @DAVILA 24-07-2025
    Esta función verifica el estado del procesador y espera hasta que se cumplan las condiciones de
    UpdateAttribute, es decir, que el valor de la variable name_variable cambie.
    :param id_processor: ID del procesador a verificar.
    :param name_variable: Nombre de la variable que se utilizará en el procesador.
    :return: None
    """

    estado_inicial = funciones_nifi.get_processor_state(url_nifi_api, id_processor, token, verify=False)
    valor_inicial = funciones_nifi.parse_state(estado_inicial,name_variable)
    
    while True:
        estado_actual = funciones_nifi.get_processor_state(url_nifi_api, id_processor, token, verify=False)
        valor_actual = funciones_nifi.parse_state(estado_actual,name_variable)
        
        if valor_inicial == valor_actual:
            logging.info("Waiting...")
            logging.info(f"Actual state:{valor_actual}")
            funciones_nifi.pause(15)
        else:
            logging.info(f"State updated: {valor_actual}")
            break

def wait_for_update_counters(id_counter1, id_counter2):
    """ Espera hasta que los contadores con los IDs id_counter1 e id_counter2 sean iguales.
    @DAVILA 24-07-2025
    Esta función verifica el valor de los contadores y espera hasta que sean iguales,
    lo que indica que ambos contadores han alcanzado el mismo número de registros procesados.
    :param id_counter1: ID del primer contador a verificar.
    :param id_counter2: ID del segundo contador a verificar.
    :return: None
    """
    # Obtener los contadores
    todos_contadores = funciones_nifi.get_counters(url_nifi_api, token, verify=False)
    valor_inicial1 = funciones_nifi.get_counter_value_by_id(todos_contadores, id_counter1)
    valor_inicial2 = funciones_nifi.get_counter_value_by_id(todos_contadores, id_counter2)
    logging.info(f"Initial values: Counter 1: {valor_inicial1}, Counter 2: {valor_inicial2}")

    while True:
        todos_contadores_actual = funciones_nifi.get_counters(url_nifi_api, token, verify=False)
        valor_actual1 = funciones_nifi.get_counter_value_by_id(todos_contadores_actual, id_counter1)
        valor_actual2 = funciones_nifi.get_counter_value_by_id(todos_contadores_actual, id_counter2)

        if valor_actual1 != valor_actual2:
            logging.info("Waiting for counters to match...")
            logging.info(f"Current values: Counter 1: {valor_actual1}, Counter 2: {valor_actual2}")
            funciones_nifi.pause(15)
        else:
            logging.info(f"Counters matched: Counter 1: {valor_actual1}, Counter 2: {valor_actual2}")
            break


with DAG(dag_id = DAG_ID,
         description=DAG_DESCRIPTION,
         schedule_interval=DAG_SCHEDULE,
         start_date=START_VAR,
         tags=TAGS,
         default_args=default_args,
         catchup = False, # false para que no ejecute tareas anteriores
         max_active_runs = 1,
        ) as dag:
        
        star_task = EmptyOperator(task_id="inicia_proceso")
        end_task = EmptyOperator(task_id="finaliza_proceso")

        # Setear los procesadores necesarios

        #processor_initial = '51bbb3d2-1650-3dc0-d6bd-676fe3feba7c'
        #processor_attibute_loop_invoke_employees = '1f331143-9a62-3440-60b4-7cf455f6b6f6'

        #count_split_employees = 'f175c1de-f869-3e16-a027-7dd52bb86166'
        #counter_split_jobs = '71b1beee-4741-3617-a03b-c80570ffc6f4'

        #count_upserts_employees = 'fe4c56d7-7bfb-3b51-a74b-524710cb899d'
        #count_upserts_jobs = '54b0691b-6363-36bb-8186-0e774c3bfd14'

        #count_upserts_role = '59d08934-f3e7-31fe-a4ed-5b60eb34e4eb'
        #count_upserts_boss = '44a7cc1f-d84d-35c4-a845-00d85ce7bd7a'
        #count_upserts_current_jobunt = '31f3aac0-c4b8-3efc-84da-10bcaa88459c'
        

        prepare_processor_loop_invoke = PythonOperator(task_id='preparar_procesador_loop_invoke',python_callable=prepare_processor_state, op_kwargs={
            'id_processor': '1f331143-9a62-3440-60b4-7cf455f6b6f6',
            'name_variable': 'no_has_next'
        })

        prepare_all_counters = PythonOperator(task_id='preparar_contadores',python_callable=prepare_counter, op_kwargs={
            'id_counters': ['f175c1de-f869-3e16-a027-7dd52bb86166', '71b1beee-4741-3617-a03b-c80570ffc6f4', 
                            'fe4c56d7-7bfb-3b51-a74b-524710cb899d', '54b0691b-6363-36bb-8186-0e774c3bfd14',
                            '59d08934-f3e7-31fe-a4ed-5b60eb34e4eb', '44a7cc1f-d84d-35c4-a845-00d85ce7bd7a',
                            '31f3aac0-c4b8-3efc-84da-10bcaa88459c']
        })

        running_processor_intial = PythonOperator(task_id='correr_procesador_inicial',python_callable=startup, op_kwargs={
            'id_processor': '51bbb3d2-1650-3dc0-d6bd-676fe3feba7c'
        })

        wait_final_process_loop_invoke = PythonOperator(task_id='esperar_final_loop_invoke',python_callable=wait_for_update_state_processor, op_kwargs={
            'id_processor': '1f331143-9a62-3440-60b4-7cf455f6b6f6',
            'name_variable': 'no_has_next'
        })

        wait_final_counter_employees = PythonOperator(task_id='esperar_final_contador_employees',python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': 'f175c1de-f869-3e16-a027-7dd52bb86166',
            'id_counter2': 'fe4c56d7-7bfb-3b51-a74b-524710cb899d'
        })

        wait_final_counter_jobs = PythonOperator(task_id='esperar_final_contador_jobs',python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': '71b1beee-4741-3617-a03b-c80570ffc6f4',
            'id_counter2': '54b0691b-6363-36bb-8186-0e774c3bfd14'
        })

        wait_final_counter_current_job = PythonOperator(task_id='esperar_final_contador_current_job',python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': 'f175c1de-f869-3e16-a027-7dd52bb86166',
            'id_counter2': '31f3aac0-c4b8-3efc-84da-10bcaa88459c'
        })

        wait_final_counter_role = PythonOperator(task_id='esperar_final_contador_role',python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': '71b1beee-4741-3617-a03b-c80570ffc6f4',
            'id_counter2': '59d08934-f3e7-31fe-a4ed-5b60eb34e4eb'
        })

        wait_final_counter_boss = PythonOperator(task_id='esperar_final_contador_boss',python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': '71b1beee-4741-3617-a03b-c80570ffc6f4',
            'id_counter2': '44a7cc1f-d84d-35c4-a845-00d85ce7bd7a'
        })


        star_task >> [prepare_processor_loop_invoke, prepare_all_counters] >> running_processor_intial
        running_processor_intial >> wait_final_process_loop_invoke >> [wait_final_counter_employees, wait_final_counter_jobs, wait_final_counter_current_job, wait_final_counter_role, wait_final_counter_boss] >> end_task


# [END instantiate_dag]