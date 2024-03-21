from abc import ABC, abstractmethod

class BaseMessages(ABC):

  def __init__(self, implementor):
    self.implementor = implementor

  @abstractmethod
  def template(self):
    """
    Message template.
    """
    pass

  @abstractmethod
  def sample(self, interactor):
    """
    Sample message using the message template.

    Parameters:
    interactor (str): The interactor represents the entity interacting with the message template. 
    """
    pass
  
  @abstractmethod
  def description(self):
    """
    Description of the message.
    """
    pass

  @abstractmethod 
  def properties(self):
    """
    List of available properties of the message.
    """
    pass
  
  def generate(self, interactor, obj):
    obj["implementor"] = self.implementor
    obj["interactor"] = interactor
    return self.template().format(**obj)