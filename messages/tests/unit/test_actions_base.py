import pytest
from sirji_messages.messages.actions.base import BaseMessages

# Creating a concrete class by inheriting from BaseMessages for testing purposes


class ConcreteMessage(BaseMessages):
    def template_payload_part(self):
        return "Payload part"

    def sample(self):
        return "Sample message"

    def description(self):
        return "Description"

    def custom_properties(self):
        return ['DETAILS']


def test_base_messages_instantiation():
    concrete_message = ConcreteMessage()
    assert isinstance(concrete_message, BaseMessages)


def test_base_messages_methods():
    concrete_message = ConcreteMessage()
    assert concrete_message.template_payload_part() == "Payload part"
    assert concrete_message.sample() == "Sample message"
    assert concrete_message.description() == "Description"
    assert concrete_message.custom_properties() == ['DETAILS']
