import requests
import logging
from datetime import datetime, timezone
import json

logging.basicConfig(level=logging.INFO)

API_BASE_URL = "http://hackathons.masterschool.com:3030"
TEAM_NAME = "CTRL_ALT_DEFEAT"
HACKATHON_NUMBER = "491771786208"  # The hackathon's number without the '+' sign

SURVEY = [
    "What is your age group? Reply with A (18-25), B (26-35), C (36-45), D (46+)",
    "How often do you exercise? A (Daily), B (2-3 times a week), C (Once a week), D (Rarely)",
    "How would you rate your overall health? A (Excellent), B (Good), C (Fair), D (Poor)"
]

# In-memory storage for user data and overall results
user_data = {}


def save_old_data(phone_number, data):
    filename = f"old_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump({phone_number: data}, f)
    logging.info(f"Old data for {phone_number} saved to {filename}")


def register_number(name, phone_number):
    logging.info(f"Preparing registration for: {phone_number} for {name}")

    # Save and clear existing data for this phone number if it exists
    if phone_number in user_data:
        logging.info(f"Saving and clearing existing data for {phone_number}")
        save_old_data(phone_number, user_data[phone_number])
        del user_data[phone_number]

    endpoint = f"{API_BASE_URL}/team/registerNumber"
    data = {"phoneNumber": phone_number, "teamName": TEAM_NAME}
    try:
        response = requests.post(endpoint, json=data)
        logging.info(f"Register API response status: {response.status_code}")
        logging.info(f"Register API response content: {response.text}")

        if response.status_code != 200 and "already exists" not in response.text:
            logging.error(f"Failed to register number with API. Status code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"An error occurred during API registration: {str(e)}")
        return False

    welcome_msg = (
        f"Welcome {name} to our health survey! To start, send 'SUBSCRIBE {TEAM_NAME}' to {HACKATHON_NUMBER}. "
        f"After subscribing, you'll receive the first question.")

    if send_sms(phone_number, welcome_msg):
        registration_time = datetime.now(timezone.utc).isoformat()
        user_data[phone_number] = {
            "name": name,
            "responses": [],
            "current_question": 0,
            "subscribed": False,
            "registration_time": registration_time,
            "last_processed_time": registration_time
        }
        logging.info(f"User data created for {phone_number} with registration time set to {registration_time}")
        logging.info(f"Current user_data: {user_data}")
        return True
    else:
        logging.error(f"Failed to send SMS to {phone_number}")
        return False


def unregister_number(phone_number):
    logging.info(f"Attempting to unregister number: {phone_number}")
    endpoint = f"{API_BASE_URL}/team/unregisterNumber"
    data = {"phoneNumber": phone_number, "teamName": TEAM_NAME}
    try:
        response = requests.post(endpoint, json=data)
        logging.info(f"Unregister API response status: {response.status_code}")
        logging.info(f"Unregister API response content: {response.text}")
        if response.status_code == 200:
            if phone_number in user_data:
                save_old_data(phone_number, user_data[phone_number])
                del user_data[phone_number]
            logging.info(f"User data cleared for {phone_number}")
            return True
        else:
            logging.error(f"Unregistration failed with status code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"An error occurred during unregistration: {str(e)}")
        return False


def send_sms(phone_number, message):
    logging.info(f"Attempting to send SMS to: {phone_number}")
    logging.info(f"Message content: {message}")
    endpoint = f"{API_BASE_URL}/sms/send"
    data = {
        "phoneNumber": phone_number,
        "message": message,
        "sender": HACKATHON_NUMBER
    }
    try:
        logging.info(f"Sending request to {endpoint} with data: {data}")
        response = requests.post(endpoint, json=data)
        logging.info(f"SMS API response status: {response.status_code}")
        logging.info(f"SMS API response content: {response.text}")

        if response.status_code == 200:
            response_json = response.json()
            logging.info(f"Full API response: {response_json}")
            if 'messages' in response_json and len(response_json['messages']) > 0:
                message_status = response_json['messages'][0]['status']['name']
                message_description = response_json['messages'][0]['status']['description']
                logging.info(f"Message status: {message_status}")
                logging.info(f"Message description: {message_description}")
                if message_status == "PENDING_ACCEPTED":
                    logging.info(f"SMS to {phone_number} accepted for delivery")
                    return True
                else:
                    logging.error(
                        f"SMS to {phone_number} not accepted. Status: {message_status}, Description: {message_description}")
                    return False
            else:
                logging.error(f"Unexpected response format from SMS API: {response.text}")
                return False
        else:
            logging.error(f"SMS API returned non-200 status code: {response.status_code}")
            return False
    except Exception as e:
        logging.error(f"An error occurred while sending SMS: {str(e)}")
        return False


def process_message(phone_number, message):
    logging.info(f"Processing message from {phone_number}: {message}")
    if phone_number not in user_data:
        logging.warning(f"Unregistered number {phone_number} attempting to use the service")
        return None

    user = user_data[phone_number]
    message = message.strip().upper()
    logging.info(f"Processed message: {message}")

    if not user["subscribed"]:
        if message == f"SUBSCRIBE {TEAM_NAME}":
            user["subscribed"] = True
            user["current_question"] = 0
            logging.info(f"User {phone_number} successfully subscribed. Sending first question.")
            return SURVEY[0]  # Send the first question
        else:
            logging.warning(f"User {phone_number} sent incorrect subscription message: {message}")
            return f"To start the survey, please send 'SUBSCRIBE {TEAM_NAME}' first."
    elif message == f"SUBSCRIBE {TEAM_NAME}":
        # User is already subscribed, resend the current question
        logging.info(f"User {phone_number} is already subscribed. Resending current question.")
        return SURVEY[user["current_question"]]
    elif message in ['A', 'B', 'C', 'D']:
        if user["current_question"] < len(SURVEY):
            user["responses"].append(message)
            user["current_question"] += 1

            if user["current_question"] < len(SURVEY):
                logging.info(f"Sending next question to user {phone_number}")
                return SURVEY[user["current_question"]]
            else:
                logging.info(f"Survey completed for user {phone_number}")
                return end_survey(phone_number)
        else:
            logging.warning(f"Received answer after survey completion from user {phone_number}")
            return "You have already completed the survey. Thank you for your participation!"
    else:
        logging.warning(f"Invalid response from user {phone_number}: {message}")
        return f"Invalid response. Please reply with A, B, C, or D to answer the question. Current question: {SURVEY[user['current_question']]}"


def end_survey(phone_number):
    user = user_data[phone_number]
    name = user["name"]
    responses = user["responses"]
    result_message = f"Thank you for completing the survey, {name}. Here are your results:\n"
    for i, answer in enumerate(responses):
        result_message += f"Question {i + 1}: {answer}\n"
    result_message += "\nThank you for participating in our health survey!"
    return result_message


def get_results():
    current_results = [{} for _ in SURVEY]
    for phone_number, user in user_data.items():
        for i, response in enumerate(user['responses']):
            if i < len(current_results):
                current_results[i][response] = current_results[i].get(response, 0) + 1
    return current_results


def fetch_and_process_messages():
    logging.info(f"Current user_data at start of fetch_and_process_messages: {user_data}")
    endpoint = f"{API_BASE_URL}/team/getMessages/{TEAM_NAME}"
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            messages = response.json()
            logging.info(f"Fetched messages: {messages}")

            if isinstance(messages, list):
                logging.info(f"Fetched {len(messages)} message groups")
                for message_group in messages:
                    for phone_number, message_list in message_group.items():
                        if phone_number in user_data:
                            logging.info(f"Processing messages for registered user {phone_number}")
                            registration_time = datetime.fromisoformat(user_data[phone_number]['registration_time'])
                            last_processed_time = datetime.fromisoformat(
                                user_data[phone_number].get('last_processed_time',
                                                            user_data[phone_number]['registration_time']))

                            # Filter messages received after last processed time
                            new_messages = [
                                msg for msg in message_list
                                if datetime.fromisoformat(msg['receivedAt']) > last_processed_time
                            ]

                            if new_messages:
                                logging.info(f"Found {len(new_messages)} new messages for {phone_number}")
                                # Process only the most recent message
                                latest_message = max(new_messages, key=lambda x: x['receivedAt'])
                                logging.info(
                                    f"Processing latest message: {latest_message['text']} (received at {latest_message['receivedAt']})")
                                response = process_message(phone_number, latest_message['text'])
                                if response:
                                    send_sms(phone_number, response)
                                user_data[phone_number]['last_processed_time'] = latest_message['receivedAt']
                            else:
                                logging.info(f"No new messages to process for {phone_number}")
                        else:
                            logging.info(f"Skipping messages for unregistered number {phone_number}")
            else:
                logging.error(f"Unexpected message format: {type(messages)}")
        else:
            logging.error(f"Failed to fetch messages. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred while fetching messages: {str(e)}")
        logging.exception("Exception details:")