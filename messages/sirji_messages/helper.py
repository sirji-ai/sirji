from sirji_messages import permissions_dict, AgentEnum, MessageFactory

def generate_allowed_response_template(from_agent, to_agent):
    response_template = ''

    if from_agent != AgentEnum.ORCHESTRATOR:
        response_template += f'Allowed Response Templates TO {to_agent.name}:\n'

    if (from_agent, to_agent) == (AgentEnum.ANY, AgentEnum.ORCHESTRATOR):
        response_template += f'Respond to the {to_agent.name} at the end of task completion. Please respond with the following, including the starting and ending \'***\', with no commentary above or below.'
    if (from_agent, to_agent) == (AgentEnum.ORCHESTRATOR, AgentEnum.ANY):
        response_template += f'To invoke an agent, please respond with the text below, including the starting and ending \'***\', and ensure there is no commentary above or below:'
    else:
        response_template += f'Invoke the {to_agent.name} for the following functions. Please respond with the following, including the starting and ending \'***\', with no commentary above or below.'

    action_list = permissions_dict[(from_agent, to_agent)]

    for index, action in enumerate(action_list):
        message_class = MessageFactory[action.name]
        response_template += f'\n\nFunction {index + 1}. {message_class().description()}\n'
        instructions = message_class().instructions()
        if instructions:
            response_template += '\nInstructions:\n'
            for instruction in instructions:
                response_template += f'- {instruction}\n'
        
        if (from_agent, to_agent) == (AgentEnum.ANY, AgentEnum.ORCHESTRATOR):
            response_template += f'\nResponse template:{message_class().generate({"from_agent_id": "{{Installed Agent ID}}", "to_agent_id": AgentEnum.ORCHESTRATOR.name, "summary": "Empty", "body": "{{Task update. Whether the task was done successfully or not. Any other details which you might think are necessary for ORCHESTRATOR to know of.}"})}'
        else:
            response_template += f'\nResponse template:{message_class().sample()}'

    return response_template