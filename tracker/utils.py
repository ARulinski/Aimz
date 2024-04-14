from twilio.rest import Client
from django.conf import settings
from decouple import config

def send_verification_code(user):
    # Retrieve Twilio credentials from settings
    account_sid = config("TWILIO_ACCOUNT_SID")
    auth_token = config("TWILIO_AUTH_TOKEN")
    verify_service_sid = config('verify_service_sid')

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    try:
        # Send verification code using Twilio Verify service
        verification = client.verify \
                            .services(verify_service_sid) \
                            .verifications \
                            .create(to=f'phone_number:{user.profile.phone_number}', channel='sms')
        print(verification.status)  
        return True 
    except Exception as e:
        print(f"Failed to send verification code: {e}")  # Log error for debugging
        return False

def verify_code_with_twilio(phone_number, code):
    # Retrieve Twilio credentials from settings
    account_sid = config("TWILIO_ACCOUNT_SID")
    auth_token = config("TWILIO_AUTH_TOKEN")
    verify_service_sid = config('verify_service_sid')

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    try:
        # Check if the verification code is valid using Twilio Verify service
        verification_check = client.verify \
                                   .services(verify_service_sid) \
                                   .verification_checks \
                                   .create(to=f'phone_number:{phone_number}', code=code)
        if verification_check.status == 'approved':
            # Code is verified successfully by Twilio
            print("code is verified!")
            return True
            
        else:
            # Code verification failed
            print("verification Failed")
            return False
    except Exception as e:
        # Log any errors for debugging
        print(f"Error verifying code with Twilio: {e}")
        return False