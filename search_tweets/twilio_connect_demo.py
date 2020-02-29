import os
from twilio.rest import Client


def twilio_connect():
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)
    return client


def send_message(client):
    return client.messages.create(
        from_=os.environ.get("TWILIO_PHONE_NUMBER"),
        to=os.environ.get("CELL_PHONE_NUMBER"),
        body="You don't have to move your car tonight. Enjoy your night!",
    )
