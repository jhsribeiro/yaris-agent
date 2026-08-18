import pytest
from src.graph.edges import roteamento_inicial

def test_roteamento_saudacoes():
    saudacoes = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "tudo bem", "tudo bem?"]
    for s in saudacoes:
        state = {"question": s}
        assert roteamento_inicial(state) == "direto_llm"

def test_roteamento_saudacoes_com_espacos():
    state = {"question": "  Olá  "}
    assert roteamento_inicial(state) == "direto_llm"

def test_roteamento_consulta_rag():
    perguntas_rag = [
        "Como funciona a solicitação de reembolso?",
        "Qual o procedimento para reset de senha no Omie?",
        "Quais são os prazos de análise jurídica de contratos?",
        "Como consultar o rastreamento de peças do fornecedor Florent?"
    ]
    for p in perguntas_rag:
        state = {"question": p}
        assert roteamento_inicial(state) == "ir_para_rag"
