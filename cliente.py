from xmlrpc.client import ServerProxy

#cria o cliente, conectando-se ao servidor criado e chama as funções por meio do proxy
#necessário um terminal para rodar o servidor e outro para rodar o cliente
class Cliente:

    def __init__(self):
        self.proxy = ServerProxy("http://localhost:9876")

    def iniciar_jogo(self):
        return self.proxy.iniciar_jogo()

    def tentar_palavra(self, palavra):
        return self.proxy.tentar_palavra(palavra)

    def pedir_dica(self):
        return self.proxy.pedir_dica()

    def desistir(self):
        return self.proxy.desistir()