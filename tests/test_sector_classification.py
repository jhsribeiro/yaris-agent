import pytest
from scripts.pipeline_ingestao import get_sector_from_filename

def test_juridico_contratos_classification():
    assert get_sector_from_filename("POL-006_Juridico_Contratos_e_NDAs.md") == "Jurídico & Contratos"
    assert get_sector_from_filename("16_juridico_contratos.md") == "Jurídico & Contratos"
    assert get_sector_from_filename("minuta_contrato_fornecedor.pdf") == "Jurídico & Contratos"

def test_compliance_lgpd_classification():
    assert get_sector_from_filename("POL-004_Politica_de_Compliance_LGPD_e_Anticorrupcao.md") == "Compliance & LGPD"
    assert get_sector_from_filename("1_politica_de_privacidade.md") == "Compliance & LGPD"
    assert get_sector_from_filename("5_termos_uso.pdf") == "Compliance & LGPD"

def test_rh_classification():
    assert get_sector_from_filename("POL-003_Direitos_Trabalhistas_e_Conduta.md") == "Recursos Humanos"
    assert get_sector_from_filename("POL-005_Politica_de_Beneficios_e_Banco_de_Horas.md") == "Recursos Humanos"
    assert get_sector_from_filename("GUI-001_Onboarding_Novos_Colaboradores.md") == "Recursos Humanos"
    assert get_sector_from_filename("GUI-002_Diretorio_Contatos_Ramais_Emails.md") == "Recursos Humanos"

def test_financeiro_classification():
    assert get_sector_from_filename("SOP-002_Operacao_Caixa_e_Emissao_NF_Omie.md") == "Financeiro"
    assert get_sector_from_filename("13_financeiro_relatorio.pdf") == "Financeiro"

def test_sac_classification():
    assert get_sector_from_filename("GUI-003_Atendimento_SAC_e_Ouvidoria.md") == "Atendimento ao Cliente (SAC)"
    assert get_sector_from_filename("14_atendimento_sac.md") == "Atendimento ao Cliente (SAC)"

def test_ti_classification():
    assert get_sector_from_filename("FAQ-002_Duvidas_Operacionais_e_Sistemas.md") == "TI & Chamados"
    assert get_sector_from_filename("FAQ-003_Chamados_TI_SLAs_e_Suprimentos_Loja.md") == "TI & Chamados"

def test_comercial_classification():
    assert get_sector_from_filename("POL-007_Alcadas_Comerciais_e_Comissoes.md") == "Comercial & Vendas"
    assert get_sector_from_filename("FAQ-001_Duvidas_Frequentes_Vendas_e_Produtos.md") == "Comercial & Vendas"

def test_facilities_classification():
    assert get_sector_from_filename("SOP-005_Solicitacao_de_Materiais_de_Escritorio_e_Papelaria.md") == "Facilities & Suprimentos"

def test_loja_conceito_classification():
    assert get_sector_from_filename("SOP-001_Atendimento_e_Venda_Presencial.md") == "Loja Conceito"
    assert get_sector_from_filename("SOP-007_Suprimentos_e_Sacolas_Loja_Conceito.md") == "Loja Conceito"

def test_operacoes_logistica_classification():
    assert get_sector_from_filename("SOP-003_Logistica_Reversa_e_Trocas.md") == "Operações & Logística"
    assert get_sector_from_filename("SOP-004_Gestao_Estoque_e_Contingencia_Atelie_Almada.md") == "Operações & Logística"
    assert get_sector_from_filename("SOP-006_Rastreamento_de_Pecas_e_Fornecedores_Florent.md") == "Operações & Logística"

def test_politicas_internas_fallback():
    assert get_sector_from_filename("POL-000_Missao_Visao_Valores_Yara.md") == "Políticas Internas"
    assert get_sector_from_filename("POL-001_Politica_de_Moda_Sustentavel_e_Fornecedores.md") == "Políticas Internas"
    assert get_sector_from_filename("POL-002_Gestao_Social_e_Impacto_Comunitario.md") == "Políticas Internas"
    assert get_sector_from_filename("POL-008_Politicas_Internas_e_Reembolso.md") == "Políticas Internas"
    assert get_sector_from_filename("documento_desconhecido.md") == "Políticas Internas"
