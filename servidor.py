from xmlrpc.server import SimpleXMLRPCServer
from processamento import *

server = SimpleXMLRPCServer(("localhost", 9876))

server.register_function(Processamento.sorteio_palavra, 'sorteio_palavra')
server.register_function(Processamento.distancia_euclidiana, 'distancia_euclidiana')
server.register_function(Processamento.calculo_distancias, 'calculo_distancias')
server.register_function(Processamento.criacao_ranking, 'criacao_ranking')
server.register_function(Processamento.carregar_dados, 'carregar_dados')

server.serve_forever()