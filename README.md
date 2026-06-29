# Sistema de Evacuação Inteligente de Prédios

**Número da Lista:** 22  
**Disciplina:** Estruturas de Dados II

## Alunos

| Matrícula | Aluno |
|-----------|--------|
| 211061903 | Isaque Santos |
| 200023985 | Maria Eduarda dos Santos Marques |

## Sobre

Sistema desenvolvido em **Python** para simular a evacuação de um prédio durante uma emergência utilizando **Busca em Largura (BFS)** como algoritmo principal.

O projeto representa o prédio como um grafo não ponderado, onde cada sala é um vértice e cada corredor é uma aresta. O objetivo é encontrar o menor caminho entre a sala em que a pessoa se encontra e a saída mais próxima, preservando a estrutura do grafo por lista de adjacência.

A principal motivação para a escolha do BFS é sua capacidade de encontrar a rota com o menor número de corredores em grafos não ponderados.

---

## Screenshots

Tela inicial do programa

![Tela inicial](assets/menu.png)

Tela de cadastro de salas e corredores

![Cadastro](assets/cadastro.png)

Tela de exibição do mapa e rota de fuga

![Listagem](assets/listagem.png)

---

## Instalação

### Pré-requisitos

- Python 3.x
- Terminal ou Prompt de Comando

### Execução

No diretório do projeto:

```bash
cd EvacuacaoPredio
python main.py
```

Ou para iniciar a interface gráfica:

```bash
python main.py gui
```

---

## Algoritmo Utilizado

### Busca em Largura (BFS)

O BFS explora o grafo em níveis, visitando primeiro todos os nós a distância 1, depois distância 2 e assim por diante. Isso permite encontrar o menor caminho em número de arestas quando o grafo não é ponderado.

