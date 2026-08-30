from pathlib import Path
import pandas as pd
import re
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

pasta_atual = Path(__file__).resolve().parent
df_bruto = pd.read_csv(pasta_atual /    "vendas.csv")

def inspecionar_dados(df_bruto):
    """Exibe as informacoes estruturais do DataFrame."""
    print("\n=== INSPECAO INICIAL DO DATASET ===")
    print(f"Shape: {df_bruto.shape}")
    print(f"\nColunas: {list(df_bruto.columns)}")
    print(f"\nTipos de dados:\n{df_bruto.dtypes}")
    print(f"\nValores nulos por coluna:\n{df_bruto.isnull().sum()}")
    print(f"\nPrimeiros registros:\n{df_bruto.head()}")
    return

inspecionar_dados(df_bruto)

df_limpo = df_bruto.copy()

def limpeza_dados(df_limpo):
    """Limpa e padroniza os dados do DataFrame."""
    print("\n=== INICIO DA LIMPEZA DE DADOS ===")
    
    # Limpar espaço extras em todas as colunas que sao strings #
    for coluna in df_limpo.select_dtypes(include=['object', 'string']).columns:
        df_limpo[coluna] = df_limpo[coluna].str.strip()

    # Converte a coluna data_venda para o formato de data #
    df_limpo["data_venda"] = pd.to_datetime(df_limpo["data_venda"], errors="coerce")
    
    # Verificar quantidades de nulos e quantidade de registros apos a conversao de data #
    datas_nulas_registradas = df_limpo["data_venda"].isna().sum()
    print(f"\nQuantidade de registros com data_venda nula que serão removidos apos conversao: {datas_nulas_registradas}")

    # Remover linhas nulas geradas após a correção de dados invalidos para nulos (NaT) #
    df_limpo = df_limpo.dropna(subset=["data_venda"])
    
    # Verificar quantidade de registros de nulos para quantidade e preco_unitario #
    nulos_quantidade = df_limpo["quantidade"].isna().sum()
    nulos_preco_unitario = df_limpo["preco_unitario"].isna().sum()
    print(f"\nQuantidade de registros com preco_unitario nulo que serão removidos: {nulos_preco_unitario}")
    print(f"\nQuantidade de registros com quantidade nula que serão removidos: {nulos_quantidade}")

    # Remover nulos de quantidade e preco_unitario:#
    df_limpo = df_limpo.dropna(subset=["quantidade", "preco_unitario"])

    # Garantir tipo de dados #
    df_limpo["quantidade"] = df_limpo["quantidade"].astype(int)
    df_limpo["preco_unitario"] = df_limpo["preco_unitario"].astype(float)
 
    # Remover caracteres indesejaveis da coluna cliente #
    n_cliente_registros_antes = df_limpo["cliente"].shape[0]
    df_limpo["cliente"] = df_limpo["cliente"].apply(
        lambda nome: re.sub(r"[^a-zA-Z-0-9À-ÿ_]", "", str(nome).strip())
        )
    print(f"\nQuantidade de registros de clientes antes da limpeza: {n_cliente_registros_antes}")
    
    # Validacao de formato com padrao para nome de clientes #
    padrao_cliente = re.compile(r"^Cliente_\d{3}$", flags=re.IGNORECASE)
    clientes_validos = df_limpo["cliente"].str.fullmatch(padrao_cliente)
    clientes_invalidos = (~clientes_validos).sum()
    df_limpo = df_limpo.loc[clientes_validos].copy()
    n_cliente_registros_depois = df_limpo["cliente"].shape[0]
    print(f"\nQuantidade de registros de clientes invalidos removidos: {clientes_invalidos}")
    print(f"\nQuantidade de registros de clientes depois da limpeza: {n_cliente_registros_depois}")
    
    # Relatorio final de quantidade de registros apos a limpeza #
    print(f"\nQuantidade de registros/linhas totais apos a limpeza: {df_limpo.shape[0]}")

    return df_limpo

df_limpo = limpeza_dados(df_limpo)
    
# Criação de Colunas Derivadas (RF04)

