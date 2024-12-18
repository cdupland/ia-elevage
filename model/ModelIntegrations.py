import os

from .ModelStrategy import ModelStrategy

from langchain_openai import ChatOpenAI
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_anthropic import ChatAnthropic

from llamaapi import LlamaAPI
from langchain_experimental.llms import ChatLlamaAPI

class MistralModel(ModelStrategy):
    def get_model(self, model_name):
        return ChatMistralAI(model=model_name)
    

class OpenAIModel(ModelStrategy):
    def get_model(self, model_name):
        return ChatOpenAI(model=model_name)


class AnthropicModel(ModelStrategy):
    def get_model(self, model_name):
        return ChatAnthropic(model=model_name)


class LlamaAPIModel(ModelStrategy):
    def get_model(self, model_name):
        llama = LlamaAPI(os.environ.get("LLAMA_API_KEY"))
        return ChatLlamaAPI(client=llama, model=model_name)

class ModelManager():
    def __init__(self):
        self.models = {
            "mistral": MistralModel(),
            "openai": OpenAIModel(),
            "anthropic": AnthropicModel(),
            "llama": LlamaAPIModel()
        }

    def get_model(self, provider, model_name):
        return self.models[provider].get_model(model_name)