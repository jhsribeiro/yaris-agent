import pytest
from src.graph.prompts import (
    SYSTEM_PROMPT,
    EMPTY_CONTEXT_PROMPT,
    REWRITE_PROMPT,
    DOCUMENT_GRADER_PROMPT,
    COMPLIANCE_CHECK_PROMPT
)

def test_system_prompt_business_rules():
    # Verifica regras do nome YARIS
    assert "YARIS" in SYSTEM_PROMPT
    assert "YARIS" in EMPTY_CONTEXT_PROMPT
    
    # Verifica proibição estrita de emojis
    assert "NUNCA utilize nenhum tipo de emoji" in SYSTEM_PROMPT
    assert "NUNCA utilize nenhum tipo de emoji" in EMPTY_CONTEXT_PROMPT
    
    # Verifica regra inegociável da proibição de "sustentabilidade" para a Yara
    assert "responsabilidade ambiental e social" in SYSTEM_PROMPT
    assert "NUNCA deve usar a palavra \"sustentabilidade\"" in SYSTEM_PROMPT
    assert "responsabilidade ambiental e social" in EMPTY_CONTEXT_PROMPT

def test_compliance_check_prompt_rules():
    assert "SEM EMOJIS" in COMPLIANCE_CHECK_PROMPT
    assert "REGRA DE SUSTENTABILIDADE" in COMPLIANCE_CHECK_PROMPT
    assert "NOME DO AGENTE" in COMPLIANCE_CHECK_PROMPT
