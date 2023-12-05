from abc import ABC, abstractmethod
from typing import List, AsyncIterable
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """
    Dataclass for chat message
    """
    role: str
    content: str


class FunctionParameterDefinition(BaseModel):
    """
    Dataclass for function parameter definition
    """
    name: str
    type: str
    description: str
    required: bool


class FunctionDefinition(BaseModel):
    """
    Dataclass for function definition
    """
    name: str
    description: str
    parameters: List[FunctionParameterDefinition]


class ChatReply(BaseModel):
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
    async def complete(self,
            messages: List[ChatMessage],
            functions: List[FunctionDefinition]=None,
            temperature=0,
            max_tokens=400,
            frequency_penalty=0,
            presence_penalty=0,
            stream=False
        ) -> AsyncIterable[ChatReply]:
        pass
