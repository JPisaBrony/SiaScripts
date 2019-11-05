import requests
import os.path

BASE_URL = "https://api.scaleway.com/instance/v1/zones/fr-par-1"
SETUP_REPO = "https://github.com/JPisaBrony/SiaScripts"
SETTINGS_FILE = "settings.txt"
auth_token = None
organization = None

if os.path.isfile(SETTINGS_FILE):
    with open(SETTINGS_FILE) as f:
        lines = f.readlines()
        auth_token = lines[0].strip()
        organization = lines[1].strip()
else:
    print SETTINGS_FILE + " doesn't exist"
    exit(0)

JSON_HEADERS = {"X-Auth-Token": auth_token, "Content-Type": "application/json"}
TEXT_HEADERS = {"X-Auth-Token": auth_token, "Content-Type": "text/plain"}

json = {
    "name": "sia",
    "commercial_type": "DEV1-S",
    "image": "89c80d27-ddf4-4ffa-8215-b335cce3fd05",
    "organization": organization
}

cloud_init_script = "#!/bin/bash\n git clone " + SETUP_REPO + "\n sh /SiaScripts/setup-sia.sh"

# create server
server = requests.post(BASE_URL + "/servers", headers=JSON_HEADERS, json=json)
id = server["id"]

# server created
#server = requests.get(BASE_URL + "/servers", headers=JSON_HEADERS).json()
#id = server["servers"][0]["id"]

resp = requests.patch(BASE_URL + "/servers/" + id + "/user_data/cloud-init", headers=TEXT_HEADERS, data=cloud_init_script)
resp = requests.post(BASE_URL + "/servers/" + id + "/action", headers=JSON_HEADERS, json={"action": "poweron"})
print resp.text
