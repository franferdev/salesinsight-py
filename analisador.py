from pathlib import Path
import pandas as pd

from salesinsight import (
    inspecionar_dados,
    limpeza_dados,
    criar_colunas_derivadas,
    calcular_metricas,
    segmentar_clientes,
    calcular_estatisticas,
    gerar_visualizacoes,
    processar_coluna,
    exportar_resultados
)


class AnalisadorDeVendas:

    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.df_bruto = None
        self.df_limpo = None
        self.metricas = {}
        self.clientes = None
        self.estatisticas = {}
        self.relatorio_limpeza = {}

    def carregar(self):
        self.df_bruto = pd.read_csv(self.caminho_arquivo)

    def limpar(self):
        """Limpa os dados e guarda o relatorio da limpeza."""

        self.df_limpo, self.relatorio_limpeza = limpeza_dados(
            self.df_bruto.copy())

    def transformar(self):
        """Cria colunas derivadas e aplica transformacoes reutilizaveis."""

        self.df_limpo = criar_colunas_derivadas(
            self.df_limpo
        )

        self.df_limpo = processar_coluna(
            self.df_limpo,
            "receita_total",
            lambda x: round(x / 1000, 2),
            nome_saida="receita_em_milhares"
        )

        self.df_limpo = processar_coluna(
            self.df_limpo,
            "quantidade",
            lambda q: "Alto Volume" if q > 5 else "Baixo Volume",
            nome_saida="perfil_volume"
        )

    def analisar(self):
        self.metricas = calcular_metricas(self.df_limpo)
        self.clientes = segmentar_clientes(self.df_limpo)
        self.estatisticas = calcular_estatisticas(self.df_limpo)

    def visualizar(self):
        gerar_visualizacoes(
            self.df_limpo,
            self.metricas
        )

    def resumo(self):
        print("\n=== RESUMO ===")
        print(f"Registros brutos: {len(self.df_bruto)}")
        print(f"Registros limpos: {len(self.df_limpo)}")
        print(f"Clientes: {len(self.clientes)}")
        
def main():
    """Executa o pipeline completo de analise de vendas."""

    pasta_atual = Path(__file__).resolve().parent
    caminho_arquivo = pasta_atual / "vendas.csv"
    pasta_saida = pasta_atual / "outputs"

    if not caminho_arquivo.exists():
        print("Erro: arquivo vendas.csv não encontrado.")
        return

    analisador = AnalisadorDeVendas(
        caminho_arquivo
    )

    # 1 - Carregar
    analisador.carregar()

    # 2 - Inspecionar
    inspecionar_dados(
        analisador.df_bruto
    )

    # 3 - Limpar
    analisador.limpar()

    # 4 - Transformar
    analisador.transformar()

    # 5 - Analisar
    analisador.analisar()

    # 6 - Visualizar
    analisador.visualizar()

    # 7 - Exportar
    exportar_resultados(
        analisador.metricas,
        analisador.clientes,
        analisador.estatisticas,
        pasta_saida
    )

    # 8 - Resumo
    analisador.resumo()


if __name__ == "__main__":
    main()