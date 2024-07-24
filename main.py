from flask import Flask, request, render_template_string, jsonify
import api
import error_html
import main_web_page
import success_html
import results_html
import logging
import threading
import time

app = Flask(__name__)

TEAM_NAME = "CTRL_ALT_DEFEAT"

logging.basicConfig(level=logging.INFO)


@app.route('/')
def index():
    return main_web_page.web_HTML.format(team_name=TEAM_NAME)


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    phone_number = request.form['phoneNumber']
    if api.register_number(name, phone_number):
        return render_template_string(success_html.success_result)
    else:
        error_message = "Failed to register. Please check your phone number and try again."
        return render_template_string(error_html.error_result, error_message=error_message)


@app.route('/unregister', methods=['POST'])
def unregister():
    phone_number = request.form['phoneNumber']
    if api.unregister_number(phone_number):
        return jsonify({"status": "success", "message": "Phone number unregistered successfully"}), 200
    else:
        return jsonify({"status": "error",
                        "message": "Failed to unregister phone number. It may not be registered or associated with this team."}), 400


@app.route('/results')
def results():
    overall_results = api.get_results()
    return render_template_string(results_html.results_template, results=overall_results)


@app.route('/test_sms/<phone_number>')
def test_sms(phone_number):
    result = api.send_sms(phone_number, "This is a test message from the health survey app.")
    if result:
        return "Test SMS sent successfully. Please check your phone."
    else:
        return "Failed to send test SMS. Please check the logs for more information."


@app.route('/process_messages', methods=['GET'])
def process_messages():
    api.fetch_and_process_messages()
    return "Messages processed", 200


def message_polling():
    while True:
        api.fetch_and_process_messages()
        time.sleep(10)  # Poll every 10 seconds


if __name__ == '__main__':
    # Start the message polling in a separate thread
    polling_thread = threading.Thread(target=message_polling)
    polling_thread.daemon = True
    polling_thread.start()

    app.run(debug=True, use_reloader=False)
