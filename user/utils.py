import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

load_dotenv()

client = Client(os.getenv('account_sid'), os.getenv('auth_token'))
verify = client.verify.v2.services(os.getenv('service_sid'))


def send(phone):
    verify.verifications.create(to=phone, channel='sms')


def check(phone, code):
    try:
        result = verify.verification_checks.create(
            to=phone, code=code
        )
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'