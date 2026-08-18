from src.graph.state import AgentState

def roteamento_inicial(state: AgentState) -> str:
    """
    Verifica a pergunta inicial e roteia o fluxo.
    Se for uma saudação curta, vai direto para a LLM, ignorando a busca (RAG).
    Caso contrário, direciona para o pipeline RAG.
    """
    question = state["question"].strip().lower()
    
    # Lista de saudações curtas
    saudacoes = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "tudo bem", "tudo bem?"]
    
    # Verifica se a pergunta é uma saudação curta exata ou muito próxima
    if question in saudacoes:
        return "direto_llm"
    
    return "ir_para_rag"


