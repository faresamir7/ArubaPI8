import requests
from requests.auth import HTTPBasicAuth
from typing import Optional
import urllib3
import json
import pandas as pd

class ArubaAPIClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def test_login(self):
        url = f"https://{self.base_url}:4343/v1/api/login"
        credentials = "username={}&password={}".format(self.username, self.password)
        response = requests.post(url, verify=False, data=credentials)
        if response.status_code == 200:
            token = response.json()['_global_result']['UIDARUBA']
            print("Login Successful, token is: {}".format(token))
            return token
        else:
            raise Exception(f"Login failed: {response.status_code}")

    def login(self, session):
        headers = {}
        payload = ""
        cookies = ""
        url = f"https://{self.base_url}:4343/v1/api/login"
        loginparams = {'username': self.username, 'password' : self.password}
        response = session.get(url, params=loginparams, headers=headers, data=payload, verify=False)
        if response.status_code == 200:
            return response.json()['_global_result']['UIDARUBA']
        else:
            raise Exception(f"Login failed: {response.status_code}")

    def show_command(self, show_command: str):
        session=requests.Session()
        sessionToken=self.login(session)
        headers = {}
        payload = ""
        cookies = ""
        showParams = {
            'command' : show_command,
            'UIDARUBA' : sessionToken
        }
        response = session.get("https://"+self.base_url+":4343/v1/configuration/showcommand", params=showParams, headers=headers, data=payload, verify=False)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            raise Exception(f"Request failed: {response.status_code}")

    def logout(self):
        url = f"https://{self.base_url}:4343/v1/api/logout"
        response = requests.post(url, verify=False)
        if response.status_code != 200:
            raise Exception(f"Logout failed: {response.status_code}")