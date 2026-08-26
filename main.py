from server import *

# server.fazer_dowloads()

texto = server.ler_pdf("O Alienista.pdf")

texto = server.tokenizacao(texto)

texto = server.remocao_stopwords(texto)

server.contagem_frequencia(texto)