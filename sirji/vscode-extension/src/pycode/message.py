import sys
import json
from sirji_messages import message_parse, MessageFactory,AgentSystemPromptFactory, ActionEnum, AgentEnum, validate_permission

def generate_problem_statement_message(problem_statement):
    message = MessageFactory[ActionEnum.PROBLEM_STATEMENT.name]()
    return message.generate({"details": problem_statement})

def generate_coder_system_prompt():
    prompt_class = AgentSystemPromptFactory[AgentEnum.CODER.name]
    return prompt_class().system_prompt()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python message.p '{\"function\":\"function_name\", \"args\":{...}'")
        sys.exit(1)
        
    json_arg = sys.argv[1]
        
    try:
        parsed_json = json.loads(json_arg)

        if not parsed_json.get("function"):
            print("Function name not provided.")
            sys.exit(1)
          
        if parsed_json.get("function") == "generate_problem_statement_message":
            response = generate_problem_statement_message(**parsed_json.get("args"))
        elif parsed_json.get("function") == "generate_coder_system_prompt":
            response = generate_coder_system_prompt()
        else:
            print("Function", parsed_json.get("function"), "not found")
            sys.exit(1)

        print(response)

        sys.exit(0)

    except json.JSONDecodeError as e:
        print("Invalid JSON. Please ensure the input is a correct JSON string.")
        print(e)
        sys.exit(1)