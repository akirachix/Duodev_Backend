import base64
from datetime import datetime
import requests
from payments.auth import get_access_token
import os 
# Generate password based on shortcode, passkey, and timestamp
def generate_password(shortcode, passkey):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f'{shortcode}{passkey}{timestamp}'.encode()).decode('utf-8')
    return password

# Get the current timestamp
def get_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')

# Query M-Pesa payment status
def query_mpesa_payment_status(checkout_request_id):
    access_token = get_access_token()  # Access token should be invoked with parentheses
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"  # Production URL for live systems
    
    shortcode = os.getenv('MPESA_SHORTCODE')
    passkey = os.getenv('MPESA_PASSKEY')
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    # Generate the password for querying
    password = generate_password(shortcode, passkey)
    
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,  # Use the generated password
        "Timestamp": get_timestamp(),
        "CheckoutRequestID": checkout_request_id,
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        result_code = result.get('ResultCode')

        if result_code == "0":
            return {
                'status': 'success',
                'message': 'Payment was successful',
                'data': result
            }
        else:
            return {
                'status': 'error',
                'message': 'Payment failed or is pending',
                'data': result
            }
    else:
        return {
            'status': 'error',
            'message': 'Failed to query payment status',
            'data': response.text
        }
