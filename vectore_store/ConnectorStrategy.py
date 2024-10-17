from abc import ABC, abstractmethod

class ConnectorStrategy(ABC):
    @abstractmethod
    def getDocs(self):
        pass
    
    @abstractmethod
    def addDoc(self, filename, text_chunks, embedding):
        pass
    
    @abstractmethod
    def retriever(self, query, embedding):
        pass
