from __future__ import annotations

from typing import Optional

from .sala import Sala


class Grafo:
    """Representa o prédio como um grafo não ponderado de salas e corredores."""

    def __init__(self) -> None:
        self.salas: dict[str, Sala] = {}

    def adicionar_sala(self, nome: str, saida: bool = False) -> Sala:
        """Adiciona uma sala ao prédio."""
        nome = nome.strip()
        if not nome:
            raise ValueError("O nome da sala não pode ser vazio.")

        if nome in self.salas:
            raise ValueError(f"A sala '{nome}' já está cadastrada.")

        sala = Sala(nome, saida)
        self.salas[nome] = sala
        return sala

    def adicionar_corredor(self, nome_a: str, nome_b: str) -> None:
        """Adiciona um corredor bidirecional entre duas salas."""
        nome_a = nome_a.strip()
        nome_b = nome_b.strip()

        if nome_a == nome_b:
            raise ValueError("Um corredor deve conectar duas salas diferentes.")

        sala_a = self.buscar_sala(nome_a)
        sala_b = self.buscar_sala(nome_b)

        if sala_a is None or sala_b is None:
            raise ValueError("Ambas as salas devem existir para cadastrar um corredor.")

        sala_a.adicionar_vizinho(sala_b)
        sala_b.adicionar_vizinho(sala_a)

    def remover_corredor(self, nome_a: str, nome_b: str) -> None:
        """Remove o corredor bidirecional entre duas salas."""
        nome_a = nome_a.strip()
        nome_b = nome_b.strip()

        sala_a = self.buscar_sala(nome_a)
        sala_b = self.buscar_sala(nome_b)

        if sala_a is None or sala_b is None:
            raise ValueError("Ambas as salas devem existir para bloquear/desbloquear um corredor.")

        sala_a.remover_vizinho(sala_b)
        sala_b.remover_vizinho(sala_a)

    def mostrar_mapa(self) -> None:
        """Exibe o mapa do prédio no formato de lista de adjacência."""
        if not self.salas:
            print("Nenhuma sala cadastrada no prédio.")
            return

        print("\nMAPA DO PRÉDIO")
        for nome in sorted(self.salas):
            sala = self.salas[nome]
            vizinhos = " ".join(sorted(sala.vizinhos_nomes()))
            marca_saida = " [SAÍDA]" if sala.saida else ""
            print(f"{nome}{marca_saida} -> {vizinhos}")

    def buscar_sala(self, nome: str) -> Optional[Sala]:
        """Retorna uma sala pelo nome, ou None se não existir."""
        return self.salas.get(nome.strip())

    def listar_saidas(self) -> list[Sala]:
        """Retorna todas as salas marcadas como saída."""
        return [sala for sala in self.salas.values() if sala.saida]

    def carregar_de_arquivo(self, caminho: str) -> None:
        """Carrega salas e corredores de um arquivo de texto simples."""
        with open(caminho, encoding="utf-8") as arquivo:
            for linha in arquivo:
                texto = linha.strip()
                if not texto or texto.startswith("#"):
                    continue

                partes = texto.split()
                if len(partes) == 1:
                    nome = partes[0]
                    saida = "saida" in nome.lower()
                    if nome not in self.salas:
                        self.adicionar_sala(nome, saida=saida)
                    elif saida:
                        self.salas[nome].saida = True
                elif len(partes) == 2:
                    nome_a, nome_b = partes
                    saida_a = "saida" in nome_a.lower()
                    saida_b = "saida" in nome_b.lower()
                    if nome_a not in self.salas:
                        self.adicionar_sala(nome_a, saida=saida_a)
                    if nome_b not in self.salas:
                        self.adicionar_sala(nome_b, saida=saida_b)
                    self.adicionar_corredor(nome_a, nome_b)
                else:
                    raise ValueError("Formato inválido no arquivo de dados. Use uma sala por linha ou duas salas por linha para corredores.")
