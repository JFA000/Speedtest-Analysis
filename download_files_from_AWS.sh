#!/bin/bash

# Instalar AWS CLI
pip install awscli

# Configurar AWS CLI
aws configure

# Baixar arquivos da Amazon S3
aws s3 cp --no-sign-request s3://ookla-open-data/parquet/performance/type=fixed/year=2023/quarter=1/2023-01-01_performance_fixed_tiles.parquet ./
aws s3 cp --no-sign-request s3://ookla-open-data/parquet/performance/type=fixed/year=2023/quarter=2/2023-04-01_performance_fixed_tiles.parquet ./
aws s3 cp --no-sign-request s3://ookla-open-data/parquet/performance/type=fixed/year=2023/quarter=3/2023-07-01_performance_fixed_tiles.parquet ./
aws s3 cp --no-sign-request s3://ookla-open-data/parquet/performance/type=fixed/year=2023/quarter=4/2023-10-01_performance_fixed_tiles.parquet ./