from sirji_messages import ActionEnum, AgentEnum

# Defining permissions_dict
# Key: (from_agent, to_agent)
# Value: set of allowed actions between the agents
permissions_dict = {
    (AgentEnum.ANY, AgentEnum.EXECUTOR): {
        ActionEnum.CREATE_WORKSPACE_FILE,
        ActionEnum.CREATE_SHARED_RESOURCE_FILE,
        ActionEnum.EXECUTE_COMMAND,
        ActionEnum.RUN_SERVER,
        ActionEnum.READ_WORKSPACE_FILES,
        ActionEnum.READ_SHARED_RESOURCES_FILES,
        ActionEnum.READ_DIR,
        ActionEnum.READ_DIR_STRUCTURE,
        ActionEnum.APPEND_TO_SHARED_RESOURCES_INDEX,
        ActionEnum.READ_SHARED_RESOURCE_INDEX,
        ActionEnum.FIND_AND_REPLACE,
        ActionEnum.INSERT_TEXT
    },
    (AgentEnum.ANY, AgentEnum.SIRJI_USER): {
        ActionEnum.QUESTION
    },
    (AgentEnum.ANY, AgentEnum.CALLER): {
        ActionEnum.RESPONSE
    },
    (AgentEnum.ORCHESTRATOR, AgentEnum.SIRJI_USER): {
        ActionEnum.SOLUTION_COMPLETE
    },
    (AgentEnum.ORCHESTRATOR, AgentEnum.ANY): {
        ActionEnum.INVOKE_AGENT
    },
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
