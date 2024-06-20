# Instalar e carregar as bibliotecas necessárias
install.packages("readxl")
install.packages("ggplot2")
install.packages("gridExtra")
install.packages("cowplot")
install.packages("dplyr")

library(readxl)
library(ggplot2)
library(gridExtra)
library(cowplot)
library(dplyr)

# Carregar o arquivo Excel
file_path <- "C:\\Users\\gabri\\Downloads\\dados_final_agregados.xlsx"
data <- read_excel(file_path)

# Selecionar apenas as colunas numéricas
numeric_cols <- data %>% select(where(is.numeric))

# Calcular o resumo estatístico incluindo desvio padrão para cada coluna
resumo_list <- lapply(numeric_cols, function(col) {
  data.frame(
    Mínimo = min(col, na.rm = TRUE),
    `1º Quartil` = quantile(col, 0.25, na.rm = TRUE),
    Mediana = median(col, na.rm = TRUE),
    Média = mean(col, na.rm = TRUE),
    `3º Quartil` = quantile(col, 0.75, na.rm = TRUE),
    Máximo = max(col, na.rm = TRUE),
    `Desvio Padrão` = sd(col, na.rm = TRUE)
  )
})

# Combinar todas as colunas resumidas em um único data frame
resumo_df <- do.call(rbind, resumo_list)
rownames(resumo_df) <- colnames(numeric_cols)

# Arredondar os valores para duas casas decimais, exceto para o IDHM (3 casas decimais)
resumo_df <- resumo_df %>% mutate(across(where(is.numeric), round, 2))
resumo_df["IDHM", ] <- format(round(resumo_df["IDHM", ], 3), nsmall = 3)

# Ajustar os nomes das colunas
colnames(resumo_df) <- c("Mínimo", "1º Quartil", "Mediana", "Média", "3º Quartil", "Máximo", "Desvio Padrão")

# Criar a tabela com gridExtra
tabela <- tableGrob(resumo_df)

# Salvar a tabela como uma imagem PNG
png("resumo_estatistico.png", width = 1200, height = 800)
grid.draw(tabela)
dev.off()
