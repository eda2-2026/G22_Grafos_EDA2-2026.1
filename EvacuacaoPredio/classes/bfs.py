from __future__ import annotations

import time
from collections import deque
from typing import Any

from .grafo import Grafo


class BFS:
    """Implementa a busca em largura para encontrar a rota de evacuação."""

    def __init__(self, grafo: Grafo) -> None:
        self.grafo = grafo

    def buscar_menor_caminho(self, origem_nome: str, mostrar_detalhes: bool = True) -> dict[str, Any]:
        """Executa o BFS e retorna os resultados da busca."""
        origem_nome = origem_nome.strip()
        origem = self.grafo.buscar_sala(origem_nome)

        if origem is None:
            raise ValueError(f"Sala '{origem_nome}' não encontrada no prédio.")

        if not self.grafo.listar_saidas():
            raise ValueError("Não há saídas definidas no prédio.")

        fila = deque([origem])
        visitados: set[str] = {origem.nome}
        predecessores: dict[str, str] = {}
        inicio = time.perf_counter()
        logs: list[str] = []

        self._registrar("\n==============================", logs, mostrar_detalhes)
        self._registrar("Buscando rota...", logs, mostrar_detalhes)
        self._registrar("==============================", logs, mostrar_detalhes)

        while fila:
            self._imprimir_fila(list(fila), logs, mostrar_detalhes)
            atual = fila.popleft()
            self._registrar("\nVisitando", logs, mostrar_detalhes)
            self._registrar(atual.nome, logs, mostrar_detalhes)

            if atual.saida:
                caminho = self._reconstruir_caminho(predecessores, atual.nome)
                tempo_ms = (time.perf_counter() - inicio) * 1000
                self._registrar("\nSaída encontrada", logs, mostrar_detalhes)
                self._imprimir_caminho(caminho, logs, mostrar_detalhes)
                return {
                    "origem": origem.nome,
                    "destino": atual.nome,
                    "visitados": len(visitados),
                    "distancia": max(len(caminho) - 1, 0),
                    "tempo_ms": tempo_ms,
                    "caminho": caminho,
                    "logs": logs,
                }

            novas_salas = []
            for vizinho in sorted(atual.vizinhos, key=lambda sala: sala.nome):
                if vizinho.nome not in visitados:
                    visitados.add(vizinho.nome)
                    predecessores[vizinho.nome] = atual.nome
                    fila.append(vizinho)
                    novas_salas.append(vizinho.nome)

            self._imprimir_novas_salas(novas_salas, logs, mostrar_detalhes)
            self._imprimir_predecessores(predecessores, logs, mostrar_detalhes)

        raise ValueError("Não existe caminho para nenhuma saída.")

    def _reconstruir_caminho(self, predecessores: dict[str, str], destino: str) -> list[str]:
        caminho = [destino]
        while caminho[-1] in predecessores:
            caminho.append(predecessores[caminho[-1]])
        return list(reversed(caminho))

    def _imprimir_fila(self, fila: list["Sala"], logs: list[str], mostrar: bool) -> None:
        nomes = [item.nome for item in fila]
        self._registrar("\nFila atual", logs, mostrar)
        self._registrar(f"[{ ' '.join(nomes) }]" if nomes else "[]", logs, mostrar)

    def _imprimir_novas_salas(self, novas_salas: list[str], logs: list[str], mostrar: bool) -> None:
        self._registrar("\nNovas salas descobertas", logs, mostrar)
        self._registrar(f"[{ ' '.join(novas_salas) }]" if novas_salas else "[]", logs, mostrar)

    def _imprimir_predecessores(self, predecessores: dict[str, str], logs: list[str], mostrar: bool) -> None:
        self._registrar("\nPais de cada vértice", logs, mostrar)
        for filho, pai in sorted(predecessores.items()):
            self._registrar(f"{filho}: {pai}", logs, mostrar)

    def _imprimir_caminho(self, caminho: list[str], logs: list[str], mostrar: bool) -> None:
        self._registrar("\nReconstrução do caminho", logs, mostrar)
        for index, sala in enumerate(caminho):
            self._registrar(sala, logs, mostrar)
            if index < len(caminho) - 1:
                self._registrar("->", logs, mostrar)

    def _registrar(self, texto: str, logs: list[str], mostrar: bool) -> None:
        logs.append(texto)
        if mostrar:
            print(texto)
