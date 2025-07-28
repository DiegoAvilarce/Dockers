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


TAGS = ["NiFI API BUK Chile"]
DAG_ID = 'DAG_NiFi_API_BUK_Chile'
DAG_DESCRIPTION = 'DAG que desencadena flujos de NiFi para guardar datos JSON obenidos por API de BUK Chile en una base de datos PostgreSQL de BI y Oracle de TI Cramer.'

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

# Setear los procesadores necesarios

processor_initial_employees = '51bbb3d2-1650-3dc0-d6bd-676fe3feba7c'
processor_initial_areas = '10684319-4892-3a37-aabd-fe7b7905a4f3'
processor_initial_companies = '2e16fded-0198-1000-4e1f-bc41dcfa00f7'

processor_attibute_loop_invoke_employees = '1f331143-9a62-3440-60b4-7cf455f6b6f6'
processor_attibute_loop_invoke_areas = '06c99f61-03c9-3624-ea9a-566ef6a23b35'

count_split_employees = 'f175c1de-f869-3e16-a027-7dd52bb86166'
count_split_jobs = '71b1beee-4741-3617-a03b-c80570ffc6f4'
count_split_areas = '819bba42-79d8-31ea-b9bf-6568171477ab'

count_upserts_employees = 'fe4c56d7-7bfb-3b51-a74b-524710cb899d'
count_upserts_jobs = '54b0691b-6363-36bb-8186-0e774c3bfd14'
count_upsert_areas = 'd2d30110-e678-3a6f-92b6-7e0655729471'
count_upserts_role = '59d08934-f3e7-31fe-a4ed-5b60eb34e4eb'
count_upserts_boss = '44a7cc1f-d84d-35c4-a845-00d85ce7bd7a'
count_upserts_current_job = '31f3aac0-c4b8-3efc-84da-10bcaa88459c'


# Definir funciones Python

def startup(*id_processors, **kwargs):
    """ Inicia el flujo inicial de NiFi con múltiples procesadores.   
    @DAVILA 24-07-2025
    Esta función inicia los procesadores iniciales y luego los detiene,
    ya que no es necesario que sigan corriendo una vez que se ha iniciado el flujo.
    Se utiliza para preparar el flujo de trabajo de NiFi antes de ejecutar otras tareas.
    :param *id_processors: IDs de los procesadores a iniciar.
    :param **kwargs: Para compatibilidad con llamadas usando id_processors=
    :return: None
    """
    # Si se pasa como keyword argument
    if 'id_processors' in kwargs:
        if isinstance(kwargs['id_processors'], list):
            processors_to_start = kwargs['id_processors']
        else:
            processors_to_start = [kwargs['id_processors']]
    else:
        processors_to_start = id_processors
    
    logging.info(f"Starting {len(processors_to_start)} initial processor(s) to trigger NiFi flow...")
    
    # 1. Iniciar todos los procesadores
    for id_processor in processors_to_start:
        running_processor = funciones_nifi.update_processor_status(id_processor, "RUNNING", token, url_nifi_api, verify=False)
        logging.info(f"{running_processor.status_code} - {running_processor.reason} Processor {id_processor} started")
    
    # Esperar 15 segundos para que el flujo se inicie
    # Esto es necesario para que el flujo de NiFi tenga tiempo de procesar la solicitud y generar los FlowFiles necesarios.
    logging.info("Waiting 15 seconds for NiFi flow to initialize...")
    funciones_nifi.pause(15)

    # 2. Detener todos los procesadores, ya que no es necesario que sigan corriendo
    logging.info("Stopping processors...")
    for id_processor in processors_to_start:
        stopped_processor = funciones_nifi.update_processor_status(id_processor, "STOPPED", token, url_nifi_api)
        logging.info(f"{stopped_processor.status_code} - {stopped_processor.reason} Processor {id_processor} stopped")
        
