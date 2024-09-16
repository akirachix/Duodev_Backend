import base64
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_access_token():
    """
    Fetch the access token from Safaricom API.
    """
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET

    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

































    headers = {
        'Authorization': f'Basic {encoded_credentials}'
    }

    response = requests.get(api_url, headers=headers)
    json_response = response.json()

    if response.status_code == 200:
        access_token = json_response['access_token']
        logger.info(f'Access token fetched successfully: {access_token}')
        return access_token
    else:
        logger.error(f'Error fetching access token: {json_response}')
        raise Exception('Error fetching access token')
