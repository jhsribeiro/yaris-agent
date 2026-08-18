FROM python:3.12-slim

WORKDIR /app

# Instala pacotes do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto
COPY . .

# Porta padrão do Streamlit
EXPOSE 8501

# Executa o Streamlit ouvindo em todas as interfaces
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
