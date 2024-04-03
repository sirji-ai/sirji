from abc import ABC, abstractmethod

from sirji_messages import MessageFactory, ActionEnum


class AgentSystemPromptBase(ABC):

    def system_prompt(self):
        system_prompt = ""
        system_prompt += f"{self.intro()}\n"

        system_prompt += "Your job is to:"
        system_prompt += f"{self.responsibilities()}\n"

        system_prompt += f"{self.can_interact_with()}"

        system_prompt += f"{self.other_agents_capabilities()}"

        system_prompt += f"{self.interactions()}"

        system_prompt += f"{self.ending_prompt()}"

        # print(system_prompt)

        return system_prompt

    @abstractmethod
    def short_name(self):
        """
        Agent short name - taken from correct agent enum.
        """
        pass

    @abstractmethod
    def intro(self):
        """
        Agent intro.
        """
        pass

    @abstractmethod
    def responsibilities(self):
        """
        Agent responsibilities.
        """
        pass

    @abstractmethod
    def capabilities(self):
        """
        Agent capabilties.
        """
        pass

    @abstractmethod
    def ending_prompt(self):
        """
        Agent ending message for the system prompt.
        """
        pass

    def can_interact_with(self):
        can_interact_with_message = ""

        other_agents = self.get_other_agents()

        if not other_agents:
            return can_interact_with_message

        can_interact_with_message += f"You can interact with:\n"
        for agent_enum in other_agents:
            can_interact_with_message += f"- {agent_enum.full_name} ({agent_enum.name}).\n"

        can_interact_with_message += "\n"

        return can_interact_with_message

    def other_agents_capabilities(self):
        other_agents_capabilities_message = ""

        other_agents = self.get_other_agents()

        if not other_agents:
            return other_agents_capabilities_message

        for agent_enum in other_agents:
            other_agents_capabilities_message += f"{agent_enum.name} can:"

            from sirji_messages.system_prompts.factory import AgentSystemPromptFactory

            other_agents_capabilities_message += f"{AgentSystemPromptFactory[agent_enum.name]().capabilities()}\n\n"

        return other_agents_capabilities_message

    def interactions(self):
        interactions_message = "Allowed responses and their formats are described below.\n\n"

        # We create a helper function to reduce redundancy
        def append_action_messages(actions, heading):
            action_message = heading

            # Check if 'actions' is a single ActionEnum object and not an iterable (list, set, etc.)
            if isinstance(actions, ActionEnum):
                actions = [actions]  # Convert it into a list

            for count, action_enum in enumerate(actions, start=1):
                message_obj = MessageFactory[action_enum.name]()
                action_message += f"{count}. {message_obj.description()}\n{message_obj.sample()}\n"

            return action_message

        from sirji_messages import permissions_dict

        # Iterating through each key-value pair in the permissions_dict
        for agents, actions in permissions_dict.items():
            from_agent, to_agent = agents  # Unpacking the key which is a tuple of two agents

            # Dynamically determining which messages to append based on the agent's role
            if self.short_name() == from_agent.name:
                heading = f"The allowed responses that you can send to the {to_agent.name} are:\n\n"
                interactions_message += append_action_messages(
                    actions, heading)
            elif self.short_name() == to_agent.name:
                heading = f"The allowed responses from the {from_agent.name} to you are:\n\n"
                interactions_message += append_action_messages(
                    actions, heading)

        return interactions_message

    def get_other_agents(self):
        other_agents = set()
        from sirji_messages import permissions_dict
        for agents, _ in permissions_dict.items():
            from_agent, to_agent = agents  # Unpacking the key which is a tuple of two agents

            if self.short_name() == from_agent.name:
                other_agents.add(to_agent)
            elif self.short_name() == to_agent.name:
                other_agents.add(from_agent)

        return other_agents