def criar_colunas_derivadas(df_limpo):
    """Cria colunas derivadas no DataFrame."""
    print("\n=== CRIACAO DE COLUNAS DERIVADAS ===")
        
    # Criar coluna receita_total #
    df_limpo["receita_total"] = df_limpo["quantidade"] * df_limpo["preco_unitario"]
    
    # Criar coluna mes #
    df_limpo["mes"] = df_limpo["data_venda"].dt.month
    
    # Criar coluna mes_nome #
    meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }
    
    df_limpo["mes_nome"] = df_limpo["mes"].map(meses)
    
    # Criar coluna trimestre #
    df_limpo["trimestre"] = df_limpo["data_venda"].dt.quarter
    
    # Criar coluna ano #
    df_limpo["ano"] = df_limpo["data_venda"].dt.year
    
    # Criar coluna faixa_receita_item com np #
    condicoes = [
    df_limpo["receita_total"] < 500,
    (df_limpo["receita_total"] >= 500) & (df_limpo["receita_total"] < 5000),
    df_limpo["receita_total"] >= 5000
    ]

    faixas = ["Baixo Valor", "Medio Valor", "Alto Valor"]

    df_limpo["faixa_receita_item"] = np.select(
    condicoes, faixas, default="Nao Classificado"
    )

    print(f"\nColunas derivadas criadas: {['receita_total', 'mes', 'mes_nome', 'trimestre', 'ano', 'faixa_receita_item']}")
    return df_limpo

colunas_derivadas = criar_colunas_derivadas(df_limpo)

# RF05 – Calcular Métricas Agregadas com groupby #

def calcular_metricas(df_limpo):
    """Calcula métricas agregadas usando groupby."""
    
    por_mes = df_limpo.groupby(["mes", "mes_nome"]).agg(
    receita_total=("receita_total", "sum"),
    quantidade=("quantidade", "sum"),
    n_vendas=("id_venda", "count")
    ).reset_index()
    
    top_produtos = df_limpo.groupby("produto").agg(
    receita_total=("receita_total", "sum")
    ).sort_values("receita_total", ascending=False).head(5).reset_index()
    
    por_categoria = df_limpo.groupby("categoria").agg(
    receita_total=("receita_total", "sum")
    ).reset_index()
    
    por_regiao = df_limpo.groupby("regiao").agg(
    receita_total=("receita_total", "sum"),
    receita_media=("receita_total", "mean"),
    ).reset_index()

    metricas = {
    "por_mes": por_mes,
    "top_produtos": top_produtos,
    "por_categoria": por_categoria,
    "por_regiao": por_regiao
    }
    return metricas

metricas = calcular_metricas(df_limpo)

print("\n=== MÉTRICAS CALCULADAS ===")

print("\n--- VENDAS POR MÊS ---")
print(metricas["por_mes"].to_string(index=False))

print("\n--- TOP 5 PRODUTOS ---")
print(metricas["top_produtos"].to_string(index=False))

print("\n--- RECEITA POR CATEGORIA ---")
print(metricas["por_categoria"].to_string(index=False))

print("\n--- RECEITA POR REGIÃO ---")
print(metricas["por_regiao"].to_string(index=False))

# RF06 – Segmentar Clientes por Nível de Gasto #

def segmentar_clientes(df_limpo):
    """ Agrupa por cliente, soma a receita e classifica em
    Bronze / Prata / Ouro.
    Retorna um DataFrame com: cliente, total_gasto, segmento."""
    clientes = df_limpo.groupby("cliente").agg(
    total_gasto=("receita_total", "sum")
    ).reset_index()

    # Classificação de clientes em segmentos com lambda #  
    clientes["segmento"] = clientes["total_gasto"].apply(
    lambda gasto: "Bronze" if gasto < 5000 else ("Prata" if gasto < 15000 else "Ouro")
    if gasto >= 15000 else "Ouro"
    )
        
    print("\n=== OS 10 MAIORES CLIENTES POR TOTAL GASTO === ")
    print(clientes.sort_values("total_gasto", ascending=False).head(10).to_string(index=False))
    print("\n=== QUANTIDADE DE CLIENTES POR SEGMENTO === ")
    print(clientes["segmento"].value_counts().to_string())
    
    return clientes

clientes_segmentados = segmentar_clientes(df_limpo)
    
   # RF07 – Operações Numéricas com NumPy #

def calcular_estatisticas(df_limpo):
    """
    Aplica operacoes NumPy sobre a coluna receita_total.
    Retorna um dicionario com os valores agregados calculados.
    """
    receitas = df_limpo["receita_total"].to_numpy()
    media = np.mean(receitas)
    mediana = np.median(receitas)
    desvio_np = np.std(receitas)
    desvio_pandas = pd.Series(receitas).std()
    soma = np.sum(receitas)
    minimo = np.min(receitas)
    maximo = np.max(receitas)
    print("\n=== ESTATÍSTICAS DESCRITIVAS DA COLUNA RECEITA_TOTAL ===")
    print(f" Média: {media}")
    print(f" Mediana: {mediana}")
    print(f" Desvio Padrão: {desvio_np}")
    print(f" Desvio Padrão (Pandas): {desvio_pandas}")
    print(f" Soma: {soma}")
    print(f" Mínimo: {minimo}") 
    print(f" Máximo: {maximo}")
    
    # Broadcasting com NumPy para criar uma coluna de receita_total_padronizada e escalonar 0-1 #
    receita_total_padronizada = (receitas - minimo) / (maximo - minimo)
    print(f"\nReceita total padronizada (primeiros 5 registros): {receita_total_padronizada[:5]}")
    
    # Filtragem booleana com NumPy para identificar registros acima da média #
    acima_media = receitas > media
    print(f"\nQuantidade de registros com receita_total acima da média: {np.sum(acima_media)}")
    
    estatisticas = {
    "media": media, 
    "mediana": mediana,
    "desvio_np": desvio_np ,
    "desvio_pandas": desvio_pandas,
    "soma": soma,
    "minimo": minimo,
    "maximo": maximo,
    "qtd_acima_media": np.sum(acima_media)
    }
    
    return estatisticas

