import requests
import json
import  uuid
from basicauth import encode
from decouple import config
import time

class MomoPaymentRequest:
    """ MTN MoMo API For Production Testing """

    _hostname  = "https://proxy.momoapi.mtn.com"
    _username  = config("USERNAME", cast=str)
    _password  = config("PASSWORD", cast=str)
    _subscription_key = config("SUBSCRIPTION_KEY", cast=str)

    def __init__(self, amount, phone_number, currency, payer_msg, id=None) -> None:
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        
        self.amount = amount
        self.phone_number = phone_number
        self.currency = currency
        self.payer_msg = payer_msg

    def __basic_auth(self):
        return str(encode(self._username, self._password))

    def __access_token(self):
        """Generate momo api access token to be used to authenticate other endpoints """
        url = f"{self._hostname}/collection/token/"

        headers = {
            'Authorization': self.__basic_auth(),
            'Ocp-Apim-Subscription-Key': self._subscription_key,
        }

        try:
            response = requests.request("POST", url, headers=headers, data={})
            print(response.status_code)
            print(response.reason)

            if (response.status_code == 200 or response.status_code == 202):
                auth_token = response.json()['access_token']
                print(auth_token)
                return auth_token
            
            # method failed
            return None
        except Exception as e:
            print(f"[Errno] {e}")
            return None

    def send(self):
        reference_id = self.id
        access_token = self.__access_token()

        if not access_token:
            print("request failed")
            return "Request failed."
        
        authorization = f"Bearer {access_token}"

        payload = json.dumps({
            "amount": self.amount,
            "currency": self.currency,
            "externalId": "12345",
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": self.phone_number
            },
            "payerMessage": self.payer_msg,
            "payeeNote": self.payer_msg
        })

        url = f"{self._hostname}/collection/v1_0/requesttopay"

        headers = {
            'X-Reference-Id': reference_id,
            'X-Target-Environment': 'mtnzambia', 
            'Ocp-Apim-Subscription-Key': self._subscription_key,
            'Authorization': authorization,
        }

        response = requests.post(url, headers=headers, data=payload)

        print(f"Reference ID: {reference_id}")
        print(response.status_code)
        if (response.status_code == 200 or response.status_code == 202):
            print(response.reason)
            pass
        
    def payment_status(self, reference_id):
        error_msg = "Failed to generate access token"
        access_token = self.__access_token()

        if access_token:
            print(error_msg)
            return error_msg
    
        authorization = f"Bearer {access_token}"

        headers = {
            'X-Target-Environment': 'mtnzambia', 
            'Ocp-Apim-Subscription-Key': self._subscription_key,
            'Authorization': authorization
        }

        url = f"{self._hostname}/collection/v1_0/requesttopay/{reference_id}"

        response = requests.get(url, headers=headers)

        print(response.status_code)
        print(response.reason)
        if response.status_code == 202 or response.status_code:
            print(response.reason)
            print(response.json())

if __name__ == "__main__":
    payer_number = "260761423699"

    req = MomoPaymentRequest("1", payer_number, "ZMW", "test payment 1")
    req.send()
    time.sleep(10)
    req.payment_status(req.id)
