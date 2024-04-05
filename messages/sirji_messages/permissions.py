from sirji_messages import ActionEnum, AgentEnum

# Defining permissions_dict
# Key: (from_agent, to_agent)
# Value: set of allowed actions between the agents
permissions_dict = {
    (AgentEnum.CODER, AgentEnum.EXECUTOR): {
        ActionEnum.CREATE_FILE,
        ActionEnum.EXECUTE_COMMAND,
        ActionEnum.INSTALL_PACKAGE,
        ActionEnum.READ_FILE,
        ActionEnum.READ_DIR
    },
    (AgentEnum.CODER, AgentEnum.PLANNER): (
        ActionEnum.GENERATE_STEPS
    ),
    (AgentEnum.CODER, AgentEnum.RESEARCHER): (
        ActionEnum.TRAIN_USING_URL,
        ActionEnum.INFER
    ),
    (AgentEnum.CODER, AgentEnum.USER): (
        ActionEnum.QUESTION,
        ActionEnum.INFORM,
        ActionEnum.STEP_STARTED,
        ActionEnum.STEP_COMPLETED,
        ActionEnum.SOLUTION_COMPLETE
    ),
    (AgentEnum.EXECUTOR, AgentEnum.CODER): (
        ActionEnum.OUTPUT
    ),
    (AgentEnum.PLANNER, AgentEnum.CODER): (
        ActionEnum.STEPS
    ),
    (AgentEnum.RESEARCHER, AgentEnum.CODER): (
        ActionEnum.RESPONSE,
        ActionEnum.TRAINING_OUTPUT
    ),
    (AgentEnum.USER, AgentEnum.CODER): (
        ActionEnum.PROBLEM_STATEMENT,
        ActionEnum.ANSWER,
        ActionEnum.ACKNOWLEDGE,
        ActionEnum.FEEDBACK
    )
}


def validate_permission(from_str, to_str, action_str):
    try:
        # Convert the string representations to corresponding enum values
        from_agent = AgentEnum[from_str]
        to_agent = AgentEnum[to_str]
        action = ActionEnum[action_str]

        # Check if the (from_agent, to_agent) pair is in the permissions_dict
        if (from_agent, to_agent) in permissions_dict:
            # Get the allowed actions for the given agent pair
            allowed_actions = permissions_dict[(from_agent, to_agent)]

            # If allowed_actions is directly an ActionEnum (not iterable), wrap it in a set
            if isinstance(allowed_actions, ActionEnum):
                allowed_actions = {allowed_actions}
            # If it's a tuple or another iterable
            elif not isinstance(allowed_actions, set):
                allowed_actions = set(allowed_actions)

            return action in allowed_actions
        else:
            # The agent pair does not have any permissions_dict defined
            return False
    except KeyError:
        # The provided string values do not match any enum
        return False
