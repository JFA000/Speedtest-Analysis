import pandas as pd
import geopandas as gpd
import folium
from shapely import wkt
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_and_process_data(file_names):
    dfs = []
    for file_name in file_names:
        logging.info(f'Carregando dados do arquivo: {file_name}')
        df = pd.read_parquet(file_name)
        df['geometry'] = df['tile'].apply(wkt.loads)
        df['quarter'] = file_name.split('-')[1]  # Assumindo que o nome do arquivo contém o trimestre
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df

def perform_spatial_join(df_geo, distritos_sp):
    logging.info('Realizando join espacial')
    return gpd.sjoin(df_geo, distritos_sp, how="inner", predicate='intersects')

def calculate_mean_speed(join_sp):
    logging.info('Calculando velocidade média por município e por trimestre')
    return join_sp.groupby(['NM_MUN', 'quarter'])['avg_d_kbps'].mean().reset_index()

def add_choropleth_layer(m, data, name, column, legend_name):
    folium.Choropleth(
        geo_data=data.__geo_interface__,
        name=name,
        data=data,
        columns=['NM_MUN', column],
        key_on='feature.properties.NM_MUN',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=legend_name
    ).add_to(m)

def main():
    file_names = ["2023-Q1.parquet", "2023-Q2.parquet", "2023-Q3.parquet", "2023-Q4.parquet"]
    shapefile_path = 'SP_Municipios_2022.zip'
    output_excel_mean_speed = "media_velocidade_por_municipio.xlsx"
    
    # Carrega dados de múltiplos trimestres
    df_geo = load_and_process_data(file_names)
    
    # Carrega shapefile
    logging.info(f'Carregando shapefile: {shapefile_path}')
    distritos_sp = gpd.read_file(shapefile_path).to_crs(4326)
    
    # Realiza o join espacial
    join_sp = perform_spatial_join(df_geo, distritos_sp)
    
    # Calcula média de velocidade por município e por trimestre
    media_velocidade_sp = calculate_mean_speed(join_sp)
    
    # Salva os resultados em Excel
    media_velocidade_sp_pivot = media_velocidade_sp.pivot(index='NM_MUN', columns='quarter', values='avg_d_kbps').reset_index()
    media_velocidade_sp_pivot.to_excel(output_excel_mean_speed, index=False)
    
    # Cria mapa interativo com camadas para cada trimestre
    m = folium.Map(location=[-23.5505, -46.6333], zoom_start=7)
    
    for quarter in media_velocidade_sp['quarter'].unique():
        quarter_data = media_velocidade_sp[media_velocidade_sp['quarter'] == quarter]
        map_data = distritos_sp.merge(quarter_data, left_on='NM_MUN', right_on='NM_MUN')
        add_choropleth_layer(m, map_data, f'Velocidade Média - {quarter}', 'avg_d_kbps', f'Velocidade Média de Internet (kbps) - {quarter}')
    
    # Calcula a variação na velocidade de internet entre os trimestres
    numeric_columns = media_velocidade_sp_pivot.columns[1:]  # Ignorar a coluna NM_MUN
    media_velocidade_sp_pivot['variation'] = media_velocidade_sp_pivot[numeric_columns].max(axis=1) - media_velocidade_sp_pivot[numeric_columns].min(axis=1)
    
    # Adiciona camada de variação
    variation_data = distritos_sp.merge(media_velocidade_sp_pivot[['NM_MUN', 'variation']], left_on='NM_MUN', right_on='NM_MUN')
    add_choropleth_layer(m, variation_data, 'Variação na Velocidade', 'variation', 'Variação na Velocidade de Internet (kbps)')
    
    # Adiciona controle de camadas
    folium.LayerControl().add_to(m)
    
    # Salva o mapa
    m.save('sao_paulo_heatmap_interactive.html')
    logging.info('Mapa interativo salvo no arquivo: sao_paulo_heatmap_interactive.html')

if __name__ == "__main__":
    main()

