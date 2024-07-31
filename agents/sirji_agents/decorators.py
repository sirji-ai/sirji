import os
import time
import json
import uuid
from datetime import datetime
import requests
import httpx
import openai
import anthropic

def retry_on_exception(max_retries=5, retry_delays=[5, 30], subsequent_retry_delay=300, logger=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            instance_logger = logger or (args[0].logger if hasattr(args[0], 'logger') else None)
            retry_n = 0

            # Helper function to get run path
            def _get_run_path():
                run_path = os.environ.get("SIRJI_RUN_PATH")
                if run_path is None:
                    raise ValueError("SIRJI_RUN_PATH is not set as an environment variable")
                return run_path

            # Helper function to create a notification JSON file
            def create_notification_file(exception, func_name, retry_attempt, retry_delay):
                run_path = _get_run_path()
                async_messages_folder = os.path.join(run_path, "async_messages")
                os.makedirs(async_messages_folder, exist_ok=True)

                notification = {
                    "metadata": {
                        "id": str(uuid.uuid4()),
                        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "type": "notification"
                    },
                    "content": {
                        "title": f"Task Failed on Retry {retry_attempt}",
                        "message": f"A network error occurred. Please check your network connection. Retrying in {retry_delay} seconds (attempt {retry_attempt} of {max_retries})."
                    },
                    "source": {
                        "script": func.__code__.co_filename,
                        "function": func_name
                    }
                }
                
                notification_file_path = os.path.join(async_messages_folder, f"notification_{notification['metadata']['timestamp']}.json")
                with open(notification_file_path, "w") as notification_file:
                    json.dump(notification, notification_file, indent=4)

            while retry_n < max_retries:
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.RequestException,
                        requests.exceptions.Timeout,
                        requests.exceptions.ConnectionError,
                        httpx.RequestError,
                        httpx.ConnectError,
                        openai.APIConnectionError,
                        anthropic.APIConnectionError) as e:

                    retry_delay = retry_delays[retry_n] if retry_n < len(retry_delays) else subsequent_retry_delay

                    error_message = f"Network error occurred: {e}. Retrying in {retry_delay} seconds (attempt {retry_n + 1}/{max_retries})"

                    if instance_logger:
                        instance_logger.error(error_message)

                    print(error_message)

                    # Create notification for each retry attempt
                    create_notification_file(e, func.__name__, retry_n + 1, retry_delay)

                    time.sleep(retry_delay)
                    retry_n += 1

            # Final notification if all retries fail
            create_notification_file(e, func.__name__, retry_n + 1, 0)
            final_error_message = f"Failed to call function {func.__name__} after {max_retries} attempts"
            if instance_logger:
                instance_logger.error(final_error_message)
            raise Exception(final_error_message)

        return wrapper

    return decorator