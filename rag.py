import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_community.document_loaders.csv_loader import CSVLoader

from util import getYamlConfig


# load .env in local dev
load_dotenv()
env_api_key = os.environ.get("MISTRAL_API_KEY")

class Rag:
    document_vector_store = None
    retriever = None
    chain = None
    readableModelName = ""
    all_documents = []  # Attribut pour stocker les documents injectés

    def __init__(self, vectore_store=None):
        
        # self.model = ChatMistralAI(model=llm_model)
        self.embedding = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=env_api_key)

        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100, length_function=len)
        
        base_template = getYamlConfig()['prompt_template']
        self.prompt = PromptTemplate.from_template(base_template)

        self.vector_store = vectore_store

    def setModel(self, model, readableModelName = ""):
        self.model = model
        self.readableModelName = readableModelName

    def getReadableModel(self):
        return self.readableModelName
    
    def ingestToDb(self, file_path: str, filename: str):

        docs = PyPDFLoader(file_path=file_path).load()

        # Extract all text from the document
        text = ""
        for page in docs:
            text += page.page_content

        # Split the text into chunks
        chunks = self.text_splitter.split_text(text)
        
        return self.vector_store.addDoc(filename=filename, text_chunks=chunks, embedding=self.embedding)

    def getDbFiles(self):
        return self.vector_store.getDocs()

    def ingest(self, pdf_file_path: str):
        docs = PyPDFLoader(file_path=pdf_file_path).load()
       
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)

        if self.document_vector_store is None:
            self.document_vector_store = FAISS.from_documents(chunks, self.embedding)
        else:
            self.document_vector_store.add_documents(chunks)

        # Ajout des documents dans la liste `all_documents`
        self.all_documents.extend(chunks)
        
        self.retriever = self.document_vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.5,
            },
        )


    def list_documents(self):
        """Retourne tous les documents injectés."""
        return [doc for doc in self.all_documents]


    def ask(self, query: str, prompt_system: str, messages: list, variables: list = None):
        self.chain = self.prompt | self.model | StrOutputParser()
        
        # Retrieve the context document
        if self.retriever is None:
            documentContext = ''
        else:
            documentContext = self.retriever.invoke(query)

        # Retrieve the VectoreStore
        contextCommon = self.vector_store.retriever(query, self.embedding)

        # Dictionnaire de base avec les variables principales
        chain_input = {
            "query": query,
            "documentContext": documentContext,
            "commonContext": contextCommon,
            "prompt_system": prompt_system,
            "messages": messages
        }

        # Suppression des valeurs nulles (facultatif)
        chain_input = {k: v for k, v in chain_input.items() if v is not None}

        # Si des variables sous forme de liste sont fournies
        if variables:
            # Convertir la liste en dictionnaire avec 'key' comme clé et 'value' comme valeur
            extra_vars = {item['key']: item['value'] for item in variables if 'key' in item and 'value' in item}
            
            # Fusionner avec chain_input
            chain_input.update(extra_vars)
        

        return self.chain.stream(chain_input)

    def clear(self):
        self.document_vector_store = None
        self.vector_store = None
        self.retriever = None
        self.chain = None