def prepare_processor_state(*processor_configs, **kwargs):
    """ Prepara múltiples procesadores de NiFi para el flujo de trabajo.
    @DAVILA 24-07-2025
    Esta función detiene los procesadores con las variables especificadas,
    limpia su estado y luego los reinicia para que estén listos para el flujo de trabajo.
    :param *processor_configs: Tuplas de (id_processor, name_variable) o diccionarios con las configuraciones.
    :param **kwargs: Para compatibilidad con llamadas usando processor_configs=
    :return: None
    """
    # Si se pasa como keyword argument
    if 'processor_configs' in kwargs:
        if isinstance(kwargs['processor_configs'], list):
            configs_to_process = kwargs['processor_configs']
        else:
            configs_to_process = [kwargs['processor_configs']]
    else:
        configs_to_process = processor_configs
    
    # Normalizar las configuraciones a diccionarios
    normalized_configs = []
    for config in configs_to_process:
        if isinstance(config, tuple) and len(config) == 2:
            normalized_configs.append({
                'id_processor': config[0],
                'name_variable': config[1]
            })
        elif isinstance(config, dict):
            normalized_configs.append(config)
        else:
            raise ValueError(f"Invalid processor configuration: {config}. Expected tuple (id_processor, name_variable) or dict.")
    
    logging.info(f"Preparing {len(normalized_configs)} processor(s) for workflow...")
    
    # 1. Detener todos los procesadores
    logging.info("Step 1: Stopping all processors...")
    for config in normalized_configs:
        id_processor = config['id_processor']
        name_variable = config['name_variable']
        
        stopped_processor = funciones_nifi.update_processor_status(id_processor, "STOPPED", token, url_nifi_api)
        logging.info(f"{stopped_processor.status_code} - {stopped_processor.reason} Processor {id_processor} with variable {name_variable} stopped")
    
    # 2. Limpiar el estado de todos los procesadores
    logging.info("Step 2: Clearing state for all processors...")
    for config in normalized_configs:
        id_processor = config['id_processor']
        name_variable = config['name_variable']
        
        clear_processor = funciones_nifi.clear_processor_state(url_nifi_api, id_processor, token, verify=False)
        logging.info(f"{clear_processor.status_code} - {clear_processor.reason} Processor {id_processor} with variable {name_variable} state cleared")
    
    # 3. Iniciar todos los procesadores
    logging.info("Step 3: Starting all processors...")
    for config in normalized_configs:
        id_processor = config['id_processor']
        name_variable = config['name_variable']
        
        running_processor = funciones_nifi.update_processor_status(id_processor, "RUNNING", token, url_nifi_api, verify=False)
        logging.info(f"{running_processor.status_code} - {running_processor.reason} Processor {id_processor} with variable {name_variable} started")
    
    logging.info("All processors have been prepared successfully!")

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

