from twilio.rest import Client
from tracker.models import Challenge, Profile
from django.contrib.auth.models import User
from django.utils import timezone
from decouple import config


def send_message(request, user_phone):
    account_sid = config("account_sid")
    auth_token = config("auth_token")
    client = Client(account_sid, auth_token)
    # Retrieve challenges for today
    today = timezone.now().date()
    profile = request.user.profile
    challenges = Challenge.objects.filter(profile = profile, challenge_date=today)

    # Construct the message body
    message_body = f"Hello, your daily challenges for today are:\n"
    for challenge in challenges:
        message_body += f"- {challenge.challenge}\n"

    # Convert the PhoneNumber object to a string
    user_phone_str = str(user_phone)

    # Send the message to the user's phone number
    message = client.messages.create(
        messaging_service_sid= config("messaging_service_sid"),
        body=message_body,
        to=user_phone_str
    )

    print(message.sid)
