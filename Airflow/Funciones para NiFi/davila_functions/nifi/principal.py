# %%
import json
import os
import requests
from time import time


# %%
def get_token(url_nifi_api: str, access_payload: dict, verify=False) -> str:
    """
    Obtiene un token JWT autenticando al usuario,
    usando la API REST `/access/token`.

    :param url_nifi_api: URL base de la API de NiFi.
    :param access_payload: diccionario con claves 'username' y 'password'
                           y sus respectivos valores.
    :param verify: si se debe verificar el certificado SSL.
    :return: Token JWT
    """

    header = {
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
    }
    response = requests.post(
        url_nifi_api + "access/token", headers=header, data=access_payload, verify=verify
    )
    return response.content.decode("ascii")

# %%
def get_processor(url_nifi_api: str, processor_id: str, token=None, verify=False):
    """
    Obtiene y devuelve un procesador específico.

    Utiliza la API REST `/processors/{processor_id}`.

    :param url_nifi_api: Cadena de texto
    :param processor_id: Cadena de texto
    :param token: Token de acceso JWT
    :param verify: si se debe verificar el certificado SSL.
    :returns: Objeto JSON del procesador
    """

    # Cabecera de autorización
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    # Solicita el procesador y lo convierte a JSON
    response = requests.get(url_nifi_api + f"processors/{processor_id}", headers=header, verify=verify)
    return json.loads(response.content)

# %%
def update_processor_status(processor_id: str, new_state: str, token, url_nifi_api, verify=False):
    """
    Inicia o detiene un procesador recuperando su información
    para obtener la revisión actual y luego enviando un JSON con el estado deseado.

    :param processor_id: ID del procesador al que se le aplicará el nuevo estado.
    :param new_state: Cadena de texto con el nuevo estado, valores aceptados:
                      STOPPED o RUNNING.
    :param token: Token JWT de acceso para NiFi.
    :param url_nifi_api: URL de la API de NiFi
    :param verify: si se debe verificar el certificado SSL.
    :return: None
    """

    # Obtener información del procesador desde `/processors/{processor_id}`
    processor = get_processor(url_nifi_api, processor_id, token)

    # Crear JSON con el nuevo estado y la revisión del procesador
    put_dict = {
        "revision": processor["revision"],
        "state": new_state,
        "disconnectedNodeAcknowledged": True,
    }

    # Enviar el JSON usando PUT
    payload = json.dumps(put_dict).encode("utf8")
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }
    response = requests.put(
        url_nifi_api + f"processors/{processor_id}/run-status",
        headers=header,
        data=payload,
        verify=verify
    )
    return response

# %%
def get_processor_state(url_nifi_api: str, processor_id: str, token=None, verify=False):
    """
    Obtiene y devuelve el estado de un procesador específico.

    Utiliza la API REST 'processors/{processor_id}/state'.

    :param url_nifi_api: Cadena de texto
    :param processor_id: Cadena de texto
    :param token: Token de acceso JWT
    :param verify: si se debe verificar el certificado SSL.
    :returns: Objeto JSON con el estado del procesador
    """

    # Cabecera de autorización
    if token is None:
        header = {"Content-Type": "application/json"}
    else:
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token),
        }

    # Solicita el estado del procesador y lo convierte a JSON
    response = requests.get(
        url_nifi_api + f"processors/{processor_id}/state", headers=header, verify=verify
    )
    return json.loads(response.content)

# %%
def clear_processor_state(url_nifi_api: str, processor_id: str, token, verify=False):
    """
    Limpia el estado de un procesador usando la API REST.

    Utiliza la API REST 'processors/{processor_id}/state/clear-requests'.

    :param url_nifi_api: Cadena de texto - URL base de la API de NiFi
    :param processor_id: Cadena de texto - ID del procesador
    :param token: Token de acceso JWT
    :param verify: si se debe verificar el certificado SSL.
    :returns: Objeto de respuesta
    """
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }

    # Enviar POST para limpiar estado
    response = requests.post(
        url_nifi_api + f"processors/{processor_id}/state/clear-requests", 
        headers=header, 
        verify=verify
    )
    return response

# %%

def get_counters(url_nifi_api: str, token=None, verify=False):
    """
    Obtiene todos los contadores de NiFi usando la API REST.

    Utiliza la API REST `/counters`.

    :param url_nifi_api: URL base de la API de NiFi (ej: "http://localhost:8080/nifi-api/")
    :param token: Token de acceso JWT (opcional si no hay autenticación)
    :param verify: si se debe verificar el certificado SSL
    :returns: Objeto JSON con todos los contadores
    """
    
    header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token),
        }

    # Solicita los contadores y los convierte a JSON
    response = requests.get(
        url_nifi_api + "counters", 
        headers=header, 
        verify=verify
    )
    
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        raise Exception(f"Error al obtener contadores: {response.status_code} - {response.text}")


def get_counter_value_by_id(counters_response: dict, counter_id: str):
    """
    Obtiene el valor de un contador específico por su ID desde la respuesta JSON.

    :param counters_response: Respuesta JSON completa de la API de contadores
    :param counter_id: ID del contador a buscar
    :returns: Valor del contador o None si no se encuentra
    """
    
    # Verificar si tiene aggregateSnapshot (estructura más común)
    if "aggregateSnapshot" in counters_response["counters"]:
        for counter in counters_response["counters"]["aggregateSnapshot"]["counters"]:
            if counter["id"] == counter_id:
                return counter["value"]
    
    # Verificar si tiene nodeSnapshots (estructura alternativa)
    elif "nodeSnapshots" in counters_response["counters"]:
        for node_snapshot in counters_response["counters"]["nodeSnapshots"]:
            for counter in node_snapshot["snapshot"]["counters"]:
                if counter["id"] == counter_id:
                    return counter["value"]
    
    return None


def reset_counter(url_nifi_api: str, counter_id: str, token, verify=False):
    """
    Resetea un contador específico a 0.

    :param url_nifi_api: URL base de la API de NiFi
    :param counter_id: ID del contador a resetear
    :param token: Token de acceso JWT
    :param verify: si se debe verificar el certificado SSL
    :returns: Respuesta de la API
    """
    
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token),
    }
    
    reset_payload = {
        "counter": {
            "value": 0
        }
    }
    
    response = requests.put(
        url_nifi_api + f"counters/{counter_id}",
        headers=header,
        data=json.dumps(reset_payload),
        verify=verify
    )
    
    return response


# %%
def parse_state(json_obj, state_key: str):
    """
    Obtiene el valor de un estado usando su clave desde el JSON.

    :param json_obj: el estado general del procesador.
    :param state_key: clave del estado específico.
    :raises ValueError: si no se encuentra la clave en el estado del procesador.
    :return: valor correspondiente a la clave.
    """
    states = json_obj["componentState"]["localState"]["state"]
    for state in states:
        if state["key"] == state_key:
            value = state["value"]
            return value
    raise ValueError(f"No se pudo encontrar {state_key} ")

# %%
def pause(secs):
    # Pausa la ejecución por cierta cantidad de segundos
    init_time = time()
    while time() < init_time + secs:
        pass
# %%
