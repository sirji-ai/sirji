from sirji_messages import permissions_dict, AgentEnum, MessageFactory

def generate_allowed_response_template(agent_type):
    agent_label = {
        AgentEnum.EXECUTOR: 'EXECUTOR',
        AgentEnum.SIRJI_USER: 'SIRJI USER',
        AgentEnum.ORCHESTRATOR: 'ORCHESTRATOR'
    }.get(agent_type, 'UNKNOWN')

    response_template = f'Allowed Response Templates TO {agent_label}:\n'
    
    if agent_type == AgentEnum.ORCHESTRATOR:
        response_template += f'Respond to the {agent_label} at the end of task completion. Please respond with the following, including the starting and ending \'***\', with no commentary above or below.'
    else:
        response_template += f'Invoke the {agent_label} for the following functions. Please respond with the following, including the starting and ending \'***\', with no commentary above or below.'

    action_list = permissions_dict[(AgentEnum.ANY, agent_type)]

    for index, action in enumerate(action_list):
        message_class = MessageFactory[action.name]
        response_template += f'\n\nFunction {index + 1}. {message_class().description()}\n'
        instructions = message_class().instructions()
        if instructions:
            response_template += '\nInstructions:\n'
            for instruction in instructions:
                response_template += f'- {instruction}\n'
        
        if agent_type == AgentEnum.ORCHESTRATOR:
            response_template += f'\nResponse template:{message_class().generate({"from_agent_id": "{{Installed Agent ID}}", "to_agent_id": AgentEnum.ORCHESTRATOR.name, "summary": "Empty", "body": "{{Task update. Whether the task was done successfully or not. Any other details which you might think are necessary for ORCHESTRATOR to know of.}"})}'
        else:
            response_template += f'\nResponse template:{message_class().sample()}'

    return response_template
