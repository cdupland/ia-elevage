import os 
from dotenv import load_dotenv

from .ConnectorStrategy import ConnectorStrategy

from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document

import unicodedata
import time

class PineconeConnector(ConnectorStrategy):
    def __init__(self):

        load_dotenv()

        pinecone_api_key = os.environ.get("PINECONE_API_KEY")

        self.index_name = os.environ.get("PINECONE_INDEX_NAME")
        self.namespace = os.environ.get("PINECONE_NAMESPACE")

        print(f"Index name: {self.index_name}")
        print(f"Namespace: {self.namespace}")
        print(f"Pinecone API Key: {pinecone_api_key}")

        pc = Pinecone(api_key=pinecone_api_key)

        existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

        if self.index_name not in existing_indexes:
            pc.create_index(
                name=self.index_name,
                dimension=3072,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
            while not pc.describe_index(self.index_name).status["ready"]:
                time.sleep(1)

        self.index = pc.Index(self.index_name)

    
    def getDocs(self):
        # Simulate getting docs from Pinecone
        print("Fetching documents from Pinecone")
        
        docs_names = []
        for ids in self.index.list(namespace=self.namespace):
            for id in ids:
                name_doc = "_".join(id.split("_")[:-1])
                if name_doc not in docs_names:
                    docs_names.append(name_doc)

        return docs_names
    
    
    def addDoc(self, filename, text_chunks, embedding):
        try:
            vector_store = PineconeVectorStore(index=self.index, embedding=embedding,namespace=self.namespace)

            file_name = filename.split(".")[0].replace(" ","_").replace("-","_").replace(".","_").replace("/","_").replace("\\","_").strip()

            documents = []
            uuids = []

            print(file_name)

            for i, chunk in enumerate(text_chunks):
                clean_filename = remove_non_standard_ascii(file_name)
                uuid = f"{clean_filename}_{i}"
                
                print(f"Adding document with ID {uuid}")

                document = Document(
                    page_content=chunk,
                    metadata={ "filename":filename, "chunk_id":uuid },
                )

                uuids.append(uuid)
                documents.append(document)
            

            vector_store.add_documents(documents=documents, ids=uuids)

            return {"filename_id":clean_filename}
        
        except Exception as e:
            print(e)
            return False
    
    def retriever(self, query, embedding):

        print(f"Retrieving documents from Pinecone for query '{query}'")

        vector_store = PineconeVectorStore(index=self.index, embedding=embedding,namespace=self.namespace)

        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "score_threshold": 0.6},
        )

        return retriever.invoke(query)
    

def remove_non_standard_ascii(input_string: str) -> str:
    normalized_string = unicodedata.normalize('NFKD', input_string)
    return ''.join(char for char in normalized_string if 'a' <= char <= 'z' or 'A' <= char <= 'Z' or char.isdigit() or char in ' .,!?')

