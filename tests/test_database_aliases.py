import pytest
from src.database.connection import SECTOR_ALIASES

EXPECTED_SECTORS = [
    "Jurídico & Contratos",
    "Compliance & LGPD",
    "Recursos Humanos",
    "Financeiro",
    "TI & Chamados",
    "Atendimento ao Cliente (SAC)",
    "Comercial & Vendas",
    "Facilities & Suprimentos",
    "Loja Conceito",
    "Operações & Logística",
    "Políticas Internas"
]

def test_sector_aliases_coverage():
    for sector in EXPECTED_SECTORS:
        assert sector in SECTOR_ALIASES
        aliases = SECTOR_ALIASES[sector]
        assert isinstance(aliases, list)
        assert len(aliases) >= 1
        assert sector in aliases

def test_sector_aliases_reciprocal_relationships():
    # Garantir que Jurídico & Contratos inclui Compliance & LGPD e vice-versa
    assert "Compliance & LGPD" in SECTOR_ALIASES["Jurídico & Contratos"]
    assert "Jurídico & Contratos" in SECTOR_ALIASES["Compliance & LGPD"]
    
    # Garantir que TI & Chamados inclui Facilities & Suprimentos e Loja Conceito
    assert "Facilities & Suprimentos" in SECTOR_ALIASES["TI & Chamados"]
    assert "Loja Conceito" in SECTOR_ALIASES["TI & Chamados"]
