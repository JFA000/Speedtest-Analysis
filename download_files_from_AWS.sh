#!/bin/bash

# Instalar AWS CLI - caso necessário
#pip install awscli

# Baixar arquivos da Amazon S3
aws s3 cp --no-sign-request s3://ookla-open-data/parquet/performance/type=fixed/year=2022/quarter=4/2022-10-01_performance_fixed_tiles.parquet ./