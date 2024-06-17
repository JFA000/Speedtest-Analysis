import os
import pandas as pd

# Caminho para a pasta contendo os arquivos .xlsx
pasta_caminho = 'Municipios/'

# Verifica se a pasta existe
if not os.path.exists(pasta_caminho):
    raise FileNotFoundError(f"A pasta especificada não existe: {pasta_caminho}")

# Lista para armazenar os dataframes de cada arquivo .xlsx
dataframes = []

# Contador de arquivos processados
arquivos_processados = 0

# Itera sobre todos os arquivos na pasta
for arquivo in os.listdir(pasta_caminho):
    if arquivo.endswith('.xlsx'):
        # Caminho completo do arquivo
        caminho_arquivo = os.path.join(pasta_caminho, arquivo)
        
        try:
            # Leitura do arquivo .xlsx, pulando as duas primeiras linhas
            df = pd.read_excel(caminho_arquivo, skiprows=2)
            
            # Selecionando apenas as colunas A até M
            colunas_ate = df.columns[:2]  # Seleciona as primeiras 2 colunas (A e B)
            
            # Verificando as linhas válidas (completas) nas colunas selecionadas
            df_valid = df.dropna(subset=colunas_ate, how='any')  # Remove linhas com valores ausentes nas colunas A até M
            
            # Adiciona o dataframe à lista
            dataframes.append(df_valid)
            
            # Incrementa o contador de arquivos processados
            arquivos_processados += 1

        except Exception as e:
            print(f"Erro ao processar o arquivo {caminho_arquivo}: {e}")

# Verifica se algum arquivo foi processado
if arquivos_processados == 0:
    raise ValueError("Nenhum arquivo .xlsx foi processado.")

# Concatenando todos os dataframes em um único dataframe
df_final = pd.concat(dataframes, ignore_index=True)

# Salvando o dataframe final em um novo arquivo Excel
df_final.to_excel('idh_municipios_ibge.xlsx', index=False)

# Mostrando informações sobre o dataframe final
print(f"Total de arquivos processados: {arquivos_processados}")
print(f"DataFrame final contém {df_final.shape[0]} linhas e {df_final.shape[1]} colunas.")
