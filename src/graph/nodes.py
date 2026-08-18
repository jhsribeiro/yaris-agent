from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from src.database.connection import get_retriever
from src.graph.prompts import SYSTEM_PROMPT, EMPTY_CONTEXT_PROMPT
from src.config import LLM_PROVIDER, LLM_MODEL, OLLAMA_LLM_MODEL, OLLAMA_BASE_URL
from src.graph.state import AgentState

def get_llm(provider: Optional[str] = None, model: Optional[str] = None):
    """
    Instancia dinamicamente o provedor de LLM com base na configuração em src/config.py (.env)
    ou parâmetro informado.
    """
    prov = (provider or LLM_PROVIDER).lower()
    
    if prov == "ollama":
        target_model = model or OLLAMA_LLM_MODEL
        return ChatOllama(
            model=target_model,
            base_url=OLLAMA_BASE_URL,
            temperature=0.2
        )
    else:
        target_model = model or LLM_MODEL
        return ChatGoogleGenerativeAI(
            model=target_model,
            temperature=0.2,
            max_retries=5
        )

def buscar_rag(state: AgentState):
    """
    Nó responsável por buscar o contexto no ChromaDB usando RAG.
    """
    question = state["question"]
    sector = state.get("sector")
    retriever = get_retriever(k=4, sector=sector)
    documentos = retriever.invoke(question)
    
    return {"context": documentos}

def chamar_llm(state: AgentState):
    """
    Nó responsável por chamar a LLM (Gemini ou Ollama) formatando o prompt com o contexto recuperado e a pergunta.
    Aplica as configurações definidas em src/config.py / .env e trata erros de limite de cota (429) e conexão do Ollama.
    """
    question = state["question"]
    context_docs = state.get("context", [])
    provider = state.get("llm_provider") or LLM_PROVIDER
    model = state.get("llm_model") or (OLLAMA_LLM_MODEL if provider == "ollama" else LLM_MODEL)
    
    if not context_docs:
        prompt_formatado = EMPTY_CONTEXT_PROMPT.format(question=question)
    else:
        context_text = "\n\n".join([doc.page_content for doc in context_docs])
        prompt_formatado = SYSTEM_PROMPT.format(context=context_text, question=question)
        
    try:
        llm = get_llm(provider=provider, model=model)
        resposta = llm.invoke(prompt_formatado)
        content = _format_response_content(resposta.content)
        return {"response": content}
    except Exception as e:
        err_msg = str(e).lower()
        if "429" in err_msg or "resource_exhausted" in err_msg or "quota" in err_msg:
            return {
                "response": "**Limite de Requisições da API Atingido Temporariamente (Erro 429)**\n\n"
                            "A cota de requisições por minuto da API do Gemini foi atingida devido às consultas recentes.\n\n"
                            "**Como resolver:** Aguarde cerca de 15 a 30 segundos e envie sua pergunta novamente."
            }
        elif "not found" in err_msg or "404" in err_msg:
            modelo_tentado = model or (OLLAMA_LLM_MODEL if provider == "ollama" else LLM_MODEL)
            if provider == "ollama":
                return {
                    "response": f"**Modelo do Ollama Não Instalado**\n\n"
                                f"O serviço local do Ollama está em execução, mas o modelo `{modelo_tentado}` não foi encontrado.\n\n"
                                "**Como resolver:**\n"
                                f"1. Abra seu terminal e instale/baixe o modelo executando: `ollama run {modelo_tentado}`\n"
                                "2. Ou configure o modelo no arquivo `src/config.py` ou `.env`."
                }
            else:
                return {
                    "response": f"**Modelo do Gemini Não Encontrado (Erro 404)**\n\n"
                                f"O modelo `{modelo_tentado}` não existe na API do Google Gemini.\n\n"
                                "**Como resolver:**\n"
                                "Altere o modelo no arquivo `.env` ou `src/config.py` para um modelo válido como `gemini-1.5-flash` ou `gemini-2.0-flash`."
                }
        elif "connection" in err_msg or "refused" in err_msg or "11434" in err_msg or "connecterror" in err_msg:
            modelo_tentado = model or OLLAMA_LLM_MODEL
            return {
                "response": f"**Erro de Conexão com o Ollama Local**\n\n"
                            f"Não foi possível conectar ao serviço local do Ollama (`{OLLAMA_BASE_URL}`).\n\n"
                            "**Como resolver:**\n"
                            "1. Verifique se o serviço do Ollama está rodando em segundo plano na sua máquina.\n"
                            f"2. Garanta que baixou o modelo executando no terminal: `ollama run {modelo_tentado}`\n"
                            "3. Ou altere `LLM_PROVIDER=gemini` no arquivo `.env` ou `src/config.py`."
            }
        else:
            return {"response": f"Ocorreu um erro temporário ao comunicar com o modelo de IA: {e}"}

def _format_response_content(content) -> str:
    if isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                text_parts.append(item["text"])
            elif isinstance(item, str):
                text_parts.append(str(item))
            else:
                text_parts.append(str(item))
        return "\n".join(text_parts)
    elif not isinstance(content, str):
        return str(content)
    return content
