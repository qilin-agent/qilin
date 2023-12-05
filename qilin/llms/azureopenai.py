from qilin.llms.llmabc import LLMChatCompletion, ChatReply, FunctionDefinition, ChatMessage
from typing import AsyncIterable, List


def get_openai_function_definition(function: FunctionDefinition):
    parameters = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    for parameter in function.parameters:
        parameters["properties"][parameter.name] = {
            "type": parameter.type,
            "description": parameter.description,
        }
        if parameter.required:
            parameters["required"].append(parameter.name)
    return {
        "name": function.name,
        "description": function.description,
        "parameters": parameters
    }


def get_openai_reply(choices, is_delta=False):
    if is_delta:
        return ChatReply(
            role=choices[0].delta.role,
            content=choices[0].delta.content,
            function=choices[0].delta.function_call.name if choices[0].delta.function_call is not None else None,
            arguments=choices[0].delta.function_call.arguments if choices[0].delta.function_call is not None else None,
            finish_reason=choices[0].finish_reason
        )
    else:
        return ChatReply(
            role=choices[0].message.role,
            content=choices[0].message.content,
            function=choices[0].message.function_call.name if choices[0].message.function_call is not None else None,
            arguments=choices[0].message.function_call.arguments if choices[0].message.function_call is not None else None,
            finish_reason=choices[0].finish_reason
        )


class AzureOpenAIChatCompletion(LLMChatCompletion):
    """
    Azure OpenAI chat completion
    """
    def __init__(self, azure_endpoint, model, api_version, api_key):
        self.model = model
        from openai import AsyncAzureOpenAI
        self.client = AsyncAzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_version=api_version,
            api_key=api_key
        )

    async def complete(self,
            messages: List[ChatMessage],
            functions: List[FunctionDefinition]=None,
            temperature=0,
            max_tokens=400,
            frequency_penalty=0,
            presence_penalty=0,
            stream=False
        ) -> AsyncIterable[ChatReply]:
        params = {
            "model": self.model,
            "messages": [message.model_dump() for message in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stream": stream
        }
        if functions is not None and len(functions) > 0:
            params['functions'] = [get_openai_function_definition(function) for function in functions]
            params['function_call'] = 'auto'
        completion = await self.client.chat.completions.create(**params)
        if stream:
            async for chunk in completion:
                if chunk.choices is None or len(chunk.choices) == 0:
                    continue
                yield get_openai_reply(chunk.choices, is_delta=True)
                if chunk.choices[0].finish_reason is not None:
                    break
        if not stream:
            yield get_openai_reply(completion.choices, is_delta=False)
