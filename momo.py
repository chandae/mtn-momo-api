import requests
import json
import  uuid
from basicauth import encode
from decouple import config
import time

class MTNOpenAPI:
    """ MTN MoMo API For Production Testing """

    __hostname  = "https://proxy.momoapi.mtn.com"
    __collection_username  = config("COLLECTION_USERNAME", cast=str)
    __collection_password  = config("COLLECTION_PASSWORD", cast=str)
    __collection_subscription_key = config("COLLECTION_SUBSCRIPTION_KEY", cast=str)
    __disbursement_username  = config("DISBURSEMENT_USERNAME", cast=str)
    __disbursement_password  = config("DISBURSEMENT_PASSWORD", cast=str)
    __disbursement_subscription_key = config("DISBURSEMENT_SUBSCRIPTION_KEY", cast=str)

    def __init__(self, amount, phone, currency, payer_msg, id=None) -> None:
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
    
        self.amount   = amount
        self.phone    = phone
        self.currency = currency
        self.message  = payer_msg

    def __basic_auth(self, request_type):
        if request_type == "collection":
            return str(encode(self.__collection_username, self.__collection_password))
        elif request_type == "disbursement":
            return str(encode(self.__disbursement_username, self.__disbursement_password))

    def __collection_access_token(self):
        """Generate momo api access token to be used to authenticate other endpoints """
        url = f"{self.__hostname}/collection/token/"
        key = self.__collection_subscription_key 

        headers = {
            'Authorization': self.__basic_auth('collection'),
            'Ocp-Apim-Subscription-Key': key,
        }

        try:
            response = requests.request("POST", url, headers=headers, data={})
            print(response.status_code)
            print(response.reason)

            if (response.status_code == 200 or response.status_code == 202):
                auth_token = response.json()['access_token']
                print(auth_token)
                return auth_token
            else:
                print("Failed to generate collection access token")
        except Exception as e:
            print(f"[Errno] {e}")
        return None
    
    def __disbursement_access_token(self):
        url = f"{self.__hostname}/disbursement/token/"

        headers = {
            'Authorization': self.__basic_auth(request_type='disbursement'),
        }

        try:
            response = requests.request("POST", url, headers=headers, data={})
            print(response.status_code)
            print(response.reason)

            if (response.status_code == 200 or response.status_code == 202):
                auth_token = response.json()['access_token']
                print(auth_token)
                return auth_token
            else:
                print("Failed to generate disbursement access token")
        except Exception as e:
            print(f"[Errno] {e}")
        return None

    def __generate_token(self, request_type):
        if request_type == "collection":
            return self.__collection_access_token()
        elif request_type == "disbursement":
            return self.__disbursement_access_token()

    def payment(self):
        reference_id = self.id
        subscription = self.__collection_subscription_key
        access_token = self.__generate_token(request_type="collection")
        
        if not access_token:
            print("request failed")
            return "Request failed."
        
        authorization = f"Bearer {access_token}"

        payload = json.dumps({
            "amount": self.amount,
            "currency": self.currency,
            "externalId": "123456",
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": self.phone
            },
            "payerMessage": self.message,
            "payeeNote": self.message
        })

        url = f"{self.__hostname}/collection/v1_0/requesttopay"

        headers = {
            'X-Reference-Id': reference_id,
            'X-Target-Environment': 'mtnzambia', 
            'Ocp-Apim-Subscription-Key': subscription,
            'Authorization': authorization,
        }

        response = requests.post(url, headers=headers, data=payload)

        print(f"Reference ID: {reference_id}")
        print(response.status_code)
        if (response.status_code == 200 or response.status_code == 202):
            print(response.reason)
            pass
    
    def payment_status(self):
        error_msg = "Failed to generate access token"
        subscription = self.__collection_subscription_key
        access_token = self.__generate_token(request_type="collection")

        if not access_token:
            print(error_msg)
            return error_msg
    
        authorization = f"Bearer {access_token}"

        headers = {
            'X-Target-Environment': 'mtnzambia', 
            'Ocp-Apim-Subscription-Key': subscription,
            'Authorization': authorization
        }

        url = f"{self.__hostname}/collection/v1_0/requesttopay/{self.id}"

        response = requests.get(url, headers=headers)

        print(response.status_code)
        print(response.reason)
        if response.status_code == 202 or response.status_code:
            print(response.reason)
            print(response.json())
    
    def payout(self):
        reference_id = self.id
        access_token = self.__generate_token(request_type="disbursement")

        if not access_token:
            print("Request failed")
            return "Request failed."
        
        authorization = f"Bearer {access_token}"

        url = f"{self.__hostname}/disbursement/v1_0/transfer"

        headers = {
            'Authorization': authorization,
            'X-Reference-Id': reference_id,
            'X-Target-Environment': 'mtnzambia', 
        }

        payload = json.dumps({
            "amount": self.amount,
            "currency": self.currency,
            "externalId": "12345",
            "payee": {
                "partyIdType": "MSISDN",
                "partyId": self.phone
            },
            "payerMessage": self.message,
            "payeeNote": self.message
        })

        response = requests.post(url, headers=headers, data=payload)

        print(f"Reference ID: {reference_id}")
        print(response.status_code)
        print(response.reason)
        if (response.status_code == 200 or response.status_code == 202):
            print(f"Funds disbursed to {self.phone}. Amount ZMW {self.amount}")

if __name__ == "__main__":
    test_number = ""

    req = MTNOpenAPI("1", test_number, "ZMW", "test transfer")
    # req.payment()
    # time.sleep(15)
    # req.payment_status()
    # req.payout()
    