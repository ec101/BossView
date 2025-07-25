import requests
import urllib3

# Optional: to disable warnings in case of unsecured https connections.
urllib3.disable_warnings()

def get_access_token(load_balancer: str, username: str, password: str, group: str):
    url = f"{load_balancer}/v1/api/auth"

    payload='scope=openid&response_type=code&client_id=external-client&redirect_uri=mx%3A%2F%2F'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # Get authorization code from user + password
    response = requests.request("POST", f"{url}/authorize", headers=headers, data=payload, auth=(username, password), verify=False)
    
    authorization_code = response.text

    payload=f"grant_type=authorization_code&mx_gp={group}&mx_ext_ip=127.0.0.1"
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {authorization_code}'
    }

    # Get jwt from authorization code + group
    response = requests.request("POST", f"{url}/token", headers=headers, data=payload, verify=False)

    return response.json()["access_token"]


