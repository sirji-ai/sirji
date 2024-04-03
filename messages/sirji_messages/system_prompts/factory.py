from sirji_messages import AgentEnum

# Import all the agent system prompt classes
from .agents.coder import CoderSystemPrompt
from .agents.planner import PlannerSystemPrompt
from .agents.researcher import ResearcherSystemPrompt
from .agents.executor import ExecutorSystemPrompt
from .agents.user import UserSystemPrompt


class MetaAgentSystemPromptFactory(type):
    def __getitem__(cls, agent):
        try:
            agent_enum = AgentEnum[agent]
            return cls._agent_system_prompt_map[agent_enum]
        except KeyError as e:
            raise AttributeError(
                f"{agent} not found in AgentSystemPromptFactory or Agent Enum.") from e

# Use the metaclass for our factory


class AgentSystemPromptFactory(metaclass=MetaAgentSystemPromptFactory):

    # Map ActionTypes to their respective message classes
    _agent_system_prompt_map = {
        AgentEnum.CODER: CoderSystemPrompt,
        AgentEnum.PLANNER: PlannerSystemPrompt,
        AgentEnum.RESEARCHER: ResearcherSystemPrompt,
        AgentEnum.EXECUTOR: ExecutorSystemPrompt,
        AgentEnum.USER: UserSystemPrompt
    }
