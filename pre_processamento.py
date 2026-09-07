from processamento import *

texto = Processamento.ler_pdf("O Alienista.pdf")

texto = Processamento.tokenizacao_lematizacao(texto)

texto = Processamento.remover_acentos(texto)

texto = Processamento.remocao_stopwords(texto)

vocabulario = Processamento.contagem_filtragem_frequencia(texto)

embeddings = Processamento.criar_embeddings(vocabulario)

Processamento.salvar_dados(vocabulario, embeddings)