from sirji_messages import AgentEnum
from sirji_tools.logger import p_logger as logger

from .base import LLMAgentBase


class PlanningAgent(LLMAgentBase):
    def __init__(self):
        super().__init__(AgentEnum.PLANNER, logger)
