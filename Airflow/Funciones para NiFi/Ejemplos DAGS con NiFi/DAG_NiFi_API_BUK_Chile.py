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

# quitar los warnigngs de las peticiones
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import davila_functions.nifi.principal as funciones_nifi




TAGS = ["NiFI API BUK Chile"]
DAG_ID = 'DAG_NiFi_API_BUK_Chile'
DAG_DESCRIPTION = 'DAG que desencadena flujos de NiFi para guardar datos JSON obenidos por API de BUK Chile en una base de datos PostgreSQL de BI y Oracle de TI Cramer.'

# que empiece a las 7,12,16 en horario UTC -3 (santiago de chile)
DAG_SCHEDULE =  '0 7,12,16 * * *'  # Cada día a las 7:00, 12:00 y 16:00 horas
START_VAR = pendulum.datetime(2025, 7, 30, tz="America/Santiago")

# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Diego Avila',
    'depends_on_past': False,
    'email': ['davila@cramer.cl'],
    'email_on_failure': False,
    'email_on_retry': False, 
    'retries': 0, # 0 para que no reintente
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
processor_initial_areas = 'c92accf0-e749-3ed5-4cbb-14cbb2adce04'
processor_initial_companies = '2e16fded-0198-1000-4e1f-bc41dcfa00f7'
processor_initial_overtime = '715f0f22-2038-38b1-19a6-66c163c0048e'
processor_initial_overtime_types = '8e165f9c-8cfe-3a21-a696-ab4324fe8a6e'
processor_initial_process_periods = '41987458-0368-330d-04b8-cf241c14a89a'
processor_initial_roles = '1c14b065-ceb4-31f8-dad6-78997937aa0d'


processor_loop_invoke_employees = '1f331143-9a62-3440-60b4-7cf455f6b6f6'
processor_loop_invoke_areas = 'caceeafe-4d04-3eac-877c-88618c78b650'
processor_loop_invoke_overtime = '6beb2634-f09b-33b3-8ae8-b6d00eb83ea9'
processor_loop_invoke_process_periods = '2a1a48c1-ce14-33ed-7251-4713b80c7c62'
processor_loop_invoke_roles = '3925a293-24b5-3451-ba60-bebdeea1ff93'

count_split_employees = 'f175c1de-f869-3e16-a027-7dd52bb86166'
count_split_jobs = '71b1beee-4741-3617-a03b-c80570ffc6f4'
count_split_areas = '819bba42-79d8-31ea-b9bf-6568171477ab'
count_split_overtime = 'b874ee94-ace7-328f-aa6a-d2a5303a256c'
count_split_process_periods = '90d80881-0acd-3782-a80a-364f60e49d48'
count_split_roles = '62586b42-2548-3854-9558-a4109ab52ff6'

count_upserts_employees = 'fe4c56d7-7bfb-3b51-a74b-524710cb899d'
count_upserts_jobs = '54b0691b-6363-36bb-8186-0e774c3bfd14'
count_upsert_areas = 'd2d30110-e678-3a6f-92b6-7e0655729471'
count_upserts_boss = '44a7cc1f-d84d-35c4-a845-00d85ce7bd7a'
count_upserts_current_job = '31f3aac0-c4b8-3efc-84da-10bcaa88459c'
count_upserts_overtime = 'd3e0481d-294d-31c9-9dde-efc5f5896db5'
count_upserts_process_periods = '40058cee-9684-3e64-bbbb-412033377c2b'
count_upserts_roles = '101bd8c7-9796-36b7-9ae3-52dde67d7f42'


# Definir funciones Python

