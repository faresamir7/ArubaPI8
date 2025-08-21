import requests
from requests.auth import HTTPBasicAuth
from typing import Optional
import urllib3
import json

class ArubaAPIClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def test_login(self): ##Basic function to login
        url = f"https://{self.base_url}:4343/v1/api/login" ##URL with IP or FQDN insert
        credentials = "username={}&password={}".format(self.username, self.password) ##Credentials to send
        response = requests.post(url, verify=False, data=credentials) ##Post request
        if response.status_code == 200: ##Self test
            print(json.dumps(response.json(), indent=2))
            token = response.json()['_global_result']['UIDARUBA']
            print("Login Successful, token is: {}".format(token))
            return token
        else:
            raise Exception(f"Login failed: {response.status_code}")

    def login(self, session): ##New function to login
        headers = {}
        payload = ""
        cookies = ""
        url = f"https://{self.base_url}:4343/v1/api/login" ##URL with IP or FQDN insert
        loginparams = {'username': self.username, 'password' : self.password} ##Credentials to send
        response = session.get(url, params=loginparams, headers=headers, data=payload, verify=False) ##Post request with empty Payload and Header
        if response.status_code == 200:
            return response.json()['_global_result']['UIDARUBA'] ##Returns UID
        else:
            raise Exception(f"Login failed: {response.status_code}")

    def show_command(self, show_command: str): ##Show command function
        session=requests.Session() ##Persistent session
        headers = {}
        payload = ""
        cookies = ""
        showParams = {
            'command' : show_command,
            'UIDARUBA' : self.login(session) ##Call to login function
        }
        response = session.get("https://"+self.base_url+":4343/v1/configuration/showcommand", params=showParams, headers=headers, data=payload, verify=False) ##Get request with empty Payload
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2)) ##Prints the response
        else:
            raise Exception(f"Request failed: {response.status_code}")

    def upgrade(self, filename: str, partition: str): ##Upgrade using TFTP
        session=requests.Session() ##Persistent session
        headers = {}
        payload = '{"partition_num": "'+partition+'", "tftphost": "'+self.base_url+'", "filename": "'+filename+'"}'
        cookies = ""
        showParams = {
            'UIDARUBA' : self.login(session) ##Call to login function
        } 
        response = session.post("https://"+self.base_url+":4343/v1/configuration/object/copy_tftp_system", params=showParams, headers=headers, data=payload, verify=False) ##Get request with empty Payload
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2)) ##Prints the response
        else:
            raise Exception(f"Request failed: {response.status_code}")

    def logout(self): ##Logout function
        url = f"https://{self.base_url}:4343/v1/api/logout"
        response = requests.post(url, verify=False)
        if response.status_code != 200:
            raise Exception(f"Logout failed: {response.status_code}")