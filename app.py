import streamlit as st
from src.graph.build import app_graph
from src.config import LLM_PROVIDER, LLM_MODEL, OLLAMA_LLM_MODEL
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="YARIS AI Agent",
    page_icon="🤖",
    layout="wide"
)

# Estilização CSS personalizada para Dark Mode Obsidian Premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, h4, h5, h6, input, button, textarea {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Ocultar elementos nativos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent;}
    
    /* Fundo principal da aplicação */
    .stApp {
        background-color: #0B0F17;
        color: #F8FAFC;
    }

    /* Hero Banner Principal */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F2B48 100%);
        color: #FFFFFF;
        padding: 28px 32px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.5);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::after {
        content: "";
        position: absolute;
        top: -40%;
        right: -10%;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, rgba(0, 0, 0, 0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 10px 0 6px 0;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .hero-title .gradient-text {
        background: linear-gradient(90deg, #FFFFFF 0%, #93C5FD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.02rem;
        color: #94A3B8;
        max-width: 800px;
        line-height: 1.5;
        margin-bottom: 0;
    }

    /* Badges & Pills */
    .badge-pill {
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(96, 165, 250, 0.3);
        color: #60A5FA;
        padding: 6px 14px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .badge-sidebar {
        background-color: rgba(30, 58, 138, 0.5);
        color: #93C5FD;
        border: 1px solid rgba(59, 130, 246, 0.4);
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem;
        display: block;
        margin-top: 10px;
        margin-bottom: 14px;
        text-align: center;
    }

    .badge-sidebar-footer {
        background-color: #1E293B;
        color: #94A3B8;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 10px 14px;
        font-weight: 600;
        font-size: 0.86rem;
        margin-top: 0px;
        margin-bottom: 14px;
        line-height: 1.4;
    }


    .badge-status {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Estilização da Sidebar (Dark Mode) */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }

    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
        color: #F8FAFC !important;
    }

    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #94A3B8;
    }

    /* Estilização Geral dos Botões */
    div.stButton > button {
        background-color: #1E293B !important;
        color: #F1F5F9 !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        min-height: 44px !important;
        height: auto !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        line-height: 1.3 !important;
        width: 100% !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        white-space: normal !important;
    }

    div.stButton > button:hover {
        background-color: #334155 !important;
        border-color: #3B82F6 !important;
        color: #60A5FA !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2) !important;
    }

    /* Seção e Titulo do Filtro Semântico por Botõezinhos */
    .filter-section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .filter-status-indicator {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 10px 14px;
        margin-top: 8px;
        margin-bottom: 10px;
        font-size: 0.86rem;
        font-weight: 600;
        color: #94A3B8;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .active-filter-highlight {
        color: #34D399;
        font-weight: 700;
    }

    /* Cards de Histórico e Fontes */
    .source-card {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-left: 4px solid #3B82F6;
        border-radius: 10px;
        padding: 14px 18px;
        margin-top: 10px;
        font-size: 0.9rem;
        color: #CBD5E1;
        line-height: 1.5;
    }

    .source-card table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 0.88rem;
    }

    .source-card th, .source-card td {
        border: 1px solid #334155;
        padding: 8px 12px;
        text-align: left;
    }

    .source-card th {
        background-color: #1E293B;
        color: #F8FAFC;
        font-weight: 600;
    }

    .source-card tr:nth-child(even) {
        background-color: rgba(255, 255, 255, 0.02);
    }

    .source-tag {
        background-color: #1E3A8A;
        color: #93C5FD;
        border: 1px solid #2563EB;
        padding: 4px 12px;
        border-radius: 6px;
        font-family: monospace;
        font-size: 0.82rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }

    /* Caixas de Chat */
    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 16px;
        border: 1px solid #1E293B;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #1E293B;
    }
    
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #0F172A;
    }

    /* Expander estilizado */
    div[data-testid="stExpander"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        margin-top: 6px !important;
        margin-bottom: 6px !important;
    }

    .streamlit-expanderHeader {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 10px 14px !important;
    }

    /* Custom Input de Chat */
    [data-testid="stChatInput"] {
        border-radius: 16px !important;
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        color: #F8FAFC !important;
        font-size: 0.95rem !important;
    }

