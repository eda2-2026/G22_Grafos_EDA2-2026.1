from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from classes.predio import Predio


from pathlib import Path

class PredioGUI:
    """Interface gráfica para o sistema de evacuação inteligente."""

    def __init__(self) -> None:
        self.predio = Predio()
        caminho_dados = Path(__file__).resolve().parent / "dados" / "predio.txt"
        try:
            self.predio.carregar_predio(str(caminho_dados))
        except Exception as erro:
            print(f"Aviso: não foi possível carregar dados iniciais: {erro}")

        self.window = tk.Tk()
        self.window.title("Sistema de Evacuação Inteligente")
        self.window.geometry("1280x760")
        self.window.resizable(True, True)

        self.canvas = tk.Canvas(self.window, width=860, height=720, bg="white", highlightthickness=1, highlightbackground="#888")
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.controls = tk.Frame(self.window)
        self.controls.grid(row=0, column=1, sticky="n", padx=0, pady=10)

        self.origem_var = tk.StringVar()
        self.corredor_var = tk.StringVar()
        self.status_text = tk.Text(self.controls, width=32, height=30, state="disabled", wrap="word")
        self.posicoes: dict[str, tuple[int, int]] = {}
        self.caminho_atual: list[str] = []

        self._criar_controles()
        self._atualizar_origens()
        self._desenhar_mapa()

    def _criar_controles(self) -> None:
        titulo = ttk.Label(self.controls, text="Controles", font=("Segoe UI", 12, "bold"))
        titulo.grid(row=0, column=0, pady=(0, 12), sticky="w")

        botao_recarregar = ttk.Button(self.controls, text="Recarregar Mapa", command=self._recarregar_mapa)
        botao_recarregar.grid(row=1, column=0, sticky="ew", pady=4)

        origem_label = ttk.Label(self.controls, text="Localização da pessoa:")
        origem_label.grid(row=2, column=0, sticky="w", pady=(12, 4))

        self.origem_combo = ttk.Combobox(self.controls, textvariable=self.origem_var, state="readonly")
        self.origem_combo.grid(row=3, column=0, sticky="ew", pady=4)

        botao_rotas = ttk.Button(self.controls, text="Calcular Rota", command=self._calcular_rota)
        botao_rotas.grid(row=4, column=0, sticky="ew", pady=(4, 12))

        corredor_label = ttk.Label(self.controls, text="Bloquear / desbloquear corredor:")
        corredor_label.grid(row=5, column=0, sticky="w", pady=(12, 4))

        self.corredor_entry = ttk.Entry(self.controls, textvariable=self.corredor_var)
        self.corredor_entry.grid(row=6, column=0, sticky="ew", pady=4)
        self.corredor_entry.insert(0, "SalaA SalaB")

        botao_bloquear = ttk.Button(self.controls, text="Bloquear corredor", command=self._bloquear_corredor)
        botao_bloquear.grid(row=7, column=0, sticky="ew", pady=4)

        botao_desbloquear = ttk.Button(self.controls, text="Desbloquear corredor", command=self._desbloquear_corredor)
        botao_desbloquear.grid(row=8, column=0, sticky="ew", pady=4)

        status_label = ttk.Label(self.controls, text="Relatório / Mensagens:")
        status_label.grid(row=9, column=0, sticky="w", pady=(12, 4))

        self.status_text.grid(row=10, column=0, sticky="ew")

    def _recarregar_mapa(self) -> None:
        self.predio = Predio()
        try:
            self.predio.carregar_predio("dados/predio.txt")
            self._atualizar_origens()
            self.caminho_atual = []
            self._desenhar_mapa()
            self._escrever_status("Mapa recarregado a partir de dados/predio.txt.")
        except Exception as erro:
            messagebox.showerror("Erro", f"Falha ao recarregar o mapa: {erro}")

    def _atualizar_origens(self) -> None:
        nomes = sorted(self.predio.grafo.salas.keys())
        self.origem_combo["values"] = nomes
        if nomes:
            self.origem_combo.current(0)
            self.origem_var.set(nomes[0])

    def _calcular_rota(self) -> None:
        origem = self.origem_var.get().strip()
        if not origem:
            messagebox.showwarning("Atenção", "Informe a localização da pessoa.")
            return

        try:
            resultado = self.predio.bfs.buscar_menor_caminho(origem, mostrar_detalhes=False)
            self.caminho_atual = resultado["caminho"]
            mensagem = [f"Origem: Sala {resultado['origem']}", f"Destino: {resultado['destino']}", f"Salas visitadas: {resultado['visitados']}", f"Distância: {resultado['distancia']} corredores", f"Tempo: {resultado['tempo_ms']:.3f} ms", "", "Caminho encontrado:"]
            mensagem.extend(resultado["caminho"])
            self._escrever_status("\n".join(mensagem))
            self._desenhar_mapa()
        except ValueError as erro:
            self._escrever_status(f"Erro: {erro}")

    def _bloquear_corredor(self) -> None:
        texto = self.corredor_var.get().strip()
        partes = texto.split()
        if len(partes) != 2:
            messagebox.showwarning("Atenção", "Informe duas salas separadas por espaço.")
            return

        nome_a, nome_b = partes
        try:
            self.predio.bloquear_corredor(nome_a, nome_b)
            self.caminho_atual = []
            self._desenhar_mapa()
            self._escrever_status(f"Corredor {nome_a} {nome_b} bloqueado.")
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def _desbloquear_corredor(self) -> None:
        texto = self.corredor_var.get().strip()
        partes = texto.split()
        if len(partes) != 2:
            messagebox.showwarning("Atenção", "Informe duas salas separadas por espaço.")
            return

        nome_a, nome_b = partes
        try:
            self.predio.desbloquear_corredor(nome_a, nome_b)
            self._desenhar_mapa()
            self._escrever_status(f"Corredor {nome_a} {nome_b} desbloqueado.")
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

    def _escrever_status(self, texto: str) -> None:
        self.status_text.configure(state="normal")
        self.status_text.delete("1.0", tk.END)
        self.status_text.insert(tk.END, texto)
        self.status_text.configure(state="disabled")

    def _desenhar_mapa(self) -> None:
        self.canvas.delete("all")
        self.posicoes = self._calcular_posicoes()

        self._desenhar_corredores()
        if self.caminho_atual:
            self._desenhar_caminho(self.caminho_atual)
        self._desenhar_salas()

    def _calcular_posicoes(self) -> dict[str, tuple[int, int]]:
        nomes = sorted(self.predio.grafo.salas.keys())
        total = len(nomes)
        raio = 250
        centro_x = 330
        centro_y = 310
        posicoes: dict[str, tuple[int, int]] = {}

        for i, nome in enumerate(nomes):
            angulo = 2 * math.pi * i / max(total, 1)
            x = int(centro_x + math.cos(angulo) * raio)
            y = int(centro_y + math.sin(angulo) * raio)
            posicoes[nome] = (x, y)

        return posicoes

    def _desenhar_corredores(self) -> None:
        desenhados: set[tuple[str, str]] = set()
        for sala in self.predio.grafo.salas.values():
            origem = self.posicoes[sala.nome]
            for vizinho in sala.vizinhos:
                par = tuple(sorted((sala.nome, vizinho.nome)))
                if par in desenhados:
                    continue
                destino = self.posicoes[vizinho.nome]
                self.canvas.create_line(origem[0], origem[1], destino[0], destino[1], fill="#666", width=2)
                desenhados.add(par)

    def _desenhar_caminho(self, caminho: list[str]) -> None:
        for i in range(len(caminho) - 1):
            origem = self.posicoes[caminho[i]]
            destino = self.posicoes[caminho[i + 1]]
            self.canvas.create_line(origem[0], origem[1], destino[0], destino[1], fill="#c33", width=4)

    def _desenhar_salas(self) -> None:
        raio = 24
        for nome, (x, y) in self.posicoes.items():
            sala = self.predio.grafo.buscar_sala(nome)
            cor = "#8fbc8f" if sala.saida else "#87ceeb"
            self.canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill=cor, outline="#444", width=2)
            self.canvas.create_text(x, y, text=nome, fill="#000", font=("Segoe UI", 10, "bold"))

    def run(self) -> None:
        self.window.mainloop()
