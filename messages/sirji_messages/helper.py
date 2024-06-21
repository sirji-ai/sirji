from sirji_messages import permissions_dict, AgentEnum, MessageFactory

def allowed_response_templates(from_agent, to_agent, action_list):
    response_template = ''

    if from_agent != AgentEnum.ORCHESTRATOR and from_agent != AgentEnum.CALLER:
        if to_agent == AgentEnum.CALLER:
            response_template += f'Allowed Response Templates TO agent who invoked you:\n'
        else:
            response_template += f'Allowed Response Templates TO {to_agent.name}:\n'

    if (from_agent, to_agent) == (AgentEnum.ANY, AgentEnum.CALLER):
        response_template += f'Respond to the agent which invoked you, at the end of task completion. Please respond with the following, including the starting and ending \'***\', with no commentary above or below.'
    elif (from_agent, to_agent) == (AgentEnum.ORCHESTRATOR, AgentEnum.ANY):
        response_template += f'To invoke an agent, please respond with the text below, including the starting and ending \'***\', and ensure there is no commentary above or below:'
    else:
        response_template += f'Invoke the {to_agent.name} for the following functions. Please respond with the following, including the starting and ending \'***\', with no commentary above or below.'

    for index, action in enumerate(action_list):
        message_class = MessageFactory[action.name]
        response_template += f'\n\nFunction {index + 1}. {message_class().description()}\n'
        instructions = message_class().instructions()
        if instructions:
            response_template += '\nInstructions:\n'
            for instruction in instructions:
                response_template += f'- {instruction}\n'
        
        if (from_agent, to_agent) == (AgentEnum.ANY, AgentEnum.CALLER):
            print('Inside if statement')
            response_template += f'\nResponse template:{message_class().generate({"from_agent_id": "{{Your Agent ID}}", "to_agent_id": "{{Agent ID of the invoker agent}}","step": "Provide the steps if any", "summary": "Empty", "body": "{{Task update. Whether the task was done successfully or not. Any other details which you might think are necessary for the agent which invoked you to know of.}}"})}'
        else:
            response_template += f'\nResponse template:{message_class().sample()}'

    return response_template