</style>
""", unsafe_allow_html=True)

# Lista de Setores Corporativos para o Filtro Semântico por Botõezinhos
SETORES_CHIPS = [
    ("Todos", "Todos os Setores"),
    ("Recursos Humanos", "Recursos Humanos"),
    ("Financeiro", "Financeiro"),
    ("TI & SLAs", "TI & Chamados"),
    ("SAC", "Atendimento ao Cliente (SAC)"),
    ("Comercial", "Comercial & Vendas"),
    ("Compliance", "Compliance & LGPD"),
    ("Jurídico", "Jurídico & Contratos"),
    ("Suprimentos", "Facilities & Suprimentos"),
    ("Loja", "Loja Conceito"),
    ("Logística", "Operações & Logística"),
    ("Políticas", "Políticas Internas")
]

# Inicialização do estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_sector" not in st.session_state:
    st.session_state.active_sector = "Todos os Setores"

# Barra Lateral (Sidebar)
with st.sidebar:
    st.image("assets/logo_yaris.png", width=90)
    st.markdown("<h2 style='color: #F8FAFC; margin-top: 8px;'>YARA Intelligent System</h2>", unsafe_allow_html=True)

    # Botão de Nova Conversa
    if st.button("Nova conversa", use_container_width=True):
        st.session_state.messages = []
        st.session_state.active_sector = "Todos os Setores"
        st.rerun()
        
    st.markdown("---")

    # Indicador de Busca Específica (Filtro Ativo)
    current_sector = st.session_state.active_sector
    if current_sector == "Todos os Setores":
        status_text = "🌐 <b>Busca Global</b> (Todos os setores)"
    else:
        status_text = f"🎯 <b>Busca Específica:</b> <span class='active-filter-highlight'>{current_sector}</span>"
    st.markdown(f'<div class="filter-status-indicator"><span>{status_text}</span></div>', unsafe_allow_html=True)

    # Indicador do Modelo de IA
    if LLM_PROVIDER.lower() == "ollama":
        st.markdown(f"<div class='filter-status-indicator'><span>🦙 <b>Provedor:</b> Ollama (Local)<br><small style='color: #94A3B8;'>Modelo: {OLLAMA_LLM_MODEL}</small></span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='filter-status-indicator'><span>⚡ <b>Provedor:</b> Google Gemini<br><small style='color: #94A3B8;'>Modelo: {LLM_MODEL}</small></span></div>", unsafe_allow_html=True)

    st.markdown("---")

    # Sugestões de Consulta Rápida na Sidebar
    with st.expander("**Sugestões de Consulta Rápida**", expanded=False):
        if st.button("🛡️ Compliance & LGPD", use_container_width=True, key="side_compliance"):
            st.session_state["pending_prompt"] = "Quais são as diretrizes da LGPD para proteção de dados de clientes e as regras anticorrupção na YARA?"
            st.session_state.active_sector = "Compliance & LGPD"
        if st.button("👥 Recursos Humanos", use_container_width=True, key="side_rh"):
            st.session_state["pending_prompt"] = "Quais são as regras do Banco de Horas, prazos de compensação e os benefícios (Plano de Saúde, VR/VA, VT e Desconto) oferecidos pela YARA?"
            st.session_state.active_sector = "Recursos Humanos"
        if st.button("💰 Financeiro & Faturamento", use_container_width=True, key="side_fin"):
            st.session_state["pending_prompt"] = "Como funciona a emissão de nota fiscal, pagamento de fornecedores e prazos no ERP Omie?"
            st.session_state.active_sector = "Financeiro"
        if st.button("🖥️ Chamados de TI & SLAs", use_container_width=True, key="side_ti"):
            st.session_state["pending_prompt"] = "Quais são os canais para abrir um chamado de TI, como faço reset de senha e quais os SLAs de atendimento?"
            st.session_state.active_sector = "TI & Chamados"
        if st.button("🎧 Atendimento ao Cliente", use_container_width=True, key="side_sac"):
            st.session_state["pending_prompt"] = "Quais são os prazos de resposta do SAC, canal de Ouvidoria e regras de atendimento ao cliente?"
            st.session_state.active_sector = "Atendimento ao Cliente (SAC)"
        if st.button("📈 Comercial & Alçadas", use_container_width=True, key="side_com"):
            st.session_state["pending_prompt"] = "Quais são as alçadas de desconto para vendas e a política de comissão para consultores e atacado?"
            st.session_state.active_sector = "Comercial & Vendas"
        if st.button("⚖️ Jurídico & Contratos", use_container_width=True, key="side_jur"):
            st.session_state["pending_prompt"] = "Qual o prazo de análise jurídica de contratos e em quais situações é obrigatória a assinatura de NDA?"
            st.session_state.active_sector = "Jurídico & Contratos"
        if st.button("📦 Facilities & Suprimentos", use_container_width=True, key="side_fac"):
            st.session_state["pending_prompt"] = "Como funciona a solicitação de materiais de escritório e papelaria ecológica via Facilities e qual o prazo de entrega?"
            st.session_state.active_sector = "Facilities & Suprimentos"
        if st.button("🛍️ Suprimentos para a Loja", use_container_width=True, key="side_loja"):
            st.session_state["pending_prompt"] = "Como solicitar novas sacolas biodegradáveis, ecobags e tags para a loja física do Shopping Iguatemi?"
            st.session_state.active_sector = "Loja Conceito"
        if st.button("🚚 Rastreamento de Peças", use_container_width=True, key="side_log"):
            st.session_state["pending_prompt"] = "Como consultar o rastreamento e status de entrega de lotes de peças e tecidos dos fornecedores como a Florent?"
            st.session_state.active_sector = "Operações & Logística"
    
    # Base de Documentos Indexados (Abaixo das Sugestões)
    with st.expander("**Base de Conhecimento Indexada**"):
        st.markdown("""
        - 🛡️ **Compliance & LGPD:** Proteção de Dados, Lei Anticorrupção, Ouvidoria
        - 👥 **Recursos Humanos:** Contatos, Banco de Horas, Benefícios, Plano de Saúde, Folha
        - 💰 **Financeiro:** Faturamento, NF-e, ERP Omie
        - 🎧 **Atendimento:** SAC, Prazos, Ouvidoria
        - 📈 **Comercial:** Alçadas, Comissões
        - ⚖️ **Jurídico:** Minutas, NDAs, LGPD
        - 🖥️ **TI & Suporte:** Reset de Senha, SLAs
        - 📦 **Facilities:** Materiais & Papelaria
        - 🛍️ **Loja Conceito:** Sacolas, Tags, Peças
        - 🚚 **Operações:** Logística & Rastreio
        - 💼 **Políticas:** Reembolso & Garantia
        """)




# Conteúdo Principal - Hero Banner
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">
        <span class="gradient-text">YARIS AI Agent</span>
    </h1>
    <p class="hero-subtitle">
        Seu assistente inteligente de conhecimento corporativo. Consulte instantaneamente manuais, políticas e diretrizes internas da YARA com precisão documental.
    </p>
</div>
""", unsafe_allow_html=True)

