from enum import Enum


class AgentEnum(Enum):
    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member.full_name = name
        return member

    CODER = (1, "Coding Agent")
    PLANNER = (2, "Planning Agent")
    EXECUTOR = (3, "Execution Agent")
    RESEARCHER = (4, "Research Agent")
    USER = (5, "End User")
