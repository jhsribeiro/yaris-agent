# Guia de Deploy & Evidências - YARIS AI Agent

Este documento contém o passo a passo detalhado para o deploy da aplicação **YARIS AI Agent** utilizando **Docker** e **Docker Compose** em uma máquina virtual (VM) Ubuntu, além dos procedimentos para geração das evidências de implantação.

---

## 📌 1. Visão Geral da Arquitetura de Deploy

A aplicação é composta por:
- **Interface & Orquestrador:** Streamlit (Porta `8501`) + LangChain / LangGraph.
- **Banco de Dados Vetorial:** ChromaDB (Persistido no volume `./chroma_db`).
- **Pipeline de Ingestão:** Script `pipeline_ingestao.py` executado via container para processar os documentos da pasta `./docs`.
- **Provedor de LLM/Embeddings:** Google Gemini AI Studio (configurado via `.env`).

```
 +-------------------------------------------------------+
 |                     Ubuntu VM                         |
 |                                                       |
 |  +-------------------------------------------------+  |
 |  |            Docker Container (Streamlit)         |  |
 |  |  - Python 3.12                                  |  |
 |  |  - App: app.py                                  |  |
 |  |  - Ingestão: pipeline_ingestao.py               |  |
 |  +-------------------------------------------------+  |
 |        | (Volume Persistente)                         |
 |        v                                              |
 |  [ ./chroma_db ]                                      |
 |                                                       |
 +-------------------------------------------------------+
        | (Porta 8501)
        v
 [ Usuários / Internet ]
```

---

## 🚀 2. Pré-requisitos na VM Ubuntu

No terminal SSH da VM (`ubuntu@vm1-yaris-agent-vnic1`), certifique-se de que os pacotes essenciais e o Docker estão instalados:

```bash
# 1. Atualizar o sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar Docker e Docker Compose Plugin
sudo apt install docker.io docker-buildx-plugin docker-compose-v2 git -y

# 3. Adicionar o usuário ao grupo Docker
sudo usermod -aG docker $USER
newgrp docker
```

---

## 🛠️ 3. Passo a Passo do Deploy

### Passo 3.1: Obter o Código
```bash
git clone https://github.com/jhsribeiro/yaris-agent.git
cd yaris-agent
```

### Passo 3.2: Configurar o Arquivo de Ambiente (`.env`)
Crie o arquivo `.env` na raiz do projeto:

```bash
nano .env
```

Insira suas credenciais:
```env
GOOGLE_API_KEY=sua_chave_api_aqui
EMBEDDING_PROVIDER=google
EMBEDDING_MODEL=models/gemini-embedding-001
LLM_PROVIDER=google
LLM_MODEL=gemini-2.5-flash
```

### Passo 3.3: Iniciar os Containers (Build & Run)
```bash
docker compose up -d --build
```

---

## 📂 4. Ingestão de Dados no Banco Vetorial

Após subir o container, execute o pipeline de ingestão de documentos em background:

```bash
docker compose exec yaris-agent python pipeline_ingestao.py
```

---

## 🔍 5. Checklist de Validação & Evidências de Deploy

Para comprovar que o deploy foi realizado com sucesso, execute e salve a saída dos seguintes comandos de verificação:

### Evidência 1: Status do Container Docker
**Comando:**
```bash
docker compose ps
```
**Saída Esperada:**
O container `yaris-agent` deve estar no estado `Up` / `running` exposto na porta `0.0.0.0:8501->8501/tcp`.

---

### Evidência 2: Logs da Aplicação
**Comando:**
```bash
docker compose logs --tail=50
```
**Saída Esperada:**
```
yaris-agent  |  You can now view your Streamlit app in your browser.
yaris-agent  |  Local URL: http://localhost:8501
yaris-agent  |  Network URL: http://0.0.0.0:8501
```

---

### Evidência 3: Teste de Resposta HTTP Local (Curl)
**Comando:**
```bash
curl -I http://localhost:8501
```
**Saída Esperada:**
Retorno com cabeçalho `HTTP/1.1 200 OK`.

---

### Evidência 4: Verificação da Persistência do ChromaDB
**Comando:**
```bash
ls -la chroma_db/
```
**Saída Esperada:**
Diretório contendo o arquivo `chroma.sqlite3` e as pastas de índice vetorial ativas.

---

## 🛡️ 6. Liberação de Firewall (Porta 8501)

1. **Firewall da Máquina (UFW):**
   ```bash
   sudo ufw allow 8501/tcp
   ```
2. **Oracle Cloud / Cloud Provider Security Rules:**
   - Adicionar regra de entrada (**Ingress Rule**):
     - **Source CIDR:** `0.0.0.0/0`
     - **IP Protocol:** `TCP`
     - **Destination Port Range:** `8501`

---

## 🔄 7. Comandos de Manutenção

- **Parar aplicação:** `docker compose down`
- **Reiniciar aplicação:** `docker compose restart`
- **Atualizar código e reiniciar:**
  ```bash
  git pull
  docker compose up -d --build
  ```