# FILTRO SEMÂNTICO POR BOTÕEZINHOS (CHIPS INTERATIVOS)
st.markdown('<div class="filter-section-title"><b>Selecione o Departamento de Busca Específica</b></div>', unsafe_allow_html=True)

# Primeira Linha de Chips (6 colunas)
cols_row1 = st.columns(6)
for idx, (short_label, val) in enumerate(SETORES_CHIPS[:6]):
    is_active = (st.session_state.active_sector == val)
    chip_label = f"🟢 {short_label}" if is_active else short_label
    with cols_row1[idx]:
        if st.button(chip_label, key=f"chip_{idx}", use_container_width=True):
            st.session_state.active_sector = val
            st.rerun()

# Segunda Linha de Chips (6 colunas)
cols_row2 = st.columns(6)
for idx, (short_label, val) in enumerate(SETORES_CHIPS[6:]):
    is_active = (st.session_state.active_sector == val)
    chip_label = f"🟢 {short_label}" if is_active else short_label
    with cols_row2[idx]:
        if st.button(chip_label, key=f"chip_{idx+6}", use_container_width=True):
            st.session_state.active_sector = val
            st.rerun()



# Exibindo histórico no UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg and msg["sources"]:
            with st.expander("📄 Documentos Internos Consultados (Fontes RAG)"):
                for source in msg["sources"]:
                    fonte_nome = source.metadata.get("source", "Documento Interno")
                    st.markdown(f"<span class='source-tag'>📁 {fonte_nome}</span>", unsafe_allow_html=True)
                    st.markdown(f"<div class='source-card'>\n\n{source.page_content}\n\n</div>", unsafe_allow_html=True)

# Capturando input (via sugestão da sidebar ou caixa de chat)
prompt = st.chat_input("Pergunte algo ao YARIS sobre procedimentos internos da YARA...")
if "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    # Registra a pergunta do colaborador
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Processa a resposta via LangGraph RAG com o filtro semântico ativo
    with st.chat_message("assistant"):
        sector_filter_value = None if st.session_state.active_sector == "Todos os Setores" else st.session_state.active_sector
        
        with st.spinner(f"YARIS está consultando a base de conhecimento ({st.session_state.active_sector})..."):
            resultado = app_graph.invoke({
                "question": prompt,
                "sector": sector_filter_value
            })

            resposta_texto = resultado.get("response", "Desculpe, ocorreu um erro na consulta.")
            documentos = resultado.get("context", [])
            
            st.markdown(resposta_texto)
            
            if documentos:
                with st.expander("📄 Documentos Internos Consultados (Fontes RAG)"):
                    for doc in documentos:
                        fonte_nome = doc.metadata.get("source", "Documento Interno")
                        st.markdown(f"<span class='source-tag'>📁 {fonte_nome}</span>", unsafe_allow_html=True)
                        st.markdown(f"<div class='source-card'>\n\n{doc.page_content}\n\n</div>", unsafe_allow_html=True)
        
        # Salva no histórico da sessão
        st.session_state.messages.append({
            "role": "assistant", 
            "content": resposta_texto,
            "sources": documentos
        })
        st.rerun()
