from sirji_messages import AgentEnum
from sirji_tools.logger import c_logger as logger

from .base import LLMAgentBase


class CodingAgent(LLMAgentBase):
    def __init__(self):
        super().__init__(AgentEnum.CODER, logger)
