from .messages.factory import MessageFactory
from .custom_exceptions import MessageParsingError, MessageValidationError
from .action_enum import ActionEnum
from sirji_messages import validate_permission


def parse(input_message):
    lines = _validate_message(input_message)
    message_info = _extract_message_info(lines)
    payload = "\n".join(lines[3:])
    custom_properties = MessageFactory[message_info["ACTION"]].custom_properties()

    payload_dict = _parse_payload(payload, custom_properties)

    parsed_message = {"FROM": message_info["FROM"], "TO": message_info["TO"],
                      "ACTION": message_info["ACTION"], **payload_dict}

    if parsed_message.get("ACTION") == ActionEnum.STEPS.name:
        parsed_message = {
            **parsed_message, "PARSED_STEPS": _parse_steps(parsed_message)}

    return parsed_message


def _validate_message(message):
    message = message.strip()
    if not (message.startswith("```") and message.endswith("```")):
        raise MessageValidationError("Message must start and end with ```")
    message = message[3:-3].strip()
    lines = message.split("\n")
    if len(lines) < 4:
        raise MessageValidationError(
            "Message does not meet the minimum length requirement")
    return lines


def _extract_message_info(lines):
    try:
        message_info = {line.split(":", 1)[0].strip(): line.split(":", 1)[
            1].strip() for line in lines[:3]}
    except (IndexError, ValueError):
        raise MessageParsingError(
            "Message metadata (FROM, TO, ACTION) is improperly formed")

    from_str = message_info.get("FROM")
    to_str = message_info.get("TO")
    action_str = message_info.get("ACTION")

    if not all([from_str, to_str, action_str]):
        raise MessageValidationError(
            "FROM, TO, and ACTION fields are required")
    if not validate_permission(from_str, to_str, action_str):
        raise MessageValidationError(
            f"{from_str} is not allowed to send {action_str} action to {to_str}")

    return message_info


def _parse_payload(payload, custom_properties):
    payload_dict = {}
    last_key = None
    for line in payload.split("\n"):
        if ":" in line:
            key, value = [part.strip() for part in line.split(":", 1)]
            if key in custom_properties:
                payload_dict[key] = value
                last_key = key
            elif last_key:
                payload_dict[last_key] += "\n" + line
        elif last_key:
            payload_dict[last_key] += "\n" + line
    return payload_dict


def _parse_steps(parsed_message):
    details = parsed_message.get("DETAILS", "")
    parsed_steps = []
    
    if any(line.strip().startswith("Step") for line in details.split("\n")): 
        current_step_number = None
        current_step_description = ""
        for line in details.split("\n"):
            line = line.strip() 
            if line.startswith("Step"):
                if current_step_number is not None:
                    parsed_steps.append(
                        {"step": current_step_number.strip(), "description": current_step_description.strip()})
                current_step_number, current_step_description = [part.strip() for part in line.split(":", 1)]
            else:
                current_step_description += f"\n{line}"
        if current_step_number is not None:
            parsed_steps.append({"step": current_step_number.strip(),
                                "description": current_step_description.strip()})
    else:
        step_number = 1
        for line in details.split("\n"):
            line = line.strip()
            if line:  
                parsed_steps.append({"step": f"Step {step_number}", "description": line})
                step_number += 1

    return parsed_steps