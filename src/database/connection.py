import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from src.config import VECTOR_DB_DIR, EMBEDDING_MODEL, EMBEDDING_PROVIDER, OLLAMA_EMBEDDING_MODEL

def get_embedding_function():
    """
    Retorna a função de embeddings configurada conforme a variável EMBEDDING_PROVIDER (google ou ollama).
    """
    if EMBEDDING_PROVIDER.lower() == "google":
        return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    return OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL)

def get_vectorstore():
    """
    Inicializa e retorna a conexão com o banco vetorial ChromaDB.
    Usa persist_directory para salvar os dados localmente.
    """
    embedding_function = get_embedding_function()
    vectorstore = Chroma(
        collection_name="alura_agent_yara",
        embedding_function=embedding_function,
        persist_directory=VECTOR_DB_DIR
    )
    return vectorstore

def get_retriever(k=4, sector=None):
    """
    Retorna o retriever configurado para buscar os top k documentos mais relevantes,
    permitindo filtragem por setor corporativo se especificado.
    """
    vectorstore = get_vectorstore()
    search_kwargs = {"k": k}
    if sector and sector != "Todos os Setores":
        search_kwargs["filter"] = {"sector": sector}
    return vectorstore.as_retriever(search_kwargs=search_kwargs)
