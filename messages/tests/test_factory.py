from sirji_messages.messages.factory import MessageFactory
from sirji_messages.action_enum import ActionEnum
from sirji_messages.messages.actions.execute_command import ExecuteCommandMessage
from sirji_messages.messages.actions.run_server import RunServerMessage
from sirji_messages.messages.actions.create_project_file import CreateProjectFileMessage
import pytest

def test_message_factory_getitem():
    assert MessageFactory[ActionEnum.EXECUTE_COMMAND.name] == ExecuteCommandMessage
    assert MessageFactory[ActionEnum.RUN_SERVER.name] == RunServerMessage
    assert MessageFactory[ActionEnum.CREATE_PROJECT_FILE.name] == CreateProjectFileMessage
    
def test_message_factory_invalid_action():
    with pytest.raises(AttributeError) as exc_info:
        MessageFactory["INVALID_ACTION"]
    assert str(exc_info.value) == "INVALID_ACTION not found in MessageFactory or ActionType Enum."