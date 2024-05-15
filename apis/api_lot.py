import os
from ftplib import FTP
import json
import requests

from config.config import settings


url_get_lot = f"{settings.PMSS_API_URL}/PMSS/rest/robotic/getLotStartData"
url_complete_lot = f"{settings.PMSS_API_URL}/PMSS/rest/robotic/completeLot"
url_update_cont = (
    f"{settings.PMSS_API_URL}/mnt/vol2/dockerdata/pmss/users/pmss/conet/robotic/recv"
)


def get_lot_start_data(lotNo):

    payload = json.dumps({"dsn": "orMesPMSS", "lotNo": lotNo})
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url_get_lot, headers=headers, data=payload)

    return response.json()


def complete_lot(data):

    payload = json.dumps({"dsn": "orMesPMSS", "data": data})
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url_complete_lot, headers=headers, data=payload)

    return response.json()


def update_cont(file_path):

    files = {"file": open(file_path, "rb")}
    resp = requests.post(url_update_cont, files=files)

    print(resp.content)

    return int(resp.content) == os.stat(file_path).st_size
