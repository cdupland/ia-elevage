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
#add new import
from langchain_community.document_loaders.csv_loader import CSVLoader

from prompt_template import base_template


# load .env in local dev
load_dotenv()
env_api_key = os.environ.get("MISTRAL_API_KEY")
llm_model = "open-mixtral-8x7b"

class Rag:
    document_vector_store = None
    retriever = None
    chain = None

    def __init__(self, vectore_store=None):
        
        self.model = ChatMistralAI(model=llm_model)
        self.embedding = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=env_api_key)

        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100, length_function=len)
        self.prompt = PromptTemplate.from_template(base_template)

        self.vector_store = vectore_store

    def setModel(self, model):
        self.model = model

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

        document_vector_store = FAISS.from_documents(chunks, self.embedding)
        
        self.retriever = document_vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.5,
            },
        )

    def ask(self, query: str, messages: list):
        
        self.chain = self.prompt | self.model | StrOutputParser()
        
        print("messages ", messages)

        # Retrieve the context document
        if self.retriever is None:
            documentContext = ''
        else:
            documentContext = self.retriever.invoke(query)

        # Retrieve the VectoreStore
        contextCommon = self.vector_store.retriever(query, self.embedding)

        return self.chain.invoke({
            "query": query,
            "documentContext": documentContext,
            "commonContext": contextCommon,
            "messages": messages
        })

    def clear(self):
        self.document_vector_store = None
        self.vector_store = None
        self.retriever = None
        self.chain = None