from typing import TypedDict, List, Optional
from langchain_core.documents import Document

class AgentState(TypedDict, total=False):
    """
    Define o estado que será passado entre os nós do grafo do LangGraph.
    """
    question: str
    context: List[Document]
    response: str
    sector: Optional[str]
    llm_provider: Optional[str]
    llm_model: Optional[str]



