from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Iterable


@dataclass
class ChatMessage:
    """
    Dataclass for chat message
    """
    role: str
    content: str


@dataclass
class FunctionParameterDefinition:
    """
    Dataclass for function parameter definition
    """
    name: str
    type: str
    description: str
    required: bool


@dataclass
class FunctionDefinition:
    """
    Dataclass for function definition
    """
    name: str
    description: str
    parameters: List[FunctionParameterDefinition]


@dataclass
class ChatReply:
    """
    Dataclass for chat reply
    """
    role: str
    content: str
    function: str
    arguments: str
    finish_reason: str


class LLMChatCompletion(ABC):
    """
    Abstract class for chat completion
    """
    @abstractmethod
    def complete(self,
        messages: List[ChatMessage],
        functions: List[FunctionDefinition]=None,
        temperature=0,
        max_tokens=400,
        frequency_penalty=0,
        presence_penalty=0,
        stream=False) -> Iterable[ChatMessage]:
        pass

