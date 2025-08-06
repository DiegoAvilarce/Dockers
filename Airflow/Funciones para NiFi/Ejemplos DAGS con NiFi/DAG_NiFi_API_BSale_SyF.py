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


TAGS = ["NiFI API BSale SyF"]
DAG_ID = 'DAG_NiFi_API_BSale_SyF'
DAG_DESCRIPTION = 'DAG que desencadena flujos de NiFi para guardar datos JSON obenidos por API de BSale SyF en una base de datos PostgreSQL.'

# que empiece a las 8,10,12,15 en horario UTC -3 (santiago de chile)
DAG_SCHEDULE =  '30 7,10,12,15 * * *' 
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

processor_initial_documents = '928c8105-e240-3836-2d18-dccbf3e5ecc2'
processor_initial_clients = 'aba3efbd-d14f-3c63-3ab7-a8ab26b20763'
processor_initial_variants = 'c5e35c5e-a9c5-37f5-ab09-2a6712ffb55a'
processor_initial_products = 'e69895ef-b42c-35a1-b7f5-ddcd15f34f22'
processor_initial_details = 'a55a6bb4-a05c-3987-1d33-2245cc82efec'
processor_initial_product_types = 'f149e771-8b4c-3f62-820b-d8fcd98fb4a7'
processor_initial_document_types = 'c6e6277d-3f1a-33af-194d-965385dcf53c'
processor_initial_checkout = 'f0af85bc-3e45-37e4-5ba9-8323c26c4c81'
processor_initial_payments = '6339e923-171c-374c-1d7b-8be57f7f42e0'
processor_initial_payment_types = 'ae5fd761-358f-3b8a-3985-92f057d53255'

processor_loop_invoke_documents = 'ec8f7b55-3fa5-3ed6-3505-adc6cf0541df'
processor_loop_invoke_clients = '85f46549-09f5-3d0d-2e79-86955949db39'
processor_loop_invoke_variants = 'a6ce42cd-5cca-3ff8-b671-fa4a5d9851e8'
processor_loop_invoke_products= 'b47ce041-5ca7-391d-d5a8-aad17660f36f'
processor_loop_invoke_product_types = 'a3fcad05-8e1d-3d08-be00-9b7b66f205d9'
processor_loop_invoke_document_types = 'b9731018-522e-38c7-291c-5a98242724a6'
processor_loop_invoke_checkout = 'ce830924-d09e-38b6-6bea-b694af3863b8'
processor_loop_invoke_payments = 'b1165c4d-d899-3d07-f3a6-f46d4424312a'
processor_loop_invoke_payment_types = '1098d883-b064-343b-6cc5-abfa358870f7'

count_split_documents = 'bc2c96a5-9ae0-320a-834e-2933cc80d3bb'
count_upserts_documents = '3128fd8a-53b8-34a1-9039-ba4d61b7bf36'

count_split_clients = 'edc39350-762d-34dc-8f92-2b4fb6981cca'
count_upserts_clients = 'adaedb56-4108-385f-9dc5-a4ad41ff9307'

count_split_variants = '8ea8ce6e-70cb-3b46-9ff5-9a7690779b8e'
count_upserts_variants = '5a5e5839-fda2-38ed-b138-4a925a6e082d'

count_split_products = '6e4c0f4c-5f4a-3a17-81aa-690013b59637'
count_upserts_products = '4a4589cb-c39c-3423-8962-963e77ea3c83'

count_split_details = 'ebfef6be-2474-3e46-a340-f4c4cf02e48f'
count_upserts_details = '0735eff2-6cf9-3e9b-8497-5a2c0235f15a'

count_split_product_types = '15113910-e58c-3556-8cdc-872f92de999d'
count_upserts_product_types = '8a3a4ce4-a873-3294-a01c-0731285458ce'

count_split_document_types = 'f5216e77-d1a0-3c1f-a6dd-a51c48fe8c3d'
count_upserts_document_types = '55b07a17-c23d-3de5-b722-031a765c537d'

count_split_checkout = '7a8b2e27-4a04-33d2-adba-2994fbf109dd'
count_upserts_checkout = 'ba79699b-4f78-388a-9f52-065f3699792d'

count_split_payments = 'ac1e1a4b-e368-37ee-a66d-6eda6cb06fc8'
count_upserts_payments = 'f7bd744f-df55-3568-a3a1-c7960e63f03f'

count_split_payment_types = 'bb0ee34c-6171-3cbc-b1fc-e684532feb26'
count_upserts_payment_types = 'b75cf2ef-60fd-3932-b0cd-d281514c524e'

# Definir funciones Python

