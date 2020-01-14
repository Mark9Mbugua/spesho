# import package
import africastalking
from twilio.rest import Client
from decouple import config
from celery import shared_task
from .models import Profile

# Initialize SDK
username = config('AFRICA_TALKING_USER_NAME')  # use 'sandbox' for development in the test environment
api_key = config('AFRICA_TALKING_API_KEY')  # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)

# Your Account Sid and Auth Token from twilio.com/console
account_sid = config('TWILIO_SID')
auth_token = config('TWILIO_SECRET_KEY')

client = Client(account_sid, auth_token)

# Initialize a service e.g. SMS
sms = africastalking.SMS

@shared_task()
def send_confirmation_code(code, recipient):
    """
    sends the  Hashids
    :param recipient:
    :param code: string
    :return: obj
    """
    sender_number = config('TWILIO_PHONE_NUMBER')
    message = client.messages.create(
                     body=code,
                     from_=sender_number,
                     to=recipient
                 )

    return message.status


@shared_task()
def fall_back_confirmation_code(code, recipient):
    """
    function is asynchronous
    sending Hashids to users to verify codes
    :param recipient:
    :param code: string
    :return: object
    """

    response = sms.send(code, [recipient])
    if response['SMSMessageData']['Recipients'][0]['status'] == 'Success':
        return True
    return False