import pytest
from sirji_messages import AgentEnum
from sirji_messages.system_prompts.factory import AgentSystemPromptFactory

# Here we're importing the specific system prompt classes for comparison
from sirji_messages.system_prompts.agents.coder import CoderSystemPrompt
from sirji_messages.system_prompts.agents.planner import PlannerSystemPrompt
from sirji_messages.system_prompts.agents.user import UserSystemPrompt
from sirji_messages.system_prompts.agents.executor import ExecutorSystemPrompt
from sirji_messages.system_prompts.agents.researcher import ResearcherSystemPrompt

# Test Cases for AgentSystemPromptFactory


def test_system_prompt_factory_coder():
    assert isinstance(AgentSystemPromptFactory[AgentEnum.CODER.name](
    ), CoderSystemPrompt), "Incorrect system prompt for CODER"


def test_system_prompt_factory_planner():
    assert isinstance(AgentSystemPromptFactory[AgentEnum.PLANNER.name](
    ), PlannerSystemPrompt), "Incorrect system prompt for PLANNER"


def test_system_prompt_factory_user():
    # Noting here that User might not invoke prompts, but testing for completeness
    assert isinstance(AgentSystemPromptFactory[AgentEnum.USER.name](
    ), UserSystemPrompt), "Incorrect system prompt for USER"


def test_system_prompt_factory_executor():
    assert isinstance(AgentSystemPromptFactory[AgentEnum.EXECUTOR.name](
    ), ExecutorSystemPrompt), "Incorrect system prompt for EXECUTOR"


def test_system_prompt_factory_researcher():
    assert isinstance(AgentSystemPromptFactory[AgentEnum.RESEARCHER.name](
    ), ResearcherSystemPrompt), "Incorrect system prompt for RESEARCHER"

# Optionally, you could test for the expected outputs or properties of each class, ensuring integration
# between the system prompts and their respective agent roles perform correctly.
