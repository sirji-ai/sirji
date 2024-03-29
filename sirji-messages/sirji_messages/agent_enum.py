from enum import Enum


class AgentEnum(Enum):
    def __new__(cls, value, name, short_name):
        member = object.__new__(cls)
        member._value_ = value
        member.full_name = name
        member.short_name = short_name
        return member

    CODER = (1, "Coding Agent", "Coder")
    PLANNER = (2, "Planning Agent", "Planner")
    EXECUTOR = (3, "Execution Agent", "Executor")
    RESEARCHER = (4, "Research Agent", "Researcher")
    USER = (5, "End User", "User")
