import os

# Lista de arquivos baixados
downloaded_files = [
    '2023-01-01_performance_fixed_tiles.parquet',
    '2023-04-01_performance_fixed_tiles.parquet',
    '2023-07-01_performance_fixed_tiles.parquet',
    '2023-10-01_performance_fixed_tiles.parquet'
]

for file_name in downloaded_files:
    # Constrói o caminho completo para o arquivo
    file_path = os.path.join(file_name)

    # Extrai o ano do nome do arquivo original
    year = file_name.split('-')[0]

    # Extrai o trimestre do nome do arquivo original
    # Neste exemplo, estamos considerando o segundo número após o hífen como o trimestre
    quarter = file_name.split('-')[1].split('_')[0]

    # Renomeia o arquivo para o formato desejado
    new_file_name = f'{year}-Q{quarter}.parquet'

    # Renomeia o arquivo

    os.rename(file_path, os.path.join(new_file_name))