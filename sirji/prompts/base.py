from abc import ABC, abstractmethod


class PromptGeneratorBase(ABC):

    def __init__(self, caller_name, caller_short_name):
        self.caller_name = caller_name
        self.caller_short_name = caller_short_name

    def system_prompt(self):
        system_prompt = ""
        system_prompt += f"{self.intro_prompt()}\n"
        system_prompt += "Your job is to:"
        system_prompt += f"{self.responsibilities_prompt()}\n"
        system_prompt += f"{self.caller_agent_interaction_message_prompt()}\n"
        system_prompt += f"{self.can_interact_with_other_agents_prompt()}"
        system_prompt += f"{self.other_agents_capability_prompt()}"
        system_prompt += f"{self.other_agents_interaction_message_prompt()}"
        system_prompt += f"{self.ending_prompt()}"

        return system_prompt

    @abstractmethod
    def name(self):
        """
        Agent name.
        """
        pass

    @abstractmethod
    def short_name(self):
        """
        Agent short name.
        """
        pass

    @abstractmethod
    def intro_prompt(self):
        """
        Agent intro for the system prompt.
        """
        pass

    @abstractmethod
    def responsibilities_prompt(self):
        """
        Agent responsibilities for the system prompt.
        """
        pass

    @abstractmethod
    def capabilities_prompt(self):
        """
        Agent capabilities for the system prompt.
        """
        pass

    @abstractmethod
    def interact_with(self):
        """
        List of agent class instances that this agent can interact with.
        """
        pass

    @abstractmethod
    def incoming_message_instances(self):
        """
        List of incoming message class instances that this agent can receive.
        """
        pass

    @abstractmethod
    def outgoing_message_instances(self):
        """
        List of outgoing message class instances that this agent can send.
        """
        pass

    @abstractmethod
    def ending_prompt(self):
        """
        Agent ending message for the system prompt.
        """
        pass

    def can_interact_with_other_agents_prompt(self):
        can_interact_with_prompt = ""

        if self.interact_with():
            can_interact_with_prompt += f"You can interact with:\n"

            for instance in self.interact_with():
                can_interact_with_prompt += f"- {instance.name()} ({instance.short_name()}).\n"

            can_interact_with_prompt += "\n"

        return can_interact_with_prompt

    def other_agents_capability_prompt(self):
        interact_with_prompt = ""

        for instance in self.interact_with():
            interact_with_prompt += f"{instance.short_name()} can:\n"
            interact_with_prompt += f"{instance.capabilities_prompt()}\n\n"

        return interact_with_prompt

    def other_agents_interaction_message_prompt(self):
        interaction_message_prompt = ""
        if self.interact_with():
            interaction_message_prompt += "Allowed message formats are described below. Ensure you don't give additional details/explanations/comments in the message outside of ``` delimiter. Ensure to be concise with your messages."
            for instance in self.interact_with():
                interaction_message_prompt += f"The allowed messages that you can send to {instance.short_name()} are:\n\n"
                incoming_message_display_count = 1
                incoming_message_instances = instance.incoming_message_instances()
                for message_instance in incoming_message_instances:
                    interaction_message_prompt += f"{incoming_message_display_count}. {message_instance.description()}\n"
                    interaction_message_prompt += f"{message_instance.sample(self.short_name())}\n"
                    incoming_message_display_count += 1
                interaction_message_prompt += f"The allowed messages from {instance.short_name()} to you are:\n\n"
                outgoing_message_display_count = 1
                outgoing_message_instances = instance.outgoing_message_instances()
                for message_instance in outgoing_message_instances:
                    interaction_message_prompt += f"{outgoing_message_display_count}. {message_instance.description()}\n"
                    interaction_message_prompt += f"{message_instance.sample(self.short_name())}\n"
                    outgoing_message_display_count += 1
        return interaction_message_prompt

    def caller_agent_interaction_message_prompt(self):
        interaction_message_prompt = ""
        if self.incoming_message_instances() or self.outgoing_message_instances():
            interaction_message_prompt += "Allowed message formats are described below. Ensure you don't give additional details/explanations/comments in the message outside of ``` delimiter. Ensure to be concise with your messages.\n\n"
            interaction_message_prompt += f"The allowed messages from {self.caller_short_name} to you are:\n\n"
            incoming_message_display_count = 1
            incoming_message_instances = self.incoming_message_instances()
            for message_instance in incoming_message_instances:
                interaction_message_prompt += f"{incoming_message_display_count}. {message_instance.description()}\n"
                interaction_message_prompt += f"{message_instance.sample(self.caller_short_name)}\n"
                incoming_message_display_count += 1
            interaction_message_prompt += f"The allowed messages that you can send to {self.caller_short_name} are:\n\n"
            outgoing_message_display_count = 1
            outgoing_message_instances = self.outgoing_message_instances()
            for message_instance in outgoing_message_instances:
                interaction_message_prompt += f"{outgoing_message_display_count}. {message_instance.description()}\n"
                interaction_message_prompt += f"{message_instance.sample(self.caller_short_name)}\n"
                outgoing_message_display_count += 1
        return interaction_message_prompt
