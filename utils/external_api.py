import json
import requests

def send_webhook(submission: dict, message: str = "Code executed"):
    """
    Sends a POST request to the submission's webhook URL with result data.
    """
    webhook_url = submission.get("webhook")

    if not webhook_url:
        print(f"⚠️ No webhook configured for submission {submission.get('id') or submission.get('token')}")
        return

    payload = {
        "message": message,
        "result": {
            "token":submission.get("token"),
            "stdout":submission.get("stdout"),
            "stderr":submission.get("stderr")
        }
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        print(f"📡 Webhook sent ({response.status_code}) -> {webhook_url}")

        if response.status_code >= 400:
            print(f"⚠️ Webhook responded with error: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send webhook to {webhook_url}: {e}")
