from dotenv import load_dotenv
import requests
import os

load_dotenv()
load_dotenv('.env.local', override=True)
processing_address = os.getenv("URI_PROCESSING_ADDRESS")


class Processing:

    @staticmethod
    def create_order(form):
        response = requests.post(processing_address, {
            'firstname': form.firstname.data,
            'lastname': form.lastname.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'address': form.address.data,
            'period': form.period.data,
        })
        response_json = response.json()
        if response.status_code == 200 and response_json["status"] == "new":
            return True
        else:
            return False