estatisticas = calcular_estatisticas(df_limpo)

# RF08 – Criar Visualizações com Matplotlib e Seaborn #

# configurações globais para os gráficos #
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10
plt.rcParams["legend.fontsize"] = 10
plt.rcParams["figure.titlesize"] = 16
plt.rcParams["figure.dpi"] = 100
print("Estilo para gráficos configurado.")

# Gera visualizações com Matplotlib e Seaborn. #

def gerar_visualizacoes(df_limpo, metricas):
    
    os.makedirs(pasta_atual / "outputs/graficos", exist_ok=True)
      
    # Gráfico 1 — Linha: Receita total por mês ao longo do período #
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=metricas["por_mes"], x="mes", y="receita_total", marker="o")
    plt.title("Receita Total por Mês")
    plt.xlabel("Mês")
    plt.ylabel("Receita Total")
    plt.xticks(ticks=metricas["por_mes"]["mes"], labels=metricas["por_mes"]["mes_nome"])
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(pasta_atual / "outputs/graficos/grafico_receita_por_mes.png")
    plt.close()
    
    # Gráfico 2 — Barra: Top 5 produtos (ou categorias) por receita #  
    plt.figure(figsize=(10, 6))
    sns.barplot(data=metricas["top_produtos"], x="produto", y="receita_total", hue="produto", palette="viridis", legend=False)
    plt.title("Top 5 Produtos por Receita Total")
    plt.xlabel("Produto")
    plt.ylabel("Receita Total")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(pasta_atual / "outputs/graficos/grafico_top_5_produtos.png")
    plt.close()

    # Gráfico 3 — Dispersão: quantidade × receita_total, colorido por categoria
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_limpo, x="quantidade", y="receita_total", hue="categoria", palette="colorblind", alpha=0.7)
    plt.title("Dispersão: Quantidade vs Receita Total")
    plt.xlabel("Quantidade")
    plt.ylabel("Receita Total")
    plt.tight_layout()
    plt.savefig(pasta_atual / "outputs/graficos/grafico_quantidade_vs_receita.png")
    plt.close()
    
    # Gráfico 4 — Subplots
    # Figura 2×2 combinando as visões acima e a receita por região
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    
    # Receita por mês  
    axes[0, 0].plot(metricas["por_mes"]["mes"], metricas["por_mes"]["receita_total"], marker="o")
    axes[0, 0].set_title("Receita por Mês")
    axes[0, 0].set_xlabel("Mês")
    axes[0, 0].set_ylabel("Receita Total")
    
    axes[0,1].bar(metricas["top_produtos"]["produto"], metricas["top_produtos"]["receita_total"], color="orange")
    axes[0, 1].set_title("Top 5 Produtos")
    axes[0, 1].set_xlabel("Produto")
    axes[0, 1].set_ylabel("Receita Total")
    
    axes[1, 0].scatter(df_limpo["quantidade"], df_limpo["receita_total"], c=df_limpo["categoria"].astype('category').cat.codes, cmap="Set1") 
    axes[1, 0].set_title("Quantidade vs Receita")
    axes[1, 0].set_xlabel("Quantidade")
    axes[1, 0].set_ylabel("Receita Total")
    
    axes[1, 1].bar(metricas["por_regiao"]["regiao"], metricas["por_regiao"]["receita_total"], color="purple")
    axes[1, 1].set_title("Receita por Região")
    axes[1, 1].set_xlabel("Região")
    axes[1, 1].set_ylabel("Receita Total")
    fig.suptitle("Sales Insights - Painel de Resumo", fontsize=16)
    plt.tight_layout()
    plt.savefig(pasta_atual / "outputs/graficos/painel_resumo.png", dpi=150)
    plt.close()
    


gerar_visualizacoes(df_limpo, metricas)
