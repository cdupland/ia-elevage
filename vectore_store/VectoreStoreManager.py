from vectore_store import ConnectorStrategy


class VectoreStoreManager:
    def __init__(self, strategy: ConnectorStrategy):
        self.strategy = strategy
    
    def getDocs(self):
        return self.strategy.getDocs()
    
    def addDoc(self, filename, text_chunks, embedding):
        self.strategy.addDoc(filename, text_chunks, embedding)
    
    def retriever(self, query, embedding):
        return self.strategy.retriever(query, embedding)
