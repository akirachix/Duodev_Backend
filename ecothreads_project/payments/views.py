import base64
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
from payments.models import Payment
from payments.utils import query_mpesa_payment_status
from users.models import User
mpesa_token = settings.MPESA_ACCESS_TOKEN_LINK
# Set up logging
logger = logging.getLogger(__name__)

# payments/views.py
@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            amount = data.get('amount')
            user_id = data.get('user_id') 

            if not phone_number or not amount or not user_id:
                return JsonResponse({'error': 'Phone number, amount, and user ID are required'}, status=400)

            try:
                user = User.objects.get(id=user_id)  
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            shortcode = settings.MPESA_SHORTCODE
            passkey = settings.MPESA_PASSKEY
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = base64.b64encode(f'{shortcode}{passkey}{timestamp}'.encode()).decode('utf-8')
            mpesa_link = settings.MPESA_LINK

            payload = {
                "BusinessShortCode": shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": 'https://mydomain.com/path',  
                "AccountReference": "Eco-Threads Hub",
                "TransactionDesc": "Payment for Eco-Threads Hub"
            }

            # Save the initial payment record
            payment = Payment.objects.create(
                user=user,
                checkout_request_id='',  # To be updated after successful request
                amount=amount,
                phone_number=phone_number,
                status='pending'
            )

            response = requests.post(
                mpesa_link,
                json=payload,
                headers={
                    'Authorization': f'Bearer {get_access_token()}',
                    'Content-Type': 'application/json'
                }
            )

            response_data = response.json()
            logger.info(f'STK push response: {response_data}')

            # Update the payment record with the checkout_request_id
            payment.checkout_request_id = response_data.get('CheckoutRequestID')
            payment.save()

            return JsonResponse(response_data)
        except Exception as e:
            logger.error(f'Error processing payment: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)


# payments/views.py
@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            logger.debug("Received payload: %s", payload)

            stk_callback = payload.get('Body', {}).get('stkCallback', {})
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            transaction_id = stk_callback.get('TransactionID')  # Example field if available

            try:
                payment = Payment.objects.get(checkout_request_id=checkout_request_id)
                if result_code == "0":  # Payment successful
                    payment.status = 'completed'
                    payment.transaction_id = transaction_id
                    logger.info("Payment successful: %s", result_desc)
                    return JsonResponse({'status': 'success', 'message': 'Payment was successful'})
                else:
                    payment.status = 'failed'
                    logger.error("Payment failed: %s", result_desc)
                    return JsonResponse({'status': 'error', 'message': 'Payment failed'}, status=400)
                payment.save()
            except Payment.DoesNotExist:
                logger.error("Payment with CheckoutRequestID %s does not exist", checkout_request_id)
                return JsonResponse({'status': 'error', 'message': 'Payment record not found'}, status=404)

        except json.JSONDecodeError:
            logger.error("Invalid JSON payload")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error("Exception occurred: %s", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def get_access_token():
    api_url = mpesa_token
    headers = {
        'Authorization': f'Basic {base64.b64encode(f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}".encode()).decode()}'
    }
    response = requests.get(api_url, headers=headers)
    json_response = response.json()

    if response.status_code == 200:
        access_token = json_response['access_token']
        logger.info(f'Generated Access Token: {access_token}')
        return access_token
    else:
        logger.error(f'Error getting access token: {json_response}')
        raise Exception('Error getting access token')

def check_payment_status_view(request):
    checkout_request_id = request.GET.get('checkout_request_id')  # Get the CheckoutRequestID from the request
    
    if not checkout_request_id:
        return JsonResponse({'status': 'error', 'message': 'Missing CheckoutRequestID'}, status=400)

    # Query the payment status
    result = query_mpesa_payment_status(checkout_request_id)
    
    # Check if the payment exists in the database
    payment = Payment.objects.filter(checkout_request_id=checkout_request_id).first()

    if payment:
        # Update the existing payment record
        payment.status = result.get('status')
        payment.message = result.get('message')
        payment.save()
    else:
        # Create a new payment record
        Payment.objects.create(
            checkout_request_id=checkout_request_id,
            status=result.get('status'),
            message=result.get('message')
        )

    return JsonResponse(result)