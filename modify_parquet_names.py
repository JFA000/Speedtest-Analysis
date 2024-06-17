import os

# Lista de arquivos baixados
downloaded_files = [
    '2023-01-01_performance_fixed_tiles.parquet',
    '2023-04-01_performance_fixed_tiles.parquet',
    '2023-07-01_performance_fixed_tiles.parquet',
    '2023-10-01_performance_fixed_tiles.parquet',
    '2024-01-01_performance_fixed_tiles.parquet'
]

# Mapeamento de meses para trimestres
month_to_quarter = {
    '01': 'Q01',
    '04': 'Q02',
    '07': 'Q03',
    '10': 'Q04'
}

for file_name in downloaded_files:
    # Constrói o caminho completo para o arquivo
    file_path = os.path.join(file_name)

    # Extrai o ano do nome do arquivo original
    year = file_name.split('-')[0]

    # Extrai o mês do nome do arquivo original
    month = file_name.split('-')[1]

    # Obtém o trimestre correspondente ao mês
    quarter = month_to_quarter[month]

    # Renomeia o arquivo para o formato desejado
    new_file_name = f'{year}-{quarter}.parquet'

    # Renomeia o arquivo
    os.rename(file_path, os.path.join(new_file_name))
    print(f'Arquivo {new_file_name} criado!')