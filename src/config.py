import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Verifica se a chave foi carregada (Opcional, mas recomendado para debugar)
if not os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY") == "COLOQUE_SUA_CHAVE_AQUI":
    print("Aviso: GOOGLE_API_KEY não foi configurada corretamente no arquivo .env.")

# Constantes de Configuração
VECTOR_DB_DIR = "./chroma_db"
EMBEDDING_PROVIDER = os.environ.get("EMBEDDING_PROVIDER", "google")  # Opções: "ollama" ou "gemini"
OLLAMA_EMBEDDING_MODEL = os.environ.get("OLLAMA_EMBEDDING_MODEL", "snowflake-arctic-embed2:latest")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "models/gemini-embedding-001")

# Configurações de LLM (Gemini / Ollama)
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "google")  # Opções: "gemini" ou "ollama"
LLM_MODEL = os.environ.get("LLM_MODEL", "gemini-2.5-flash")
OLLAMA_LLM_MODEL = os.environ.get("OLLAMA_LLM_MODEL", "llama3:8b")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")


