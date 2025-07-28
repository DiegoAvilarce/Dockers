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


TAGS = ["NiFI API BSale SyF"]
DAG_ID = 'DAG_NiFi_API_BSale_SyF'
DAG_DESCRIPTION = 'DAG que desencadena flujos de NiFi para guardar datos JSON obenidos por API de BSale SyF en una base de datos PostgreSQL.'

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

        # Setear los procesadores necesarios

        processor_initial_documents = '928c8105-e240-3836-2d18-dccbf3e5ecc2'
        processor_initial_clients = 'aba3efbd-d14f-3c63-3ab7-a8ab26b20763'
        processor_initial_variants = 'c5e35c5e-a9c5-37f5-ab09-2a6712ffb55a'
        processor_initial_products = 'e69895ef-b42c-35a1-b7f5-ddcd15f34f22'

        processor_loop_invoke_documents = 'ec8f7b55-3fa5-3ed6-3505-adc6cf0541df'
        processor_loop_invoke_clients = '85f46549-09f5-3d0d-2e79-86955949db39'
        processor_loop_invoke_variants = 'a6ce42cd-5cca-3ff8-b671-fa4a5d9851e8'
        processor_loop_invoke_products= 'b47ce041-5ca7-391d-d5a8-aad17660f36f'

        count_split_documents = 'bc2c96a5-9ae0-320a-834e-2933cc80d3bb'
        count_upserts_documents = '3128fd8a-53b8-34a1-9039-ba4d61b7bf36'

        count_split_clients = 'edc39350-762d-34dc-8f92-2b4fb6981cca'
        count_upserts_clients = 'adaedb56-4108-385f-9dc5-a4ad41ff9307'

        count_split_variants = '8ea8ce6e-70cb-3b46-9ff5-9a7690779b8e'
        count_upserts_variants = '5a5e5839-fda2-38ed-b138-4a925a6e082d'

        count_split_products = '6e4c0f4c-5f4a-3a17-81aa-690013b59637'
        count_upserts_products = '4a4589cb-c39c-3423-8962-963e77ea3c83'


        prepare_multiple_processors_dict = PythonOperator(task_id='preparar_procesadores_multiples',python_callable=prepare_processor_state,op_kwargs={
            'processor_configs': [
                {'id_processor': processor_loop_invoke_documents, 'name_variable': 'no_has_next'},
                {'id_processor': processor_loop_invoke_clients, 'name_variable': 'no_has_next'},
                {'id_processor': processor_loop_invoke_variants, 'name_variable': 'no_has_next'},
                {'id_processor': processor_loop_invoke_products, 'name_variable': 'no_has_next'}
                ]},
                execution_timeout=timedelta(minutes=10))
        
        prepare_all_counters = PythonOperator(task_id='preparar_contadores',python_callable=prepare_counter, op_kwargs={
            'id_counters': [count_split_documents,count_upserts_documents,
                            count_split_clients, count_upserts_clients,
                            count_split_variants, count_upserts_variants,
                            count_split_products, count_upserts_products
                                ]
        },execution_timeout =timedelta(minutes=10))

        running_processor_intial = PythonOperator(task_id='correr_procesadores_iniciales', python_callable=startup, op_kwargs={
            'id_processors': [processor_initial_documents,
                              processor_initial_clients,
                              processor_initial_variants,
                              processor_initial_products
                              ]
        }, execution_timeout=timedelta(minutes=10))
        
        wait_final_process_loop_invoke = PythonOperator(task_id='esperar_final_loop_invoke', python_callable=wait_for_update_state_processor, op_kwargs={
            'processor_configs': [
                {'id_processor': processor_loop_invoke_documents, 'name_variable': 'no_has_next'},
                {'id_processor': processor_loop_invoke_clients, 'name_variable': 'no_has_next'},
                {'id_processor': processor_loop_invoke_variants, 'name_variable': 'no_has_next'},
                {'id_processor': processor_loop_invoke_products, 'name_variable': 'no_has_next'}
            ]}, execution_timeout =timedelta(minutes=10))
        
        wait_final_counter_documents = PythonOperator(task_id='esperar_final_contador_documents', python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': count_split_documents,
            'id_counter2': count_upserts_documents
        }, execution_timeout =timedelta(minutes=10))

        wait_final_counter_clients = PythonOperator(task_id='esperar_final_contador_clients', python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': count_split_clients,
            'id_counter2': count_upserts_clients
        }, execution_timeout =timedelta(minutes=10))

        wait_final_counter_variants = PythonOperator(task_id='esperar_final_contador_variants', python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': count_split_variants,
            'id_counter2': count_upserts_variants
        }, execution_timeout =timedelta(minutes=10))

        wait_final_counter_products = PythonOperator(task_id='esperar_final_contador_products', python_callable=wait_for_update_counters, op_kwargs={
            'id_counter1': count_split_products,
            'id_counter2': count_upserts_products
        }, execution_timeout =timedelta(minutes=10))


        star_task >> prepare_multiple_processors_dict >> prepare_all_counters >> running_processor_intial
        running_processor_intial >> wait_final_process_loop_invoke >> [ wait_final_counter_documents,wait_final_counter_clients,wait_final_counter_variants, wait_final_counter_products] >> end_task

# [END instantiate_dag]