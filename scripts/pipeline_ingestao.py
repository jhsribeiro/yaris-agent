import os
import sys
import time

# Garante que a raiz do projeto esteja no sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_dir)

from tqdm.auto import tqdm
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from src.database.connection import get_vectorstore

def get_sector_from_filename(filename: str) -> str:
    """
    Classifica o setor corporativo do documento com base na identificação dos arquivos da pasta docs/ e legados.
    Mapeia exatamente com as opções de filtros da interface (SETORES_CHIPS).
    """
    fn = os.path.basename(filename).lower()
    
    # 1. Jurídico & Contratos (Análise de contratos, minutas, NDAs)
    if any(k in fn for k in ["pol-006", "16_juridico", "contrat", "juridico"]):
        return "Jurídico & Contratos"
        
    # 2. Compliance & LGPD (Política anticorrupção, proteção de dados, termos)
    elif any(k in fn for k in ["pol-004", "compliance", "lgpd", "anticorrupcao", "1_politica_de_privacidade", "5_termos"]):
        return "Compliance & LGPD"
        
    # 3. Recursos Humanos (Onboarding, Direitos CLT, Benefícios, Banco de Horas, Contatos)
    elif any(k in fn for k in ["pol-003", "pol-005", "gui-001", "gui-002", "11_contatos", "6_manual_de_rh", "onboarding", "banco_de_horas"]):
        return "Recursos Humanos"
        
    # 4. Financeiro & Faturamento (Operação de caixa Omie, emissão NF, contas)
    elif any(k in fn for k in ["sop-002", "13_financeiro", "caixa_e_emissao_nf"]):
        return "Financeiro"
        
    # 5. Atendimento ao Cliente / SAC (SAC, Ouvidoria, prazos de atendimento)
    elif any(k in fn for k in ["gui-003", "14_atendimento", "sac_"]):
        return "Atendimento ao Cliente (SAC)"
        
    # 6. TI & Chamados (Portal de chamados, SLAs, reset de senha, infraesturura)
    elif any(k in fn for k in ["faq-002", "faq-003", "12_ti_chamados", "sistemas"]):
        return "TI & Chamados"
        
    # 7. Comercial & Vendas (FAQ Vendas, Alçadas de desconto, Comissões B2B/Varejo)
    elif any(k in fn for k in ["pol-007", "faq-001", "15_comercial", "comissoes"]):
        return "Comercial & Vendas"
        
    # 8. Facilities & Suprimentos (Papelaria ecológica, insumos de escritório, almoxarifado)
    elif any(k in fn for k in ["sop-005", "facilities", "papelaria"]):
        return "Facilities & Suprimentos"
        
    # 9. Loja Conceito (Atendimento presencial Iguatemi, sacolas biodegradáveis, balcão)
    elif any(k in fn for k in ["sop-001", "sop-007", "venda_presencial", "loja_conceito", "sacolas"]):
        return "Loja Conceito"
        
    # 10. Operações & Logística (Logística reversa, contingência Ateliê Almada, estoque, fretes, Florent)
    elif any(k in fn for k in ["sop-003", "sop-004", "sop-006", "logistica", "estoque", "florent", "rastreamento", "inbound"]):
        return "Operações & Logística"
        
    # 11. Políticas Internas (Moda sustentável, gestão social, reembolso, conduta)
    elif any(k in fn for k in ["pol-001", "pol-002", "pol-008", "10_politica_interna"]):
        return "Políticas Internas"
        
    # Fallback Padrão
    else:
        return "Políticas Internas"

def executar_ingestao():
    """
    Executa o pipeline de ingestão de documentos (PDFs e MDs) no ChromaDB com metadados de setor.
    Aplica tratamento resiliente de cota (429) com pausa de 61s e retentativas infinitas por lote.
    """
    print("Iniciando o pipeline de ingestão de dados...")
    
    docs_dir = os.path.join(root_dir, "docs")
    target_dirs = [docs_dir]
    documentos = []
    
    for ddir in target_dirs:
        if os.path.exists(ddir):
            print(f"Lendo documentos da pasta '{ddir}'...")
            loader_md = DirectoryLoader(ddir, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}, show_progress=True)
            loader_pdf = DirectoryLoader(ddir, glob="**/*.pdf", loader_cls=PyPDFLoader, show_progress=True)
            documentos.extend(loader_md.load())
            documentos.extend(loader_pdf.load())
    
    if not documentos:
        print("Nenhum documento encontrado para ingestão.")
        return
        
    print(f"Encontrados {len(documentos)} documentos. Dividindo em chunks e inserindo metadados de setor...")
    
    # Injeta o setor nos metadados de cada documento original antes do split
    for doc in documentos:
        source_path = doc.metadata.get("source", "")
        doc.metadata["sector"] = get_sector_from_filename(source_path)

    # Dividindo em chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(documentos)
    
    print(f"Gerados {len(chunks)} chunks de texto. Inserindo no ChromaDB...")
    
    # Inserindo no Banco Vetorial (Limpando coleção existente para evitar duplicidade)
    vectorstore = get_vectorstore()
    try:
        vectorstore.delete_collection()
        print("Banco vetorial anterior limpo com sucesso.")
        vectorstore = get_vectorstore()
    except Exception as e:
        print("Inicializando banco vetorial limpo...")
        
    batch_size = 20
    print(f"Total de chunks a serem processados: {len(chunks)}")
    print(f"Processando em lotes de {batch_size} chunks no ChromaDB...")
    
    for i in tqdm(range(0, len(chunks), batch_size)):
        batch = chunks[i:i + batch_size]
        
        while True:
            try:
                vectorstore.add_documents(batch)
                break
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
                    print(f"\nAVISO: Limite de cota atingido (Erro 429). Aguardando 61 segundos para reiniciar...")
                    time.sleep(61)
                    print("Tentando processar o mesmo lote novamente...")
                else:
                    raise e
    
    print("\n--- Vector Store criado com sucesso! ---")

if __name__ == "__main__":
    executar_ingestao()
