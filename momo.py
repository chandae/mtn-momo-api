import requests
import json
import  uuid
from basicauth import encode
from decouple import config

_hostname  = "https://proxy.momoapi.mtn.com"
_username  = config("USERNAME", cast=str)
_password  = config("PASSWORD", cast=str)

_subscription_key = config("SUBSCRIPTION_KEY", cast=str)

def generate_access_token():
    """Generate momo api access token to be used to authenticate other endpoints """
    basic_auth = str(encode(_username, _password))

    headers = {
        'Authorization': basic_auth,
        'Ocp-Apim-Subscription-Key': _subscription_key,
    }

    url = f"{_hostname}/collection/token/"

    try:
        response = requests.request("POST", url, headers=headers, data={})
        auth_token = response.json()['access_token']
        print(response.status_code)
        print(auth_token)
        return auth_token
    except Exception as e:
        print(f"[Errno] {e}")
        return None

def request_to_pay(phone_number, amount, payer_message):
    reference_id = str(uuid.uuid4())
    access_token = generate_access_token()

    if not access_token:
        print("request failed")
        return "Request failed."
    
    authorization = f"Bearer {access_token}"

    payload = json.dumps({
        "amount": amount,
        "currency": "ZMW",
        "externalId": "12345",
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": phone_number
        },
        "payerMessage": payer_message,
        "payeeNote": payer_message
    })

    url = f"{_hostname}/collection/v1_0/requesttopay"

    headers = {
        'X-Reference-Id': reference_id,
        'X-Target-Environment': 'mtnzambia', 
        'Ocp-Apim-Subscription-Key': _subscription_key,
        'Authorization': authorization,
    }

    response = requests.post(url, headers=headers, data=payload)

    print(f"Reference ID: {reference_id}")
    print(response.status_code)
    if (response.status_code == 200 or response.status_code == 202):
        print(response.reason)

def payment_status(reference_id):
    access_token = generate_access_token()
    authorization = f"Bearer {access_token}"

    headers = {
        'X-Target-Environment': 'mtnzambia', 
        'Ocp-Apim-Subscription-Key': _subscription_key,
        'Authorization': authorization
    }

    url = f"{_hostname}/collection/v1_0/requesttopay/{reference_id}"

    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 202 or response.status_code:
        print(response.reason)
        print(response.json())


if __name__ == "__main__":
    payer_number = "0761423699"
    reference_id = "c9b28b44-7943-4f53-a421-07502e162d9e"

    # request_to_pay("260761423699", "5", "demo payment")
    payment_status(reference_id)