def startup(*processor_configs, **kwargs):
    """ Inicia el flujo inicial de NiFi con múltiples procesadores.   
    @DAVILA 24-07-2025 - Mejorado con nombres descriptivos
    Esta función inicia los procesadores iniciales y luego los detiene,
    ya que no es necesario que sigan corriendo una vez que se ha iniciado el flujo.
    Se utiliza para preparar el flujo de trabajo de NiFi antes de ejecutar otras tareas.
    :param *processor_configs: Tuplas de (id_processor, name) o diccionarios con las configuraciones.
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
    for i, config in enumerate(configs_to_process):
        if isinstance(config, tuple) and len(config) == 2:
            normalized_configs.append({
                'id_processor': config[0],
                'name': config[1]
            })
        elif isinstance(config, dict):
            name = config.get('name', f'Processor_{i+1}')
            normalized_configs.append({
                'id_processor': config['id_processor'],
                'name': name
            })
        elif isinstance(config, str):  # Solo ID, generar nombre automático
            normalized_configs.append({
                'id_processor': config,
                'name': f'Processor_{i+1}'
            })
        else:
            raise ValueError(f"Invalid processor configuration: {config}. Expected tuple (id_processor, name), dict, or string.")
    
    logging.info(f"Starting {len(normalized_configs)} initial processor(s) to trigger NiFi flow...")
    
    # 1. Iniciar todos los procesadores
    for config in normalized_configs:
        id_processor = config['id_processor']
        name = config['name']
        
        running_processor = funciones_nifi.update_processor_status(id_processor, "RUNNING", token, url_nifi_api, verify=False)
        logging.info(f"{running_processor.status_code} - {running_processor.reason} - {name} ({id_processor}) started")
    
    # Esperar 15 segundos para que el flujo se inicie
    logging.info("Waiting 15 seconds for NiFi flow to initialize...")
    funciones_nifi.pause(15)

    # 2. Detener todos los procesadores
    logging.info("Stopping processors...")
    for config in normalized_configs:
        id_processor = config['id_processor']
        name = config['name']
        
        stopped_processor = funciones_nifi.update_processor_status(id_processor, "STOPPED", token, url_nifi_api)
        logging.info(f"{stopped_processor.status_code} - {stopped_processor.reason} - {name} ({id_processor}) stopped")

def prepare_processor_state(*processor_configs, **kwargs):
    """ Prepara múltiples procesadores de NiFi para el flujo de trabajo.
    @DAVILA 24-07-2025 - Mejorado con nombres descriptivos
    Esta función detiene los procesadores con las variables especificadas,
    limpia su estado y luego los reinicia para que estén listos para el flujo de trabajo.
    :param *processor_configs: Tuplas de (id_processor, name_variable, name) o diccionarios con las configuraciones.
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
    for i, config in enumerate(configs_to_process):
        if isinstance(config, tuple) and len(config) == 3:
            normalized_configs.append({
                'id_processor': config[0],
                'name_variable': config[1],
                'name': config[2]
            })
        elif isinstance(config, tuple) and len(config) == 2:
            normalized_configs.append({
                'id_processor': config[0],
                'name_variable': config[1],
                'name': f'Processor_{i+1}'
            })
        elif isinstance(config, dict):
            name = config.get('name', f'Processor_{i+1}')
            normalized_configs.append({
                'id_processor': config['id_processor'],
                'name_variable': config['name_variable'],
                'name': name
            })
        else:
            raise ValueError(f"Invalid processor configuration: {config}. Expected tuple (id_processor, name_variable) or (id_processor, name_variable, name) or dict.")
    
    logging.info(f"Preparing {len(normalized_configs)} processor(s) for workflow...")
    
    # 1. Detener todos los procesadores
    logging.info("Step 1: Stopping all processors...")
    for config in normalized_configs:
        id_processor = config['id_processor']
        name_variable = config['name_variable']
        name = config['name']
        
        stopped_processor = funciones_nifi.update_processor_status(id_processor, "STOPPED", token, url_nifi_api)
        logging.info(f"{stopped_processor.status_code} - {stopped_processor.reason} - {name} ({name_variable}) stopped")
    
    # 2. Limpiar el estado de todos los procesadores
    logging.info("Step 2: Clearing state for all processors...")
    for config in normalized_configs:
        id_processor = config['id_processor']
        name_variable = config['name_variable']
        name = config['name']
        
        clear_processor = funciones_nifi.clear_processor_state(url_nifi_api, id_processor, token, verify=False)
        logging.info(f"{clear_processor.status_code} - {clear_processor.reason} - {name} ({name_variable}) state cleared")
    
    # 3. Iniciar todos los procesadores
    logging.info("Step 3: Starting all processors...")
    for config in normalized_configs:
        id_processor = config['id_processor']
        name_variable = config['name_variable']
        name = config['name']
        
        running_processor = funciones_nifi.update_processor_status(id_processor, "RUNNING", token, url_nifi_api, verify=False)
        logging.info(f"{running_processor.status_code} - {running_processor.reason} - {name} ({name_variable}) started")
    
    logging.info("All processors have been prepared successfully!")

