from __future__ import annotations

from .predio import Predio


class Menu:
    """Interface de texto para interação com o usuário."""

    def __init__(self) -> None:
        self.predio = Predio()
        self.origem_atual: str | None = None

    def exibir_menu(self) -> None:
        print("\n==================================")
        print("Sistema de Evacuação Inteligente")
        print("==================================")
        print("1 - Cadastrar sala")
        print("2 - Cadastrar corredor")
        print("3 - Definir saída")
        print("4 - Mostrar mapa")
        print("5 - Informar localização da pessoa")
        print("6 - Calcular rota de fuga")
        print("7 - Bloquear corredor")
        print("8 - Desbloquear corredor")
        print("9 - Sair")

    def executar(self) -> None:
        while True:
            self.exibir_menu()
            escolha = input("Escolha uma opção: ").strip()

            if escolha == "1":
                self.cadastrar_sala()
            elif escolha == "2":
                self.cadastrar_corredor()
            elif escolha == "3":
                self.definir_saida()
            elif escolha == "4":
                self.mostrar_mapa()
            elif escolha == "5":
                self.informar_localizacao()
            elif escolha == "6":
                self.calcular_rota_de_fuga()
            elif escolha == "7":
                self.bloquear_corredor()
            elif escolha == "8":
                self.desbloquear_corredor()
            elif escolha == "9":
                print("Saindo do sistema. Até breve!")
                break
            else:
                print("Opção inválida. Tente novamente.")

    def cadastrar_sala(self) -> None:
        nome = self.ler_texto("Nome da sala: ")
        if not nome:
            print("Nome inválido.")
            return

        saida = input("É uma saída de emergência? (s/n): ").strip().lower() == "s"
        try:
            self.predio.cadastrar_sala(nome, saida)
            print(f"Sala '{nome}' cadastrada com sucesso.")
        except ValueError as erro:
            print(f"Erro: {erro}")

    def cadastrar_corredor(self) -> None:
        texto = self.ler_texto("Informe duas salas separadas por espaço: ")
        partes = texto.split()

        if len(partes) != 2:
            print("É preciso informar exatamente duas salas.")
            return

        nome_a, nome_b = partes
        try:
            self.predio.cadastrar_corredor(nome_a, nome_b)
            print(f"Corredor entre '{nome_a}' e '{nome_b}' cadastrado.")
        except ValueError as erro:
            print(f"Erro: {erro}")

    def definir_saida(self) -> None:
        nome = self.ler_texto("Nome da sala de saída: ")
        try:
            self.predio.definir_saida(nome)
            print(f"Sala '{nome}' definida como saída.")
        except ValueError as erro:
            print(f"Erro: {erro}")

    def mostrar_mapa(self) -> None:
        self.predio.mostrar_mapa()

    def informar_localizacao(self) -> None:
        nome = self.ler_texto("Localização da pessoa: ")
        sala = self.predio.grafo.buscar_sala(nome)
        if sala is None:
            print(f"Sala '{nome}' não existe no prédio.")
            return

        self.origem_atual = nome
        print(f"Localização registrada: {nome}")

    def calcular_rota_de_fuga(self) -> None:
        if not self.origem_atual:
            print("Informe a localização da pessoa antes de calcular a rota.")
            return

        try:
            self.predio.evacuar(self.origem_atual)
        except ValueError as erro:
            print(f"Erro: {erro}")

    def bloquear_corredor(self) -> None:
        texto = self.ler_texto("Informe o corredor a ser bloqueado (salaA salaB): ")
        partes = texto.split()

        if len(partes) != 2:
            print("É preciso informar exatamente duas salas.")
            return

        nome_a, nome_b = partes
        try:
            self.predio.bloquear_corredor(nome_a, nome_b)
            print(f"Corredor entre '{nome_a}' e '{nome_b}' bloqueado.")
        except ValueError as erro:
            print(f"Erro: {erro}")

    def desbloquear_corredor(self) -> None:
        texto = self.ler_texto("Informe o corredor a ser desbloqueado (salaA salaB): ")
        partes = texto.split()

        if len(partes) != 2:
            print("É preciso informar exatamente duas salas.")
            return

        nome_a, nome_b = partes
        try:
            self.predio.desbloquear_corredor(nome_a, nome_b)
            print(f"Corredor entre '{nome_a}' e '{nome_b}' desbloqueado.")
        except ValueError as erro:
            print(f"Erro: {erro}")

    def ler_texto(self, prompt: str) -> str:
        texto = input(prompt).strip()
        return texto
