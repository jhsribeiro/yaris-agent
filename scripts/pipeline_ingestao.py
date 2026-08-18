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
    """
    fn = os.path.basename(filename).lower()
    
    # 1. Recursos Humanos (Onboarding, Direitos CLT, Benefícios, Banco de Horas, Contatos)
    if any(k in fn for k in ["pol-003", "pol-005", "gui-001", "gui-002", "11_contatos", "6_manual_de_rh", "onboarding", "banco_de_horas"]):
        return "Recursos Humanos"
        
    # 2. Compliance, LGPD & Integridade (Política anticorrupção, proteção de dados, termos)
    elif any(k in fn for k in ["pol-004", "compliance", "lgpd", "anticorrupcao", "16_juridico", "1_politica_de_privacidade", "5_termos"]):
        return "Compliance & LGPD"
        
    # 3. Financeiro & Faturamento (Operação de caixa Omie, emissão NF, reembolso)
    elif any(k in fn for k in ["sop-002", "13_financeiro", "2_politica_de_reembolso", "caixa_e_emissao_nf"]):
        return "Financeiro"
        
    # 4. Atendimento ao Cliente / SAC (Atendimento presencial Iguatemi, FAQ vendas)
    elif any(k in fn for k in ["sop-001", "faq-001", "14_atendimento", "venda_presencial"]):
        return "Atendimento ao Cliente (SAC)"
        
    # 5. TI, Sistemas & Suporte (FAQ operacionais Omie/Impressora/Pix, chamados TI)
    elif any(k in fn for k in ["faq-002", "12_ti_chamados", "10_politica_interna", "sistemas"]):
        return "TI & Chamados"
        
    # 6. Comercial, Marketing & Produtos (Moda sustentável, fornecedores, posicionamento)
    elif any(k in fn for k in ["pol-001", "15_comercial", "moda_sustentavel", "marketing"]):
        return "Comercial & Vendas"
        
    # 7. Gestão Social & Impacto Comunitário (Doações Estrutural/Ceilândia, transparência)
    elif any(k in fn for k in ["pol-002", "gestao_social", "impacto_comunitario"]):
        return "Gestão Social & Impacto"
        
    # 8. Facilities, Suprimentos & Almoxarifado (Papelaria ecológica, insumos de escritório)
    elif any(k in fn for k in ["sop-005", "facilities", "papelaria"]):
        return "Facilities & Suprimentos"
        
    # 9. Operações, Logística & Estoque (Logística reversa, contingência Ateliê Almada, estoque)
    elif any(k in fn for k in ["sop-003", "sop-004", "logistica_reversa", "gestao_estoque"]):
        return "Operações & Logística"
        
    # Fallback Padrão
    else:
        return "Operações & Logística"

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