def prepare_counter(*counter_configs, **kwargs):
    """ Prepara los contadores de NiFi para el flujo de trabajo.
    @DAVILA 24-07-2025 - Mejorado con nombres descriptivos
    Esta función reinicia los contadores especificados para que estén listos para el flujo de trabajo.
    :param *counter_configs: Tuplas de (id_counter, name) o diccionarios con las configuraciones.
    :param **kwargs: Para compatibilidad con llamadas usando counter_configs=
    :return: None
    """
    # Si se pasa como keyword argument
    if 'counter_configs' in kwargs:
        if isinstance(kwargs['counter_configs'], list):
            configs_to_process = kwargs['counter_configs']
        else:
            configs_to_process = [kwargs['counter_configs']]
    else:
        configs_to_process = counter_configs
    
    # Normalizar las configuraciones a diccionarios
    normalized_configs = []
    for i, config in enumerate(configs_to_process):
        if isinstance(config, tuple) and len(config) == 2:
            normalized_configs.append({
                'id_counter': config[0],
                'name': config[1]
            })
        elif isinstance(config, dict):
            name = config.get('name', f'Counter_{i+1}')
            normalized_configs.append({
                'id_counter': config['id_counter'],
                'name': name
            })
        elif isinstance(config, str):  # Solo ID, generar nombre automático
            normalized_configs.append({
                'id_counter': config,
                'name': f'Counter_{i+1}'
            })
        else:
            raise ValueError(f"Invalid counter configuration: {config}. Expected tuple (id_counter, name), dict, or string.")
    
    logging.info(f"Preparing {len(normalized_configs)} counter(s) for workflow...")
    
    for config in normalized_configs:
        id_counter = config['id_counter']
        name = config['name']
        
        # Reiniciar el contador
        reset_counter = funciones_nifi.reset_counter(url_nifi_api, id_counter, token, verify=False)
        logging.info(f"{reset_counter.status_code} - {reset_counter.reason} - {name} counter ({id_counter}) reset")
    
    logging.info("All counters have been prepared successfully!")

