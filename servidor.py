from xmlrpc.server import SimpleXMLRPCServer
from jogo import Jogo


jogo = Jogo()

#cria o servidor e registra as funções do jogo nele
#necessário um terminal para rodar o servidor e outro para rodar o cliente
server = SimpleXMLRPCServer(("localhost", 9876))

server.register_function(jogo.iniciar_jogo, "iniciar_jogo")
server.register_function(jogo.tentar_palavra, "tentar_palavra")
server.register_function(jogo.pedir_dica, "pedir_dica")
server.register_function(jogo.desistir, "desistir")

print("Servidor iniciado em localhost:9876")

server.serve_forever()