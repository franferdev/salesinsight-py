{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOERMiPeRz8Pzi/+0uXXgWd",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/franferdev/salesinsight-py/blob/develop/gerar_DataSet_e_inspencionar_py.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "GSgjxTSO9Lmw",
        "outputId": "fae0ffcc-41bd-4e01-e640-8fb90fc2e331"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Dataset gerado com 200 registros.\n",
            "   id_venda  data_venda      cliente  produto     categoria        regiao  \\\n",
            "0         1  2025-12-31  Cliente_041    Mouse   Perifericos  Centro-Oeste   \n",
            "1         2  2025-07-26  Cliente_047  Teclado   Perifericos           Sul   \n",
            "2         3  2025-08-03  Cliente_004    Mouse   Perifericos         Norte   \n",
            "3         4  2025-02-23  Cliente_022  Teclado   Perifericos  Centro-Oeste   \n",
            "4         5  2025-10-26  Cliente_046  Monitor  Computadores         Norte   \n",
            "\n",
            "   quantidade  preco_unitario  \n",
            "0         7.0          132.46  \n",
            "1         2.0          246.83  \n",
            "2         3.0          108.46  \n",
            "3         8.0          228.97  \n",
            "4         4.0         1175.98  \n"
          ]
        }
      ],
      "source": [
        "import pandas as pd\n",
        "import numpy as np\n",
        "import random\n",
        "from datetime import datetime, timedelta\n",
        "\n",
        "def gerar_dataset_vendas(n_registros=200, seed=151):\n",
        "    \"\"\"Gera um dataset sintetico de vendas com dados sujos.\"\"\"\n",
        "    random.seed(seed)\n",
        "    np.random.seed(seed)\n",
        "\n",
        "    produtos = [\"Notebook\", \"Smartphone\", \"Tablet\", \"Monitor\",\n",
        "                \"Teclado\", \"Mouse\", \"Headset\"]\n",
        "    categorias = {\"Notebook\": \"Computadores\", \"Smartphone\": \"Celulares\",\n",
        "                  \"Tablet\": \"Celulares\", \"Monitor\": \"Computadores\",\n",
        "                  \"Teclado\": \"Perifericos\", \"Mouse\": \"Perifericos\",\n",
        "                  \"Headset\": \"Perifericos\"}\n",
        "    precos = {\"Notebook\": 3500, \"Smartphone\": 2200, \"Tablet\": 1800,\n",
        "              \"Monitor\": 1200, \"Teclado\": 250, \"Mouse\": 120,\n",
        "              \"Headset\": 350}\n",
        "    regioes = [\"Sudeste\", \"Sul\", \"Nordeste\", \"Centro-Oeste\", \"Norte\"]\n",
        "\n",
        "    data_inicio = datetime(2025, 1, 1)\n",
        "    dados = []\n",
        "\n",
        "    for i in range(n_registros):\n",
        "        produto = random.choice(produtos)\n",
        "        categoria = categorias[produto]\n",
        "        quantidade = random.randint(1, 10)\n",
        "        preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)\n",
        "        data = data_inicio + timedelta(days=random.randint(0, 364))\n",
        "        data_txt = data.strftime(\"%Y-%m-%d\")\n",
        "        cliente = f\"Cliente_{random.randint(1, 50):03d}\"\n",
        "\n",
        "        # --- sujeira proposital para a etapa de limpeza ---\n",
        "        if random.random() < 0.05:\n",
        "            quantidade = None                    # valor nulo\n",
        "        if random.random() < 0.04:\n",
        "            preco = None                         # valor nulo\n",
        "        if random.random() < 0.06:\n",
        "            produto = \"  \" + produto + \" \"       # espacos extras\n",
        "        if random.random() < 0.03:\n",
        "            data_txt = \"DATA INVALIDA\"           # data invalida\n",
        "        if random.random() < 0.10:\n",
        "            cliente = random.choice([            # ruido no nome\n",
        "                cliente.upper().replace(\"_\", \"-\"),\n",
        "                cliente + \"!!\",\n",
        "                \"  \" + cliente,\n",
        "                cliente.replace(\"Cliente_\", \"cliente#\"),\n",
        "            ])\n",
        "\n",
        "        dados.append({\n",
        "            \"id_venda\": i + 1,\n",
        "            \"data_venda\": data_txt,\n",
        "            \"cliente\": cliente,\n",
        "            \"produto\": produto,\n",
        "            \"categoria\": categoria,\n",
        "            \"regiao\": random.choice(regioes),\n",
        "            \"quantidade\": quantidade,\n",
        "            \"preco_unitario\": preco,\n",
        "        })\n",
        "\n",
        "    return pd.DataFrame(dados)\n",
        "\n",
        "\n",
        "# Gerar e salvar o CSV bruto\n",
        "df_bruto = gerar_dataset_vendas()\n",
        "df_bruto.to_csv(\"vendas.csv\", index=False)\n",
        "print(f\"Dataset gerado com {len(df_bruto)} registros.\")\n",
        "print(df_bruto.head())\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#verificar linhas e colunas\n",
        "df_bruto.shape\n",
        "print(f\"Dataset gerado com {df_bruto.shape[0]} linhas e {df_bruto.shape[1]} colunas.\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "O4WsrquEB8w9",
        "outputId": "4ba273ca-4bad-4562-a286-5f05b50a4c3e"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Dataset gerado com 200 linhas e 8 colunas.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#ver os nomes das colunas\n",
        "df_bruto.columns.tolist()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "8qYCHsk9ESbc",
        "outputId": "b578d3af-72e4-4fe0-82b5-4a3c64743981"
      },
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "['id_venda',\n",
              " 'data_venda',\n",
              " 'cliente',\n",
              " 'produto',\n",
              " 'categoria',\n",
              " 'regiao',\n",
              " 'quantidade',\n",
              " 'preco_unitario']"
            ]
          },
          "metadata": {},
          "execution_count": 9
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#ver o tipo de dado de cada coluna\n",
        "df_bruto.dtypes"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 335
        },
        "id": "j5wP0DCaE7_E",
        "outputId": "45780b97-4250-4671-b95f-68adcdc0e003"
      },
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "id_venda            int64\n",
              "data_venda         object\n",
              "cliente            object\n",
              "produto            object\n",
              "categoria          object\n",
              "regiao             object\n",
              "quantidade        float64\n",
              "preco_unitario    float64\n",
              "dtype: object"
            ],
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>0</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>id_venda</th>\n",
              "      <td>int64</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>data_venda</th>\n",
              "      <td>object</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>cliente</th>\n",
              "      <td>object</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>produto</th>\n",
              "      <td>object</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>categoria</th>\n",
              "      <td>object</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>regiao</th>\n",
              "      <td>object</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>quantidade</th>\n",
              "      <td>float64</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>preco_unitario</th>\n",
              "      <td>float64</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div><br><label><b>dtype:</b> object</label>"
            ]
          },
          "metadata": {},
          "execution_count": 10
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#Valores nulos — encontrar dados faltando\n",
        "df_bruto.isnull() #retorna a lista com true onde esta faltando\n",
        "df_bruto.isnull().sum() #localiza onde esta faltando"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 335
        },
        "id": "LEGJ3IPvFeME",
        "outputId": "daed88b1-95c1-4a9a-98b8-0533b28c07c5"
      },
      "execution_count": 18,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "id_venda          0\n",
              "data_venda        0\n",
              "cliente           0\n",
              "produto           0\n",
              "categoria         0\n",
              "regiao            0\n",
              "quantidade        7\n",
              "preco_unitario    6\n",
              "dtype: int64"
            ],
            "text/html": [
              "<div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>0</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>id_venda</th>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>data_venda</th>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>cliente</th>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>produto</th>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>categoria</th>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>regiao</th>\n",
              "      <td>0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>quantidade</th>\n",
              "      <td>7</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>preco_unitario</th>\n",
              "      <td>6</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div><br><label><b>dtype:</b> int64</label>"
            ]
          },
          "metadata": {},
          "execution_count": 18
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "#visualizar as primeiras linhas\n",
        "df_bruto.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 206
        },
        "id": "JKCIcODKGvwF",
        "outputId": "3913874c-03c6-4e84-f435-1ea198eed6e3"
      },
      "execution_count": 19,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "   id_venda  data_venda      cliente  produto     categoria        regiao  \\\n",
              "0         1  2025-12-31  Cliente_041    Mouse   Perifericos  Centro-Oeste   \n",
              "1         2  2025-07-26  Cliente_047  Teclado   Perifericos           Sul   \n",
              "2         3  2025-08-03  Cliente_004    Mouse   Perifericos         Norte   \n",
              "3         4  2025-02-23  Cliente_022  Teclado   Perifericos  Centro-Oeste   \n",
              "4         5  2025-10-26  Cliente_046  Monitor  Computadores         Norte   \n",
              "\n",
              "   quantidade  preco_unitario  \n",
              "0         7.0          132.46  \n",
              "1         2.0          246.83  \n",
              "2         3.0          108.46  \n",
              "3         8.0          228.97  \n",
              "4         4.0         1175.98  "
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-c6675d71-bb0e-45a5-83a5-5a480873cedf\" class=\"colab-df-container\">\n",
              "    <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>id_venda</th>\n",
              "      <th>data_venda</th>\n",
              "      <th>cliente</th>\n",
              "      <th>produto</th>\n",
              "      <th>categoria</th>\n",
              "      <th>regiao</th>\n",
              "      <th>quantidade</th>\n",
              "      <th>preco_unitario</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>1</td>\n",
              "      <td>2025-12-31</td>\n",
              "      <td>Cliente_041</td>\n",
              "      <td>Mouse</td>\n",
              "      <td>Perifericos</td>\n",
              "      <td>Centro-Oeste</td>\n",
              "      <td>7.0</td>\n",
              "      <td>132.46</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>2</td>\n",
              "      <td>2025-07-26</td>\n",
              "      <td>Cliente_047</td>\n",
              "      <td>Teclado</td>\n",
              "      <td>Perifericos</td>\n",
              "      <td>Sul</td>\n",
              "      <td>2.0</td>\n",
              "      <td>246.83</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>3</td>\n",
              "      <td>2025-08-03</td>\n",
              "      <td>Cliente_004</td>\n",
              "      <td>Mouse</td>\n",
              "      <td>Perifericos</td>\n",
              "      <td>Norte</td>\n",
              "      <td>3.0</td>\n",
              "      <td>108.46</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>4</td>\n",
              "      <td>2025-02-23</td>\n",
              "      <td>Cliente_022</td>\n",
              "      <td>Teclado</td>\n",
              "      <td>Perifericos</td>\n",
              "      <td>Centro-Oeste</td>\n",
              "      <td>8.0</td>\n",
              "      <td>228.97</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>5</td>\n",
              "      <td>2025-10-26</td>\n",
              "      <td>Cliente_046</td>\n",
              "      <td>Monitor</td>\n",
              "      <td>Computadores</td>\n",
              "      <td>Norte</td>\n",
              "      <td>4.0</td>\n",
              "      <td>1175.98</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>\n",
              "    <div class=\"colab-df-buttons\">\n",
              "\n",
              "  <div class=\"colab-df-container\">\n",
              "    <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-c6675d71-bb0e-45a5-83a5-5a480873cedf')\"\n",
              "            title=\"Convert this dataframe to an interactive table.\"\n",
              "            style=\"display:none;\">\n",
              "\n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\" viewBox=\"0 -960 960 960\">\n",
              "    <path d=\"M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z\"/>\n",
              "  </svg>\n",
              "    </button>\n",
              "\n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    .colab-df-buttons div {\n",
              "      margin-bottom: 4px;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "    <script>\n",
              "      const buttonEl =\n",
              "        document.querySelector('#df-c6675d71-bb0e-45a5-83a5-5a480873cedf button.colab-df-convert');\n",
              "      buttonEl.style.display =\n",
              "        google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "      async function convertToInteractive(key) {\n",
              "        const element = document.querySelector('#df-c6675d71-bb0e-45a5-83a5-5a480873cedf');\n",
              "        const dataTable =\n",
              "          await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                    [key], {});\n",
              "        if (!dataTable) return;\n",
              "\n",
              "        const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "          '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "          + ' to learn more about interactive tables.';\n",
              "        element.innerHTML = '';\n",
              "        dataTable['output_type'] = 'display_data';\n",
              "        await google.colab.output.renderOutput(dataTable, element);\n",
              "        const docLink = document.createElement('div');\n",
              "        docLink.innerHTML = docLinkHtml;\n",
              "        element.appendChild(docLink);\n",
              "      }\n",
              "    </script>\n",
              "  </div>\n",
              "\n",
              "\n",
              "    </div>\n",
              "  </div>\n"
            ],
            "application/vnd.google.colaboratory.intrinsic+json": {
              "type": "dataframe",
              "variable_name": "df_bruto",
              "summary": "{\n  \"name\": \"df_bruto\",\n  \"rows\": 200,\n  \"fields\": [\n    {\n      \"column\": \"id_venda\",\n      \"properties\": {\n        \"dtype\": \"number\",\n        \"std\": 57,\n        \"min\": 1,\n        \"max\": 200,\n        \"num_unique_values\": 200,\n        \"samples\": [\n          96,\n          16,\n          31\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"data_venda\",\n      \"properties\": {\n        \"dtype\": \"string\",\n        \"num_unique_values\": 149,\n        \"samples\": [\n          \"2025-01-24\",\n          \"2025-12-12\",\n          \"2025-10-08\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"cliente\",\n      \"properties\": {\n        \"dtype\": \"category\",\n        \"num_unique_values\": 78,\n        \"samples\": [\n          \"Cliente_038\",\n          \"Cliente_041\",\n          \"Cliente_024\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"produto\",\n      \"properties\": {\n        \"dtype\": \"category\",\n        \"num_unique_values\": 11,\n        \"samples\": [\n          \"Smartphone\",\n          \"Mouse\",\n          \"  Monitor \"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"categoria\",\n      \"properties\": {\n        \"dtype\": \"category\",\n        \"num_unique_values\": 3,\n        \"samples\": [\n          \"Perifericos\",\n          \"Computadores\",\n          \"Celulares\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"regiao\",\n      \"properties\": {\n        \"dtype\": \"category\",\n        \"num_unique_values\": 5,\n        \"samples\": [\n          \"Sul\",\n          \"Nordeste\",\n          \"Norte\"\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"quantidade\",\n      \"properties\": {\n        \"dtype\": \"number\",\n        \"std\": 2.801883387675996,\n        \"min\": 1.0,\n        \"max\": 10.0,\n        \"num_unique_values\": 10,\n        \"samples\": [\n          10.0,\n          2.0,\n          5.0\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    },\n    {\n      \"column\": \"preco_unitario\",\n      \"properties\": {\n        \"dtype\": \"number\",\n        \"std\": 1125.8563694398179,\n        \"min\": 103.4,\n        \"max\": 3907.69,\n        \"num_unique_values\": 194,\n        \"samples\": [\n          2033.1,\n          119.06,\n          342.42\n        ],\n        \"semantic_type\": \"\",\n        \"description\": \"\"\n      }\n    }\n  ]\n}"
            }
          },
          "metadata": {},
          "execution_count": 19
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "def inspecionar_dados(df_bruto):\n",
        "    \"\"\"Exibe as informacoes estruturais do DataFrame.\"\"\"\n",
        "    print(\"\\n=== INSPECAO INICIAL DO DATASET ===\")\n",
        "    print(f\"Shape: {df_bruto.shape}\")\n",
        "    print(f\"\\nColunas: {list(df_bruto.columns)}\")\n",
        "    print(f\"\\nTipos de dados:\\n{df_bruto.dtypes}\")\n",
        "    print(f\"\\nValores nulos por coluna:\\n{df_bruto.isnull().sum()}\")\n",
        "    print(f\"\\nPrimeiros registros:\\n{df_bruto.head()}\")\n",
        "    return\n"
      ],
      "metadata": {
        "id": "4SHVBF22HL8D"
      },
      "execution_count": 27,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "inspecionar_dados(df_bruto)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "-Xiw4qPQHWNE",
        "outputId": "4666e66a-3132-47b2-ec22-088a8a802d7b"
      },
      "execution_count": 28,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "=== INSPECAO INICIAL DO DATASET ===\n",
            "Shape: (200, 8)\n",
            "\n",
            "Colunas: ['id_venda', 'data_venda', 'cliente', 'produto', 'categoria', 'regiao', 'quantidade', 'preco_unitario']\n",
            "\n",
            "Tipos de dados:\n",
            "id_venda            int64\n",
            "data_venda         object\n",
            "cliente            object\n",
            "produto            object\n",
            "categoria          object\n",
            "regiao             object\n",
            "quantidade        float64\n",
            "preco_unitario    float64\n",
            "dtype: object\n",
            "\n",
            "Valores nulos por coluna:\n",
            "id_venda          0\n",
            "data_venda        0\n",
            "cliente           0\n",
            "produto           0\n",
            "categoria         0\n",
            "regiao            0\n",
            "quantidade        7\n",
            "preco_unitario    6\n",
            "dtype: int64\n",
            "\n",
            "Primeiros registros:\n",
            "   id_venda  data_venda      cliente  produto     categoria        regiao  \\\n",
            "0         1  2025-12-31  Cliente_041    Mouse   Perifericos  Centro-Oeste   \n",
            "1         2  2025-07-26  Cliente_047  Teclado   Perifericos           Sul   \n",
            "2         3  2025-08-03  Cliente_004    Mouse   Perifericos         Norte   \n",
            "3         4  2025-02-23  Cliente_022  Teclado   Perifericos  Centro-Oeste   \n",
            "4         5  2025-10-26  Cliente_046  Monitor  Computadores         Norte   \n",
            "\n",
            "   quantidade  preco_unitario  \n",
            "0         7.0          132.46  \n",
            "1         2.0          246.83  \n",
            "2         3.0          108.46  \n",
            "3         8.0          228.97  \n",
            "4         4.0         1175.98  \n"
          ]
        }
      ]
    }
  ]
}