def startup(*processor_configs, **kwargs):
    """ Inicia el flujo inicial de NiFi con múltiples procesadores usando RUN_ONCE.   
    @DAVILA 24-07-2025 - Mejorado con nombres descriptivos y RUN_ONCE
    Esta función ejecuta los procesadores una sola vez usando RUN_ONCE.
    Con RUN_ONCE, los procesadores se detendrán automáticamente después de ejecutarse,
    eliminando la necesidad de esperar y detenerlos manualmente.
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
    
    logging.info(f"Executing {len(normalized_configs)} processor(s) with RUN_ONCE strategy...")
    
    # Ejecutar todos los procesadores con RUN_ONCE (se detendrán automáticamente después de una ejecución)
    for config in normalized_configs:
        id_processor = config['id_processor']
        name = config['name']
        
        running_processor = funciones_nifi.update_processor_status(id_processor, "RUN_ONCE", token, url_nifi_api, verify=False)
        logging.info(f"{running_processor.status_code} - {running_processor.reason} - {name} ({id_processor}) executed with RUN_ONCE")
    
    logging.info("All processors executed with RUN_ONCE strategy. They will stop automatically after completion.")

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


        
        # Preparar procesadores con nombres descriptivos
        prepare_multiple_processors_named = PythonOperator(task_id='preparar_procesadores_multiples',python_callable=prepare_processor_state,op_kwargs={
            'processor_configs': [
                {'id_processor': processor_loop_invoke_documents, 'name_variable': 'no_has_next', 'name': 'Documents  Invoke'},
                {'id_processor': processor_loop_invoke_clients, 'name_variable': 'no_has_next', 'name': 'Clients Loop Invoke'},
                {'id_processor': processor_loop_invoke_variants, 'name_variable': 'no_has_next', 'name': 'Variants Loop Invoke'},
                {'id_processor': processor_loop_invoke_products, 'name_variable': 'no_has_next', 'name': 'Products Loop Invoke'},
                {'id_processor': processor_loop_invoke_product_types, 'name_variable': 'no_has_next', 'name': 'Product Types Loop Invoke'},
                {'id_processor': processor_loop_invoke_document_types, 'name_variable': 'no_has_next', 'name': 'Document Types Loop Invoke'},
                {'id_processor': processor_loop_invoke_checkout, 'name_variable': 'no_has_next', 'name': 'Checkout Loop Invoke'},
                {'id_processor': processor_loop_invoke_payments, 'name_variable': 'no_has_next', 'name': 'Payments Loop Invoke'},
                {'id_processor': processor_loop_invoke_payment_types, 'name_variable': 'no_has_next', 'name': 'Payment Types Loop Invoke'}
                ]
            },execution_timeout=timedelta(minutes=10))
        
        # Preparar contadores con nombres descriptivos
        prepare_all_counters_named = PythonOperator(task_id='preparar_contadores',python_callable=prepare_counter,op_kwargs={
            'counter_configs': [
                (count_split_documents, 'count_split_documents'),
                (count_upserts_documents, 'count_upserts_documents'),
                (count_split_clients, 'count_split_clients'),
                (count_upserts_clients, 'count_upserts_clients'),
                (count_split_variants, 'count_split_variants'),
                (count_upserts_variants, 'count_upserts_variants'),
                (count_split_products, 'count_split_products'),
                (count_upserts_products, 'count_upserts_products'),
                (count_split_details, 'count_split_details'),
                (count_upserts_details, 'count_upserts_details'),
                (count_split_product_types, 'count_split_product_types'),
                (count_upserts_product_types, 'count_upserts_product_types'),
                (count_split_document_types, 'count_split_document_types'),
                (count_upserts_document_types, 'count_upserts_document_types'),
                (count_split_checkout, 'count_split_checkout'),
                (count_upserts_checkout, 'count_upserts_checkout'),
                (count_split_payments, 'count_split_payments'),
                (count_upserts_payments, 'count_upserts_payments'),
                (count_split_payment_types, 'count_split_payment_types'),
                (count_upserts_payment_types, 'count_upserts_payment_types')
                ]
                },execution_timeout=timedelta(minutes=10))


        # Iniciar procesadores con nombres descriptivos
        running_processor_initial_named = PythonOperator(task_id='correr_procesadores_iniciales',python_callable=startup,op_kwargs={
            'processor_configs': [
                (processor_initial_documents, 'Initial Documents Processor'),
                (processor_initial_clients, 'Initial Clients Processor'),
                (processor_initial_variants, 'Initial Variants Processor'),
                (processor_initial_products, 'Initial Products Processor'),
                (processor_initial_product_types, 'Initial Product Types Processor'),
                (processor_initial_document_types, 'Initial Document Types Processor'),
                (processor_initial_checkout, 'Initial Checkout Processor'),
                (processor_initial_payments, 'Initial Payments Processor'),
                (processor_initial_payment_types, 'Initial Payment Types Processor')
                ]
            },execution_timeout=timedelta(minutes=10))
        
        
        # Esperar estado de procesadores con nombres descriptivos
        wait_final_process_loop_invoke_named = PythonOperator(task_id='esperar_final_loop_invoke',python_callable=wait_for_update_state_processor,op_kwargs={
            'processor_configs': [
                {'id_processor': processor_loop_invoke_documents, 'name_variable': 'no_has_next', 'name': 'Documents Loop Invoke'},
                {'id_processor': processor_loop_invoke_clients, 'name_variable': 'no_has_next', 'name': 'Clients Loop Invoke'},
                {'id_processor': processor_loop_invoke_variants, 'name_variable': 'no_has_next', 'name': 'Variants Loop Invoke'},
                {'id_processor': processor_loop_invoke_products, 'name_variable': 'no_has_next', 'name': 'Products Loop Invoke'},
                {'id_processor': processor_loop_invoke_product_types, 'name_variable': 'no_has_next', 'name': 'Product Types Loop Invoke'},
                {'id_processor': processor_loop_invoke_document_types, 'name_variable': 'no_has_next', 'name': 'Document Types Loop Invoke'},
                {'id_processor': processor_loop_invoke_checkout, 'name_variable': 'no_has_next', 'name': 'Checkout Loop Invoke'},
                {'id_processor': processor_loop_invoke_payments, 'name_variable': 'no_has_next', 'name': 'Payments Loop Invoke'},
                {'id_processor': processor_loop_invoke_payment_types, 'name_variable': 'no_has_next', 'name': 'Payment Types Loop Invoke'}
                ]
            },execution_timeout=timedelta(minutes=10))
        
        wait_all_counter_pairs_named = PythonOperator(task_id='esperar_final_todos_contadores',python_callable=wait_for_update_counters,op_kwargs={
            'counter_pairs': [
                {'id_counter1': count_split_clients,'id_counter2': count_upserts_clients,'pair_name': 'Clients'},
                {'id_counter1': count_split_variants,'id_counter2': count_upserts_variants,'pair_name': 'Variants'},
                {'id_counter1': count_split_products,'id_counter2': count_upserts_products,'pair_name': 'Products'},
                {'id_counter1': count_split_product_types,'id_counter2': count_upserts_product_types,'pair_name': 'Product Types'},
                {'id_counter1': count_split_document_types,'id_counter2': count_upserts_document_types,'pair_name': 'Document Types'},
                {'id_counter1': count_split_checkout,'id_counter2': count_upserts_checkout,'pair_name': 'Checkout'},
                {'id_counter1': count_split_payments,'id_counter2': count_upserts_payments,'pair_name': 'Payments'},
                {'id_counter1': count_split_payment_types,'id_counter2': count_upserts_payment_types,'pair_name': 'Payment Types'}
                ]
            },
            execution_timeout=timedelta(minutes=10))
        
        # proceso aparte para documents, ya que luego se ejecutará el flujo de detalles
        
        wait_all_counter_documents = PythonOperator(task_id='esperar_final_contador_documents',python_callable=wait_for_update_counters,op_kwargs={
            'counter_pairs': [
                {'id_counter1': count_split_documents, 'id_counter2': count_upserts_documents, 'pair_name': 'Documents'}
                ]
            },execution_timeout=timedelta(minutes=10))
        
        running_processor_initial_details = PythonOperator(task_id='correr_procesador_inicial_details',python_callable=startup,op_kwargs={
            'processor_configs': [
                (processor_initial_details, 'Initial Details Processor')
                ]
            },execution_timeout=timedelta(minutes=10))
        
        wait_count_details = PythonOperator(task_id='esperar_final_contador_details',python_callable=wait_for_update_counters,op_kwargs={
            'counter_pairs': [
                {'id_counter1': count_split_details, 'id_counter2': count_upserts_details, 'pair_name': 'Details'}
                ]
            },execution_timeout=timedelta(minutes=10))
        

        star_task >> prepare_multiple_processors_named >> prepare_all_counters_named >> running_processor_initial_named
        running_processor_initial_named >> wait_final_process_loop_invoke_named >> [wait_all_counter_pairs_named,wait_all_counter_documents]
        wait_all_counter_pairs_named >> end_task
        wait_all_counter_documents >> running_processor_initial_details >> wait_count_details >> end_task

# [END instantiate_dag]