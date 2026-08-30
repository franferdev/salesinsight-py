from pathlib import Path
import pandas as pd
import re
from datetime import datetime, timedelta

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

limpeza_dados(df_limpo)
    