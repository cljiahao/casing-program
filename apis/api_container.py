import json
import requests

from config.config import settings


url_reg_cont = f"{settings.CM_API_URL}/robotic/getRegisteredContainer/"
url_empty_cont = f"{settings.CM_API_URL}/robotic/getEmptyContainerStatus/"
url_update_cont = f"{settings.CM_API_URL}/robotic/updateContainerStatus/"
url_set_empty = f"{settings.CM_API_URL}/robotic/emptyContainerStatus/"


def get_registered(cont_id):

    headers = {
        "Content-Type": "application/json",
        "x-api-key": settings.ROB_API_KEY,
    }

    response = requests.request("GET", url_reg_cont + cont_id, headers=headers)

    return response.json()


def get_empty(cont_id):

    headers = {
        "Content-Type": "application/json",
        "x-api-key": settings.ROB_API_KEY,
    }

    response = requests.request("GET", url_empty_cont + cont_id, headers=headers)

    json = response.json()
    print(json)
    try:
        res = json[0]["kbv016"]
    except:
        res = False
    return res


def update_empty(cont_id):

    headers = {
        "Content-Type": "application/json",
        "x-api-key": settings.ROB_API_KEY,
    }

    data = json.dumps({"containerId": cont_id})

    response = requests.request("POST", url_update_cont, headers=headers, data=data)

    return response.json()


def set_empty_cont(cont_id):

    headers = {
        "Content-Type": "application/json",
        "x-api-key": settings.ROB_API_KEY,
    }

    data = json.dumps({"containerId": cont_id})

    response = requests.request("POST", url_set_empty, headers=headers, data=data)

    return response.json()