def wait_for_update_state_processor(*processor_configs, **kwargs):
    """ Espera hasta que los procesadores con las variables especificadas alcancen el valor '1'.
    @DAVILA 24-07-2025
    Esta función verifica el estado de múltiples procesadores y espera hasta que se cumplan las condiciones de
    UpdateAttribute, es decir, que el valor de las variables especificadas sea igual a '1'.
    :param *processor_configs: Tuplas de (id_processor, name_variable) o diccionarios con las configuraciones.
    :param **kwargs: Para compatibilidad con llamadas usando processor_configs=
    :return: None
    """
    # Si se pasa como keyword argument
    if 'processor_configs' in kwargs:
        if isinstance(kwargs['processor_configs'], list):
            configs_to_process = kwargs['processor_configs']
        else:
            configs_to_process = [kwargs['processor_configs']]
    else:
        configs_to_process = processor_configs
    
    # Normalizar las configuraciones a diccionarios
    normalized_configs = []
    for config in configs_to_process:
        if isinstance(config, tuple) and len(config) == 2:
            normalized_configs.append({
                'id_processor': config[0],
                'name_variable': config[1]
            })
        elif isinstance(config, dict):
            normalized_configs.append(config)
        else:
            raise ValueError(f"Invalid processor configuration: {config}. Expected tuple (id_processor, name_variable) or dict.")
    
    logging.info(f"Monitoring {len(normalized_configs)} processor(s), waiting for state = '1'...")
    
    # Obtener estados iniciales
    initial_states = {}
    for config in normalized_configs:
        id_processor = config['id_processor']
        name_variable = config['name_variable']
        
        estado_inicial = funciones_nifi.get_processor_state(url_nifi_api, id_processor, token, verify=False)
        valor_inicial = funciones_nifi.parse_state(estado_inicial, name_variable)
        initial_states[id_processor] = {
            'name_variable': name_variable,
            'initial_value': valor_inicial
        }
        logging.info(f"Initial state for processor {id_processor} ({name_variable}): {valor_inicial}")
    
    # Monitorear cambios
    processors_pending = set(config['id_processor'] for config in normalized_configs)
    
    while processors_pending:
        for id_processor in list(processors_pending):
            name_variable = initial_states[id_processor]['name_variable']
            valor_inicial = initial_states[id_processor]['initial_value']
            
            estado_actual = funciones_nifi.get_processor_state(url_nifi_api, id_processor, token, verify=False)
            valor_actual = funciones_nifi.parse_state(estado_actual, name_variable)
            
            if valor_actual == '1':
                logging.info(f"State completed for processor {id_processor} ({name_variable}): {valor_actual}")
                processors_pending.remove(id_processor)
            else:
                logging.info(f"Waiting for processor {id_processor} ({name_variable}): {valor_actual} (waiting for '1')")
        
        if processors_pending:
            logging.info(f"Still waiting for {len(processors_pending)} processor(s)...")
            funciones_nifi.pause(15)
    
    logging.info("All processors have reached state '1' successfully!")

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

        
 


        prepare_multiple_processors_dict = PythonOperator(task_id='preparar_procesadores_multiples',python_callable=prepare_processor_state,op_kwargs={
            'processor_configs': [
                {'id_processor': processor_attibute_loop_invoke_employees, 'name_variable': 'no_has_next'},
                {'id_processor': processor_attibute_loop_invoke_areas, 'name_variable': 'no_has_next'},
                ]},
                execution_timeout=timedelta(minutes=5))
        
        prepare_all_counters = PythonOperator(task_id='preparar_contadores',python_callable=prepare_counter, op_kwargs={
            'id_counters': [count_split_employees, count_upserts_employees, 
                            count_split_jobs, count_upserts_jobs,
                            count_split_areas, count_upsert_areas,
                            count_upserts_role, count_upserts_boss,
                            count_upserts_current_job]
        },execution_timeout =timedelta(minutes=5))

        running_processor_intial = PythonOperator(task_id='correr_procesadores_iniciales', python_callable=startup, op_kwargs={
            'id_processors': [
                processor_initial_employees,
                processor_initial_areas,
                processor_initial_companies
            ]
        }, execution_timeout=timedelta(minutes=5))


        wait_final_process_loop_invoke = PythonOperator(task_id='esperar_final_loop_invoke', python_callable=wait_for_update_state_processor, op_kwargs={
            'processor_configs': [
                {'id_processor': processor_attibute_loop_invoke_employees, 'name_variable': 'no_has_next'},
                {'id_processor': processor_attibute_loop_invoke_areas, 'name_variable': 'no_has_next'}
            ]}, execution_timeout =timedelta(minutes=5))
        
        wait_final_counter_employees = PythonOperator(task_id='esperar_final_contador_employees',python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': count_split_employees,
            'id_counter2': count_upserts_employees
        }, execution_timeout =timedelta(minutes=5))

        wait_final_counter_jobs = PythonOperator(task_id='esperar_final_contador_jobs',python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': count_split_jobs,
            'id_counter2': count_upserts_jobs
        }, execution_timeout =timedelta(minutes=5))

        wait_final_counter_current_job = PythonOperator(task_id='esperar_final_contador_current_job',python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': count_split_employees,
            'id_counter2': count_upserts_current_job
        }, execution_timeout =timedelta(minutes=5))

        wait_final_counter_role = PythonOperator(task_id='esperar_final_contador_role',python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': count_split_jobs,
            'id_counter2': count_upserts_role
        }, execution_timeout =timedelta(minutes=5))

        wait_final_counter_boss = PythonOperator(task_id='esperar_final_contador_boss',python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': count_split_jobs,
            'id_counter2': count_upserts_boss
        }, execution_timeout =timedelta(minutes=5))


        star_task >> [prepare_multiple_processors_dict, prepare_all_counters] >> running_processor_intial
        running_processor_intial >> wait_final_process_loop_invoke >> [wait_final_counter_employees, wait_final_counter_jobs, wait_final_counter_current_job, wait_final_counter_role, wait_final_counter_boss] >> end_task


# [END instantiate_dag]