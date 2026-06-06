import json
import os
import requests
from dotenv import load_dotenv


def load_config(config_path):
    """
    Load reminder configuration and create the payload
    to be sent to Discord.
    """

    # Open and read config.json
    with open(config_path, "r") as file:
        config = json.load(file)

    # Stop execution if reminders are disabled
    if not config["enabled"]:
        print("Reminder Disabled")
        exit()

    # Retrieve message from config
    message = config.get("message")

    # Ensure message exists
    if message is None:
        print("Message missing from config")
        exit()

    # Discord expects a dictionary with a "content" key
    message_payload = {
        "content": message
    }

    return message_payload


def send_reminder(url, message_payload):
    """
    Send reminder to Discord and return the HTTP status code.
    """

    response = requests.post(
        url,
        json=message_payload,
        timeout=10
    )

    return response.status_code


def main():
    """
    Main execution flow.
    """

    # Load environment variables from .env
    load_dotenv()

    # Retrieve webhook URL
    url = os.getenv("DISCORD_WEBHOOK")

    # Ensure webhook URL exists
    if not url:
        print("URL does not exist.")
        exit()

    # Load message configuration
    message_payload = load_config("config.json")

    # Send reminder and capture status code
    status_code = send_reminder(url, message_payload)

    # Handle response
    if status_code == 204:
        print(f"Reminder Posted: {status_code}")

    elif 400 <= status_code < 500:
        print(f"Reminder Failed. Client Error: {status_code}")

    elif 500 <= status_code < 600:
        print(f"Reminder Failed. Server Error: {status_code}")

    else:
        print(f"Unexpected Status Code: {status_code}")


if __name__ == "__main__":
    main()
