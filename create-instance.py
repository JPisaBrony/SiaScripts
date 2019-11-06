import requests
import os.path
import json

BASE_URL = "https://api.scaleway.com/instance/v1/zones/fr-par-1"
SETUP_REPO = "https://github.com/JPisaBrony/SiaScripts"
SETTINGS_FILE = "settings.json"
auth_token = None
organization = None
s3backer_passwd = None
sia_wallet_pass = None

if os.path.isfile(SETTINGS_FILE):
    data = None
    with open(SETTINGS_FILE) as f:
        data = json.load(f)
    
    auth_token = data["auth_token"]
    organization = data["organization"]
    s3backer_passwd = data["s3backer_passwd"]
    sia_wallet_pass = data["sia_wallet_pass"]
else:
    print SETTINGS_FILE + " doesn't exist"
    exit(0)

JSON_HEADERS = {"X-Auth-Token": auth_token, "Content-Type": "application/json"}
TEXT_HEADERS = {"X-Auth-Token": auth_token, "Content-Type": "text/plain"}

json_payload = {
    "name": "sia",
    "commercial_type": "DEV1-S",
    "image": "89c80d27-ddf4-4ffa-8215-b335cce3fd05",
    "organization": organization
}

# create server
server = requests.post(BASE_URL + "/servers", headers=JSON_HEADERS, json=json_payload).json()
id = server["server"]["id"]

# server created
#server = requests.get(BASE_URL + "/servers", headers=JSON_HEADERS).json()
#id = server["servers"][0]["id"]

# create cloud init script
cloud_init_script = "#!/bin/bash\n git clone " + SETUP_REPO + "\n sh /SiaScripts/setup-sia-screen.sh"
resp = requests.patch(BASE_URL + "/servers/" + id + "/user_data/cloud-init", headers=TEXT_HEADERS, data=cloud_init_script)

# set s3backer_passwd user data
resp = requests.patch(BASE_URL + "/servers/" + id + "/user_data/s3backer_passwd", headers=TEXT_HEADERS, data=s3backer_passwd)

# set sia_wallet_pass user data
resp = requests.patch(BASE_URL + "/servers/" + id + "/user_data/sia_wallet_pass", headers=TEXT_HEADERS, data=sia_wallet_pass)

# power on server
resp = requests.post(BASE_URL + "/servers/" + id + "/action", headers=JSON_HEADERS, json={"action": "poweron"})
print resp.text
