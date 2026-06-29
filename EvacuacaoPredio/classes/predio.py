from __future__ import annotations

from .bfs import BFS
from .grafo import Grafo


class Predio:
    """Controla a lógica de cadastro e evacuação do prédio."""

    def __init__(self) -> None:
        self.grafo = Grafo()
        self.bfs = BFS(self.grafo)

    def cadastrar_sala(self, nome: str, saida: bool = False) -> None:
        """Cadastra uma nova sala no prédio."""
        self.grafo.adicionar_sala(nome, saida)

    def cadastrar_corredor(self, nome_a: str, nome_b: str) -> None:
        """Cria um corredor (aresta) entre duas salas."""
        self.grafo.adicionar_corredor(nome_a, nome_b)

    def definir_saida(self, nome: str) -> None:
        """Define uma sala existente como saída de emergência."""
        sala = self.grafo.buscar_sala(nome)
        if sala is None:
            raise ValueError(f"Sala '{nome}' não encontrada.")
        sala.saida = True

    def bloquear_corredor(self, nome_a: str, nome_b: str) -> None:
        """Bloqueia um corredor removendo a aresta do grafo."""
        self.grafo.remover_corredor(nome_a, nome_b)

    def desbloquear_corredor(self, nome_a: str, nome_b: str) -> None:
        """Desbloqueia um corredor adicionando a aresta de volta."""
        self.grafo.adicionar_corredor(nome_a, nome_b)

    def mostrar_mapa(self) -> None:
        """Exibe o mapa atual do prédio."""
        self.grafo.mostrar_mapa()

    def evacuar(self, origem_nome: str) -> dict[str, object]:
        """Inicia o processo de evacuação a partir de uma sala de origem."""
        resultado = self.bfs.buscar_menor_caminho(origem_nome)

        print("\n==============================")
        print("RELATÓRIO")
        print("==============================")
        print(f"Origem: Sala {resultado['origem']}")
        print(f"Destino: {resultado['destino']}")
        print(f"Quantidade de salas visitadas: {resultado['visitados']}")
        print(f"Distância: {resultado['distancia']} corredores")
        print(f"Tempo de execução: {resultado['tempo_ms']:.3f} ms")
        return resultado

    def carregar_predio(self, caminho: str) -> None:
        """Carrega o prédio e seus corredores a partir de um arquivo de texto."""
        self.grafo.carregar_de_arquivo(caminho)
