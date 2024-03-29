from parser_factory import ParserFactory

def validate_message(message):
    # Check if the input message starts and ends with ```
    if not message.startswith("```") or not message.endswith("```"):
        return "Invalid message"
    
    # Remove the ``` from the start and end
    message = message.strip("```").strip()

    # Split the message into lines
    lines = message.split("\n")

    # Check if there are at least 4 lines
    if len(lines) < 4:
        return "Invalid message"
    
    return lines

class MessageParser:
    @staticmethod
    def parse(input_message):

        lines = validate_message(input_message)

        # Extract FROM, TO, and ACTION from the first 3 lines
        from_user = lines[0].split(":")[1].strip()
        to_user = lines[1].split(":")[1].strip()
        action = lines[2].split(":")[1].strip()

        # Check if any of FROM, TO, or ACTION is missing
        if not from_user or not to_user or not action:
            return "Invalid message"

        # Get the rest of the lines as the payload
        payload = "\n".join(lines[3:])

        available_properties = ParserFactory.get_parser(action).properties()

        payload = payload.split("\n")

        payload_dict = {}
        last_key = None

        for line in payload:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value

                if key in available_properties:
                    payload_dict[key] = value
                    last_key = key
                elif last_key:
                    payload_dict[last_key] += "\n" + line
            elif last_key:
                payload_dict[last_key] += "\n" + line
        input_text_obj = {
            "FROM": from_user,
            "TO": to_user,
            "ACTION": action,
        }
        # Merge the payload_dict with input_text_obj

        output = {**input_text_obj, **payload_dict}

        return output
            
    @staticmethod
    def parse_steps(message):
        parsed_message = MessageParser.parse(message)

        if parsed_message.get("ACTION") == "steps":
            details = parsed_message.get("DETAILS")
            
            # Initialize an empty array to store the parsed steps
            parsed_steps = []

            # Split the details into lines
            steps_lines = details.strip().split("\n")

            # Initialize variables to store current step details
            current_step_number = None
            current_step_description = ""

            # Iterate over each line to parse the steps
            for line in steps_lines:
                # Check if the line starts with "Step" followed by a number
                if line.strip().startswith("Step"):
                    # If it's a new step, add the previous step to the parsed_steps list
                    if current_step_number is not None:
                        parsed_steps.append(current_step_description.strip())
                    
                    # Extract the step number and description from the line
                    step_parts = line.split(":", 1)
                    current_step_number = step_parts[0].strip()
                    current_step_description = step_parts[1].strip()
                else:
                    # If the line doesn't start with "Step", it's part of the current step's description
                    # Append it to the current step description
                    current_step_description += "\n" + line.strip()

            # Add the last step to the parsed_steps list
            if current_step_number is not None:
                parsed_steps.append(current_step_description.strip())
            
            return parsed_steps
        else:
            return "Invalid message"