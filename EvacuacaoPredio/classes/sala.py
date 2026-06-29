from __future__ import annotations


class Sala:
    """Representa uma sala do prédio com seus corredores e status de saída."""

    def __init__(self, nome: str, saida: bool = False) -> None:
        self.nome = nome.strip()
        self.vizinhos: list["Sala"] = []
        self.saida = saida

    def adicionar_vizinho(self, sala: "Sala") -> None:
        """Adiciona uma sala vizinha sem criar duplicatas."""
        if sala is None or sala.nome == self.nome:
            return

        if sala not in self.vizinhos:
            self.vizinhos.append(sala)

    def remover_vizinho(self, sala: "Sala") -> None:
        """Remove um corredor entre duas salas se existir."""
        if sala in self.vizinhos:
            self.vizinhos.remove(sala)

    def vizinhos_nomes(self) -> list[str]:
        """Retorna os nomes das salas vizinhas para exibição."""
        return [sala.nome for sala in self.vizinhos]

    def __repr__(self) -> str:
        return f"Sala({self.nome!r}, saida={self.saida})"
