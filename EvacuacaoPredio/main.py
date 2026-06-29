import sys
from pathlib import Path

from classes.menu import Menu


def main() -> None:
    caminho_dados = Path(__file__).resolve().parent / "dados" / "predio.txt"

    if len(sys.argv) > 1 and sys.argv[1].lower() in ("gui", "--gui"):
        from gui import PredioGUI

        PredioGUI().run()
        return

    menu = Menu()

    try:
        menu.predio.carregar_predio(str(caminho_dados))
        print(f"Arquivo de dados encontrado e carregado: {caminho_dados}")
    except FileNotFoundError:
        print("Arquivo de dados não encontrado. Inicie o sistema manualmente.")
    except Exception as erro:
        print(f"Aviso: falha ao carregar dados iniciais: {erro}")

    menu.executar()


if __name__ == "__main__":
    main()
