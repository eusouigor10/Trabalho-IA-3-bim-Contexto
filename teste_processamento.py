from processamento import *

# Processamento.fazer_dowloads_nltk()

texto = Processamento.ler_pdf("O Alienista.pdf")

texto = Processamento.tokenizacao_lematizacao(texto)

texto = Processamento.remover_acentos(texto)

texto = Processamento.remocao_stopwords(texto)

vocabulario = Processamento.contagem_filtragem_frequencia(texto)

embeddings = Processamento.criar_embeddings(vocabulario)

palavra_sorteada = Processamento.sorteio_palavra(vocabulario)

distancias = Processamento.calculo_distancias(palavra_sorteada, embeddings)

ranking = Processamento.criacao_ranking(distancias)

print(palavra_sorteada)
print(ranking)