import requests
import time

API_BASE_URL = "http://hackathons.masterschool.com:3030"
TEAM_NAME = "ctrlaltdefeat"
SENDER = "CTRL_ALT_DELETE"
TEST_PHONE_NUMBER = ""  # Enter hier the number that you want to test the API with


def register_number(phone_number):
    endpoint = f"{API_BASE_URL}/team/registerNumber"
    data = {"phoneNumber": phone_number, "teamName": TEAM_NAME}
    response = requests.post(endpoint, json=data)
    print(f"Register number response: {response.status_code}")
    print(response.text)
    return response.status_code == 200


def send_sms(phone_number, message):
    endpoint = f"{API_BASE_URL}/sms/send"
    data = {"phoneNumber": phone_number, "message": message, "sender": SENDER}
    response = requests.post(endpoint, json=data)
    print(f"Send SMS response: {response.status_code}")
    print(response.text)
    return response.status_code == 200


def get_messages():
    endpoint = f"{API_BASE_URL}/team/getMessages/{TEAM_NAME}"
    response = requests.get(endpoint)
    print(f"Get messages response: {response.status_code}")
    if response.status_code == 200:
        messages = response.json()
        print(f"Received {len(messages)} messages:")
        for msg in messages:
            print(f"From: {msg['sender']}, Message: {msg['message']}, Received at: {msg['receivedAt']}")
        return messages
    else:
        print("Failed to retrieve messages")
        return []


# Test the full flow
print("Step 1: Registering number...")
if register_number(TEST_PHONE_NUMBER):
    print(f"\nStep 2: Sending test SMS to {TEST_PHONE_NUMBER}...")
    if send_sms(TEST_PHONE_NUMBER, "This is a test message. Please reply with 'TEST'"):
        print("\nSMS sent successfully. Please check the phone and reply to the message.")
        print("\nWaiting for 60 seconds to allow time for a reply...")
        time.sleep(60)

        print("\nStep 3: Checking for messages...")
        messages = get_messages()

        # Check if we received a reply
        reply = next((msg for msg in messages if
                      msg['sender'] == TEST_PHONE_NUMBER and msg['message'].strip().upper() == 'TEST'), None)

        if reply:
            print(f"\nSuccess! Received reply: {reply['message']}")
        else:
            print("\nNo matching reply found. Make sure you sent a reply with 'TEST'.")
    else:
        print("Failed to send SMS. Please check your sender ID and try again.")
else:
    print("Failed to register the number. Please check your team name and try again.")

print("\nTest complete. Please check the console output for results.")