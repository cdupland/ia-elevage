from .ModelStrategy import ModelStrategy

from langchain_community.chat_models import ChatOpenAI
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama

class MistralModel(ModelStrategy):
    def get_model(self, model_name):
        return ChatMistralAI(model=model_name)
    

class OpenAIModel(ModelStrategy):
    def get_model(self, model_name):
        return ChatOpenAI(model=model_name)


class AnthropicModel(ModelStrategy):
    def get_model(self, model_name):
        return ChatAnthropic(model=model_name)


class OllamaModel(ModelStrategy):
    def get_model(self, model_name):
        return ChatOllama(model=model_name)

class ModelManager():
    def __init__(self):
        self.models = {
            "mistral": MistralModel(),
            "openai": OpenAIModel(),
            "anthropic": AnthropicModel(),
            "ollama": OllamaModel()
        }

    def get_model(self, provider, model_name):
        return self.models[provider].get_model(model_name)