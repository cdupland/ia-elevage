from abc import ABC, abstractmethod

class ModelStrategy(ABC):
    @abstractmethod
    def get_model(self, model_name):
        pass
