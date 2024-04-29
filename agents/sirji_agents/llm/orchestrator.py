import textwrap
import os

# TODO - log file should be dynamically created based on agent ID
from sirji_tools.logger import p_logger as logger

from sirji_messages import message_parse, MessageParsingError, MessageValidationError
from .model_providers.factory import LLMProviderFactory

class Orchestrator():
    def __init__(self, recipe, installed_agents):
        
        self.recipe = recipe
        self.installed_agents = installed_agents

    def message(self, input_message, history=[]):
        conversation = self.__prepare_conversation(input_message, history)

        logger.info(f"Incoming: \n{input_message}")
        logger.info("Calling OpenAI Chat Completions API\n")

        response_message, prompt_tokens, completion_tokens = self.__get_response(conversation)

        return response_message, conversation, prompt_tokens, completion_tokens

    def __prepare_conversation(self, input_message, history):
        conversation = []

        logger.info('Hello--------')
        logger.info(history)

        if not history:
            logger.info('Hello---11111-----')
            conversation.append(
                {"role": "system", "content": self.system_prompt()})
        else:
            logger.info('Hello---2222-----')
            conversation = history
            parsed_input_message = message_parse(input_message)
            conversation.append({"role": "user", "content": input_message, "parsed_content": parsed_input_message})

        return conversation

    def __get_response(self, conversation):
        retry_llm_count = 0
        response_message = ''
        prompt_tokens = 0
        completion_tokens = 0

        while(True):
            response_message, current_prompt_tokens, current_completion_tokens = self.__call_llm(conversation)
            
            prompt_tokens += current_prompt_tokens
            completion_tokens += current_completion_tokens
            try:
                # Attempt parsing
                parsed_response_message = message_parse(response_message)
                conversation.append({"role": "assistant", "content": response_message, "parsed_content": parsed_response_message})
                break
            except (MessageParsingError, MessageValidationError) as e:
            # Handling both MessageParsingError and MessageValidationError similarly
                logger.info("Error while parsing the message.\n")
                retry_llm_count += 1
                if retry_llm_count > 2:
                    raise e
                logger.info(f"Requesting LLM to resend the message in correct format.\n")
                conversation.append({"role": "assistant", "content": response_message, "parsed_content": {}})
                conversation.append({"role": "user", "content": "Error obtained in processing your last response. Your response must conform strictly to one of the allowed Response Templates, as it will be processed programmatically and only these templates are recognized. Your response must be enclosed within '***' at the beginning and end, without any additional text above or below these markers. Not conforming above rules will lead to response processing errors."})
            except Exception as e:
                logger.info(f"Generic error while parsing message. Error: {e}\n")
                raise e
            
            
        return response_message, prompt_tokens, completion_tokens
    
    def __call_llm(self, conversation):
        history = []

        for message in conversation:
            history.append({"role": message['role'], "content": message['content']})

        model_provider = LLMProviderFactory.get_instance()

        return model_provider.get_response(history, logger)

    def system_prompt(self):
        initial_intro = textwrap.dedent(f"""
            You are an agent named "Orchestration Agent," a component of the Sirji AI agentic framework.
            Your Agent ID: ORCHESTRATOR
            Your OS (refered as SIRJI_OS later): {os.name}""")

        instructions = textwrap.dedent(f"""
            Instructions:
            - Manage the task workflow by interpreting the "recipe," which outlines a series of prescribed tasks.
            - Identify the most suitable agent (from the available options) for each task based on their skills.
            - Activate the selected agent.
            - Utilize the "tips" provided in the recipe to manage scenarios that require deviation from the prescribed task order.`
            """)

        formatted_recipe = self.__format_recipe()

        # TODO: Vaibhav - Read all the agents from the installed agents folder to come up with the following.
        # Using the file names from installed_agents first populate the variable applicable_agent_ids
        # Then use applicable_agent_ids to create following.
        formatted_installed_agents = textwrap.dedent(f"""
            Agent Name: Product Manager
            Agent ID: PRODUCT_MANAGER
            Skills:
            - Generation of epics and user stories for the problem statement.

            Agent Name: Architect
            Agent ID: ARCHITECT
            Skills:
            - Generation of architecture components.

            Agent Name: Coder
            Agent ID: CODER
            Skills:
            - Develop end-to-end working code for the epic & user stories, making use of the finalized architecture components.""")
        
        # TODO: Vaibhav - The Allowed Response Templates part of the agent system prompt must be created dynamically.
        allowed_response_templates = textwrap.dedent(f"""
            Allowed Response Templates:

            Invoke the SIRJI_USER for the following functions. Please respond with the following, including the starting and ending '***', with no commentary above or below.

            Function 1. Inform About Solution Completed

            Instructions:
            - Empty

            Response template:
            ***
            FROM: {{Your Agent ID}}
            TO: SIRJI_USER
            ACTION: SOLUTION_COMPLETE
            SUMMARY: Empty
            BODY:
            {{Summarize what all was done for gettign the solution.}}
            ***

            To invoke an agent, please respond with the text below, including the starting and ending '***', and ensure there is no commentary above or below:
            ***
            FROM: {{Your Agent ID}}
            TO: {{Installed Agent ID}}
            ACTION: INVOKE_AGENT
            SUMMARY: {{Display a concise summary to the user, describing the action using the present continuous tense.}}
            BODY:
            {{Purpose of invocation}}
            ***""")
        
        return f"{initial_intro}\n{instructions}\n{formatted_recipe}{formatted_installed_agents}\n{allowed_response_templates}".strip()
    def __format_recipe(self):
        formatted = "Recipe:\n"
        # Adding prescribed tasks with enumeration
        formatted += "- Prescribed tasks\n"
        for index, task in enumerate(self.recipe["prescribed_tasks"], start=1):
            formatted += f"   {index}. {task}\n"
        # Adding tips
        formatted += "- Tips:\n"
        for tip in self.recipe["tips"]:
            formatted += f"   - {tip}\n"
        return formatted
