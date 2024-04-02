import sys

from sirji_messages import AgentSystemPromptFactory, AgentEnum

def generate_coder_system_prompt():
    # TODO: Return a JSON object of all system prompts
    prompt_class = AgentSystemPromptFactory[AgentEnum.CODER.name]
    return prompt_class().system_prompt()

if __name__ == "__main__":
    response = generate_coder_system_prompt()

    print(response)

    sys.exit(0)