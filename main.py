from server import *

# server.fazer_dowloads()

texto = server.ler_pdf("O Alienista.pdf")

texto = server.remover_acentos(texto)

texto = server.tokenizacao(texto)

texto = server.remocao_stopwords(texto)

server.contagem_filtragem_frequencia(texto)