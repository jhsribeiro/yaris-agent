from langgraph.graph import StateGraph, END
from src.graph.state import AgentState
from src.graph.nodes import buscar_rag, chamar_llm
from src.graph.edges import roteamento_inicial

def construir_grafo():
    """
    Constrói e compila o grafo do LangGraph, definindo nós, 
    o ponto de entrada condicional e as arestas.
    """
    workflow = StateGraph(AgentState)
    
    # Adicionando os nós
    workflow.add_node("buscar_rag", buscar_rag)
    workflow.add_node("chamar_llm", chamar_llm)
    
    # Configurando o ponto de entrada condicional (Conditional Entry Point)
    workflow.set_conditional_entry_point(
        roteamento_inicial,
        {
            "ir_para_rag": "buscar_rag",
            "direto_llm": "chamar_llm"
        }
    )
    
    # Conectando buscar_rag ao chamar_llm
    workflow.add_edge("buscar_rag", "chamar_llm")
    
    # Conectando chamar_llm ao nó final END
    workflow.add_edge("chamar_llm", END)
    
    # Compilando o grafo
    return workflow.compile()

# Instância do grafo compilado para ser usada na aplicação
app_graph = construir_grafo()


