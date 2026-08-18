import os
from src.graph.build import app_graph

def gerar_e_salvar_grafo():
    """
    Gera o diagrama do grafo do LangGraph em formato PNG e salva na pasta assets.
    Exibe a imagem se executado em ambiente IPython/Jupyter.
    """
    try:
        graph_bytes = app_graph.get_graph().draw_mermaid_png()
        os.makedirs("assets", exist_ok=True)
        caminho_img = os.path.join("assets", "fluxo_langgraph.png")
        
        with open(caminho_img, "wb") as f:
            f.write(graph_bytes)
            
        print("\n--- Visualização do Fluxo do Agente ---")
        print(f"Imagem do grafo salva com sucesso em: {caminho_img}")
        
        try:
            from IPython.display import Image, display
            display(Image(graph_bytes))
        except ImportError:
            pass
            
        return caminho_img
    except Exception as e:
        print(f"\nNão foi possível gerar a imagem do grafo: {e}")
        return None

if __name__ == "__main__":
    gerar_e_salvar_grafo()

