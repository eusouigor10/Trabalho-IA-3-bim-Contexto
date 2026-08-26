from server import *

# server.fazer_dowloads()

texto = server.ler_pdf("O Alienista.pdf")

texto = server.remover_acentos(texto)

texto = server.tokenizacao(texto)

texto = server.remocao_stopwords(texto)

vocabulario = server.contagem_filtragem_frequencia(texto)

embeddings = server.criar_embeddings(vocabulario)

palavra_sorteada = server.sorteio_palavra(vocabulario)

distancias = server.calculo_distancias(palavra_sorteada, embeddings)

print(palavra_sorteada)
print(distancias)