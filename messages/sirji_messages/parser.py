from .custom_exceptions import MessageParsingError, MessageValidationError
from .action_enum import ActionEnum

message_properties = ['FROM', 'TO', 'ACTION','STEP', 'SUMMARY', 'BODY']

def parse(input_message):
    input_message = _discard_format_deviations(input_message)
    lines = _validate_message(input_message)
    parsed_message = _parse_message("\n".join(lines))
    parsed_message['BODY'] = parsed_message['BODY'].lstrip("\n")
    # Check if the message has all the required properties.
    for prop in message_properties:
        if prop not in parsed_message:
            raise MessageParsingError(f"Message does not contain {prop} property")
           
    if parsed_message['ACTION'] not in ActionEnum.__members__:
        raise MessageValidationError(f"Action {parsed_message['ACTION']} is not recognized")

    return parsed_message

def _discard_format_deviations(input_message):
    input_message = input_message.strip()

    # Locate the positions of the first and last "***" in the message.
    start_index = input_message.find("***")
    end_index = input_message.rfind("***")

    # Extract the message prefix, message, and message suffix.
    message_prefix = input_message[:start_index].strip()
    # Including "***" as part of the message content.
    message_content = input_message[start_index:end_index+3].strip()
    message_suffix = input_message[end_index+3:].strip()

    print(message_content)

    return message_content

def _validate_message(message):
    message = message.strip()
    if not (message.startswith("***") and message.endswith("***")):
        raise MessageValidationError("Message must start and end with ***")
    message = message[3:-3].strip()
    lines = message.split("\n")
    if len(lines) < 6:
        raise MessageValidationError(
            "Message does not meet the minimum length requirement")
    return lines


def _parse_message(raw_message):
    parsed_message_dict = {}
    last_key = None
    for line in raw_message.split("\n"):
        if ":" in line:
            key, value = [part.strip() for part in line.split(":", 1)]
            if key in message_properties:
                if key not in parsed_message_dict:
                    parsed_message_dict[key] = value
                else:
                    parsed_message_dict[key] += "\n" + value
                last_key = key
            elif last_key:
                parsed_message_dict[last_key] += "\n" + line
        elif last_key:
            parsed_message_dict[last_key] += "\n" + line
    return parsed_message_dict