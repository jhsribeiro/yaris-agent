import pytest
from src.graph.nodes import _format_response_content

def test_format_response_content_string():
    assert _format_response_content("Olá, mundo") == "Olá, mundo"

def test_format_response_content_list_strings():
    input_list = ["Linha 1", "Linha 2"]
    assert _format_response_content(input_list) == "Linha 1\nLinha 2"

def test_format_response_content_list_dicts():
    input_list = [{"text": "Parte 1"}, {"text": "Parte 2"}]
    assert _format_response_content(input_list) == "Parte 1\nParte 2"

def test_format_response_content_non_string():
    assert _format_response_content(12345) == "12345"