def wait_for_update_state_processor(*processor_configs, **kwargs):
    """ Espera hasta que los procesadores con las variables especificadas alcancen el valor '1'.
    @DAVILA 24-07-2025 - Mejorado con nombres descriptivos
    Esta función verifica el estado de múltiples procesadores y espera hasta que se cumplan las condiciones de
    UpdateAttribute, es decir, que el valor de las variables especificadas sea igual a '1'.
    :param *processor_configs: Tuplas de (id_processor, name_variable, name) o diccionarios con las configuraciones.
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
    for i, config in enumerate(configs_to_process):
        if isinstance(config, tuple) and len(config) == 3:
            normalized_configs.append({
                'id_processor': config[0],
                'name_variable': config[1],
                'name': config[2]
            })
        elif isinstance(config, tuple) and len(config) == 2:
            normalized_configs.append({
                'id_processor': config[0],
                'name_variable': config[1],
                'name': f'Processor_{i+1}'
            })
        elif isinstance(config, dict):
            name = config.get('name', f'Processor_{i+1}')
            normalized_configs.append({
                'id_processor': config['id_processor'],
                'name_variable': config['name_variable'],
                'name': name
            })
        else:
            raise ValueError(f"Invalid processor configuration: {config}. Expected tuple (id_processor, name_variable) or (id_processor, name_variable, name) or dict.")
    
    logging.info(f"Monitoring {len(normalized_configs)} processor(s), waiting for state = '1'...")
    
    # Obtener estados iniciales
    initial_states = {}
    for config in normalized_configs:
        id_processor = config['id_processor']
        name_variable = config['name_variable']
        name = config['name']
        
        estado_inicial = funciones_nifi.get_processor_state(url_nifi_api, id_processor, token, verify=False)
        valor_inicial = funciones_nifi.parse_state(estado_inicial, name_variable)
        initial_states[id_processor] = {
            'name_variable': name_variable,
            'name': name,
            'initial_value': valor_inicial
        }
        logging.info(f"Initial state for {name} ({name_variable}): {valor_inicial}")
    
    # Monitorear cambios
    processors_pending = set(config['id_processor'] for config in normalized_configs)
    
    while processors_pending:
        for id_processor in list(processors_pending):
            name_variable = initial_states[id_processor]['name_variable']
            name = initial_states[id_processor]['name']
            
            estado_actual = funciones_nifi.get_processor_state(url_nifi_api, id_processor, token, verify=False)
            valor_actual = funciones_nifi.parse_state(estado_actual, name_variable)
            
            if valor_actual == '1':
                logging.info(f"State completed for {name} ({name_variable}): {valor_actual}")
                processors_pending.remove(id_processor)
            else:
                logging.info(f"Waiting for {name} ({name_variable}): {valor_actual} (waiting for '1')")
        
        if processors_pending:
            logging.info(f"Still waiting for {len(processors_pending)} processor(s)...")
            funciones_nifi.pause(15)
    
    logging.info("All processors have reached state '1' successfully!")

def wait_for_update_counters(*counter_pairs, **kwargs):
    """ Espera hasta que cada par de contadores tenga valores iguales.
    @DAVILA 24-07-2025
    Esta función verifica múltiples pares de contadores y espera hasta que cada par tenga valores iguales,
    lo que indica que ambos contadores en cada par han alcanzado el mismo número de registros procesados.
    :param *counter_pairs: Tuplas de (id_counter1, id_counter2) o diccionarios con las configuraciones.
    :param **kwargs: Para compatibilidad con llamadas usando counter_pairs=
    :return: None
    """
    # Si se pasa como keyword argument
    if 'counter_pairs' in kwargs:
        if isinstance(kwargs['counter_pairs'], list):
            configs_to_process = kwargs['counter_pairs']
        else:
            configs_to_process = [kwargs['counter_pairs']]
    else:
        configs_to_process = counter_pairs
    
    # Normalizar las configuraciones a diccionarios
    normalized_pairs = []
    for i, config in enumerate(configs_to_process):
        if isinstance(config, tuple) and len(config) == 2:
            normalized_pairs.append({
                'id_counter1': config[0],
                'id_counter2': config[1],
                'pair_name': f'Pair_{i+1}'
            })
        elif isinstance(config, dict):
            pair_name = config.get('pair_name', f'Pair_{i+1}')
            normalized_pairs.append({
                'id_counter1': config['id_counter1'],
                'id_counter2': config['id_counter2'],
                'pair_name': pair_name
            })
        else:
            raise ValueError(f"Invalid counter pair configuration: {config}. Expected tuple (id_counter1, id_counter2) or dict.")
    
    if len(normalized_pairs) == 0:
        raise ValueError("Se requiere al menos un par de contadores para comparar")
    
    logging.info(f"Monitoring {len(normalized_pairs)} counter pair(s), waiting for each pair to match...")
    
    # Obtener estados iniciales
    todos_contadores = funciones_nifi.get_counters(url_nifi_api, token, verify=False)
    initial_states = {}
    
    for pair in normalized_pairs:
        id_counter1 = pair['id_counter1']
        id_counter2 = pair['id_counter2']
        pair_name = pair['pair_name']
        
        valor_inicial1 = funciones_nifi.get_counter_value_by_id(todos_contadores, id_counter1)
        valor_inicial2 = funciones_nifi.get_counter_value_by_id(todos_contadores, id_counter2)
        
        initial_states[pair_name] = {
            'id_counter1': id_counter1,
            'id_counter2': id_counter2,
            'initial_value1': valor_inicial1,
            'initial_value2': valor_inicial2
        }
        logging.info(f"Initial values for {pair_name}: Counter1={valor_inicial1}, Counter2={valor_inicial2}")
    
    # Monitorear cambios
    pairs_pending = set(pair['pair_name'] for pair in normalized_pairs)
    
    while pairs_pending:
        todos_contadores_actual = funciones_nifi.get_counters(url_nifi_api, token, verify=False)
        
        for pair_name in list(pairs_pending):
            pair_info = initial_states[pair_name]
            id_counter1 = pair_info['id_counter1']
            id_counter2 = pair_info['id_counter2']
            
            valor_actual1 = funciones_nifi.get_counter_value_by_id(todos_contadores_actual, id_counter1)
            valor_actual2 = funciones_nifi.get_counter_value_by_id(todos_contadores_actual, id_counter2)
            
            if valor_actual1 == valor_actual2:
                logging.info(f"Pair matched for {pair_name}: Counter1={valor_actual1}, Counter2={valor_actual2}")
                pairs_pending.remove(pair_name)
            else:
                logging.info(f"Waiting for {pair_name}: Counter1={valor_actual1}, Counter2={valor_actual2}")
        
        if pairs_pending:
            logging.info(f"Still waiting for {len(pairs_pending)} pair(s)...")
            funciones_nifi.pause(15)
    
    logging.info("All counter pairs have matched successfully!")


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

        


        prepare_multiple_processors_named = PythonOperator(task_id='preparar_procesadores_multiples',python_callable=prepare_processor_state,op_kwargs={
            'processor_configs': [
                {'id_processor': processor_loop_invoke_employees, 'name_variable': 'no_has_next', 'name': 'Loop Invoke Employees'},
                {'id_processor': processor_loop_invoke_areas, 'name_variable': 'no_has_next', 'name': 'Loop Invoke Areas'},
                {'id_processor': processor_loop_invoke_overtime, 'name_variable': 'no_has_next', 'name': 'Loop Invoke Overtime'},
                {'id_processor': processor_loop_invoke_process_periods, 'name_variable': 'no_has_next', 'name': 'Loop Invoke Process Periods'},
                {'id_processor': processor_loop_invoke_roles, 'name_variable': 'no_has_next', 'name': 'Loop Invoke Roles'}
                ]},
                execution_timeout=timedelta(minutes=5))
        
        prepare_all_counters_named = PythonOperator(task_id='preparar_contadores',python_callable=prepare_counter, op_kwargs={
            'counter_configs': [
                {'id_counter': count_split_employees, 'name': 'count_split_employees'},
                {'id_counter': count_upserts_employees, 'name': 'count_upserts_employees'},
                {'id_counter': count_split_jobs, 'name': 'count_split_jobs'},
                {'id_counter': count_upserts_jobs, 'name': 'count_upserts_jobs'},
                {'id_counter': count_split_areas, 'name': 'count_split_areas'},
                {'id_counter': count_upsert_areas, 'name': 'count_upsert_areas'},
                {'id_counter': count_upserts_boss, 'name': 'count_upserts_boss'},
                {'id_counter': count_upserts_current_job, 'name': 'count_upserts_current_job'},
                {'id_counter': count_split_overtime, 'name': 'count_split_overtime'},
                {'id_counter': count_upserts_overtime, 'name': 'count_upserts_overtime'},
                {'id_counter': count_split_process_periods, 'name': 'count_split_process_periods'},
                {'id_counter': count_upserts_process_periods, 'name': 'count_upserts_process_periods'},
                {'id_counter': count_split_roles, 'name': 'count_split_roles'},
                {'id_counter': count_upserts_roles, 'name': 'count_upserts_roles'}
            ]}, execution_timeout=timedelta(minutes=5))

        running_processor_initial_named = PythonOperator(task_id='correr_procesadores_iniciales', python_callable=startup, op_kwargs={
            'processor_configs': [
                {'id_processor': processor_initial_employees, 'name': 'Processor Initial Employees'},
                {'id_processor': processor_initial_areas, 'name': 'Processor Initial Areas'},
                {'id_processor': processor_initial_companies, 'name': 'Processor Initial Companies'},
                {'id_processor': processor_initial_overtime, 'name': 'Processor Initial Overtime'},
                {'id_processor': processor_initial_overtime_types, 'name': 'Processor Initial Overtime Types'},
                {'id_processor': processor_initial_process_periods, 'name': 'Processor Initial Process Periods'},
                {'id_processor': processor_initial_roles, 'name': 'Processor Initial Roles'}
            ]
        }, execution_timeout=timedelta(minutes=5))


        wait_final_process_loop_invoke_named = PythonOperator(task_id='esperar_final_loop_invoke', python_callable=wait_for_update_state_processor, op_kwargs={
            'processor_configs': [
                {'id_processor': processor_loop_invoke_employees, 'name_variable': 'no_has_next', 'name': 'Employees Loop Invoke'},    
                {'id_processor': processor_loop_invoke_areas, 'name_variable': 'no_has_next', 'name': 'Areas Loop Invoke'},
                {'id_processor': processor_loop_invoke_overtime, 'name_variable': 'no_has_next', 'name': 'Overtime Loop Invoke'},
                {'id_processor': processor_loop_invoke_process_periods, 'name_variable': 'no_has_next', 'name': 'Process Periods Loop Invoke'},
                {'id_processor': processor_loop_invoke_roles, 'name_variable': 'no_has_next', 'name': 'Roles Loop Invoke'}
            ]
        }, execution_timeout=timedelta(minutes=5))
    

        wait_all_counter_pairs_named = PythonOperator(task_id='esperar_todos_pares_contadores', python_callable=wait_for_update_counters, op_kwargs={
            'counter_pairs': [
                {'id_counter1': count_split_employees, 'id_counter2': count_upserts_employees, 'pair_name': 'Employees'},
                {'id_counter1': count_split_jobs, 'id_counter2': count_upserts_jobs, 'pair_name': 'Jobs'},
                {'id_counter1': count_split_employees, 'id_counter2': count_upserts_current_job, 'pair_name': 'Current Job'},
                {'id_counter1': count_split_jobs, 'id_counter2': count_upserts_boss, 'pair_name': 'Boss'},
                {'id_counter1': count_split_areas, 'id_counter2': count_upsert_areas, 'pair_name': 'Areas'},
                {'id_counter1': count_split_overtime, 'id_counter2': count_upserts_overtime, 'pair_name': 'Overtime'},
                {'id_counter1': count_split_process_periods, 'id_counter2': count_upserts_process_periods, 'pair_name': 'Process Periods'},
                {'id_counter1': count_split_roles, 'id_counter2': count_upserts_roles, 'pair_name': 'Roles'}
            ]
        }, execution_timeout=timedelta(minutes=5))


        star_task >> [prepare_multiple_processors_named, prepare_all_counters_named] >> running_processor_initial_named
        running_processor_initial_named >> wait_final_process_loop_invoke_named >> wait_all_counter_pairs_named >> end_task


# [END instantiate_dag]