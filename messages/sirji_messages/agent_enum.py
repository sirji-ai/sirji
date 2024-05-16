from enum import Enum


class AgentEnum(Enum):
    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member.full_name = name
        return member

    ORCHESTRATOR = (0, "Orchestrator")
    CODER = (1, "Coding Agent")
    PLANNER = (2, "Planning Agent")
    EXECUTOR = (3, "Execution Agent")
    RESEARCHER = (4, "Research Agent")
    SIRJI_USER = (5, "End User")
    ANY = (6, "Any Agent")
    CALLER = (7, "Caller Agent")
