import pytest
from src.graph.build import app_graph, construir_grafo

def test_construir_grafo_compilation():
    graph = construir_grafo()
    assert graph is not None
    # Garante que o grafo compilado possui os nós configurados
    nodes = list(graph.nodes.keys())
    assert "buscar_rag" in nodes
    assert "chamar_llm" in nodes

def test_app_graph_instance():
    assert app_graph is not None
