# Sales Insights

## Objetivo

O **Sales Insights** é um projeto de análise de dados de vendas desenvolvido em Python.

O objetivo é aplicar conceitos de manipulação, limpeza, transformação, análise e visualização de dados a partir de um arquivo CSV contendo registros de vendas.

O projeto organiza o processo de análise em um fluxo completo, desde o carregamento dos dados até a geração de métricas, gráficos e arquivos com os resultados.

---

## O que o projeto analisa

A análise utiliza os dados disponíveis no arquivo `vendas.csv`.

Entre as análises realizadas estão:

- inspeção inicial do dataset;
- identificação e tratamento de dados nulos e inválidos;
- cálculo da receita total das vendas;
- análise da receita por mês;
- identificação dos produtos com maior receita;
- análise da receita por categoria;
- análise da receita por região;
- segmentação de clientes por total gasto;
- cálculo de estatísticas utilizando NumPy;
- identificação de vendas com receita acima da média;
- criação de visualizações com Matplotlib e Seaborn.

Os clientes são classificados de acordo com o total gasto:

- **Bronze:** abaixo de R$ 5.000;
- **Prata:** de R$ 5.000 até abaixo de R$ 15.000;
- **Ouro:** R$ 15.000 ou mais.

---

## Conceitos aplicados

Durante o desenvolvimento foram aplicados conceitos de Python e análise de dados, como:

- funções;
- parâmetros e retornos;
- funções `lambda`;
- função de ordem superior;
- programação orientada a objetos;
- classes, métodos e atributos;
- leitura e escrita de arquivos;
- manipulação de DataFrames;
- tratamento de valores nulos;
- expressões regulares (Regex);
- conversão e tratamento de datas;
- `groupby` e agregações;
- operações vetorizadas com NumPy;
- broadcasting;
- filtragem booleana;
- criação de gráficos;
- exportação para CSV e JSON;
- organização do fluxo através da função `main()`.

---

##  Como executar no Google Colab

1. Abra o Google Colab.
2. Faça upload dos arquivos do projeto.
3. Certifique-se de que o arquivo `vendas.csv` esteja disponível no ambiente.
4. Instale as bibliotecas necessárias, caso ainda não estejam disponíveis:

```python
!pip install pandas numpy matplotlib seaborn
```

5. Execute o projeto:

```python
!python analisador.py
```

> Dependendo da estrutura utilizada no Colab, pode ser necessário ajustar o caminho dos arquivos.

---

## Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/franferdev/salesinsight-py.git
```

### 2. Entre na pasta do projeto

```bash
cd salesinsight-py
```

### 3. Instale as dependências

```bash
pip install pandas numpy matplotlib seaborn
```

### 4. Verifique se o arquivo `vendas.csv` está na pasta do projeto.

### 5. Execute

```bash
python analisador.py
```

O arquivo `analisador.py` executa o pipeline completo da análise.

---

## Estrutura de pastas

```text
sales-insights/
│
├── analisador.py
├── salesinsight.py
├── vendas.csv
├── README.md
│
└── outputs/
    │
    ├── metricas_por_mes.csv
    ├── segmentacao_clientes.csv
    ├── estatisticas_gerais.json
    │
    └── graficos/
        ├── grafico_receita_por_mes.png
        ├── grafico_top_5_produtos.png
        ├── grafico_quantidade_vs_receita.png
        └── painel_resumo.png
```

---

## Decisões técnicas

O projeto foi dividido em dois arquivos Python principais.

### `salesinsight.py`

Contém as funções responsáveis pelo processamento e análise dos dados, incluindo:

- inspeção;
- limpeza;
- transformação;
- cálculo de métricas;
- segmentação de clientes;
- estatísticas com NumPy;
- visualizações;
- função de ordem superior;
- exportação dos resultados.

Essa organização permite reutilizar as funções em outras partes do projeto.

### `analisador.py`

Contém a classe:

```python
AnalisadorDeVendas
```

A classe é responsável por organizar o fluxo da análise e manter o estado dos dados através dos atributos:

```python
self.df_bruto
self.df_limpo
self.metricas
self.clientes
self.estatisticas
self.relatorio_limpeza
```

O projeto utiliza a função:

```python
main()
```

para executar as etapas na seguinte ordem:

```text
Carregar dados
      ↓
Inspecionar dados
      ↓
Limpar dados
      ↓
Transformar dados
      ↓
Calcular métricas
      ↓
Segmentar clientes
      ↓
Calcular estatísticas
      ↓
Gerar gráficos
      ↓
Exportar resultados
      ↓
Exibir resumo
```

Os resultados são exportados automaticamente para a pasta `outputs`.

---

## Ferramentas utilizadas

- **Python**
- **Pandas** — manipulação e análise dos dados;
- **NumPy** — operações e cálculos numéricos;
- **Matplotlib** — criação de gráficos;
- **Seaborn** — visualização de dados;
- **Regex (`re`)** — validação e limpeza de dados;
- **JSON** — exportação das estatísticas;
- **Visual Studio Code** — desenvolvimento local;
- **Google Colab** — ambiente alternativo para execução;
- **Git e GitHub** — versionamento e disponibilização do projeto.

---

## Vídeo de apresentação

O vídeo com a apresentação e demonstração do projeto está disponível em:

**Link:** 

---

## Autora

Projeto desenvolvido como atividade prática de estudo de **Python e Análise de Dados**.
