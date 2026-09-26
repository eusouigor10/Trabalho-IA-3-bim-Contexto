import time

from processamento import Processamento

import random

class Jogo: #classe responável por abstrair a lógica do processamento já feito e criar funções compatíveis com o jogo

    def __init__(self):
        inicio = time.time()

        self.vocabulario, self.embeddings = Processamento.carregar_dados() #carrega os dados pré processados

        self.palavra_sorteada = None
        self.tentativas = []
        self.dicas = []
        self.ranking = []

    def iniciar_jogo(self):

        #sorteia a palavra
        self.palavra_sorteada = Processamento.sorteio_palavra(
            self.vocabulario
        )

        self.tentativas = []
        self.dicas = []

        #calcula as distâncias entre a palavra sorteada e todas as palavras do vocabulário
        distancias = Processamento.calculo_distancias(
            self.palavra_sorteada,
            self.vocabulario,
            self.embeddings
        )

        #cria o ranking
        ranking_bruto = Processamento.criacao_ranking(distancias)
        self.ranking = [(p, float(d)) for p, d in ranking_bruto]

        return True

    #função que recebe a tentativa de palavra
    def tentar_palavra(self, palavra):
        palavra = palavra.lower().strip() #normaliza

        #verifica se ela está no vocabulário
        if palavra not in self.vocabulario:
            return {
                "sucesso": False,
                "mensagem": "Palavra não encontrada no vocabulário."
            }

        #se a palavra está no vocabulário, retorna seu ranking com posição e distância da palavra alvo
        for posicao, (palavra_ranking, distancia) in enumerate(
            self.ranking, start=1
        ):
            if palavra_ranking == palavra:
                resultado = {
                    "sucesso": True,
                    "palavra": palavra,
                    "posicao": posicao,
                    "distancia": distancia,
                    "acertou": palavra == self.palavra_sorteada
                }

                self.tentativas.append(resultado) #adiciona nas tentativas

                return resultado

    def pedir_dica(self):  # função que retorna a próxima dica entre as 20 mais próximas
        top_20 = self.ranking[:20]

        # lista de palavras já usadas em dicas e tentativas
        palavras_usadas = (
            [tentativa["palavra"] for tentativa in self.tentativas]
            + [dica["palavra"] for dica in self.dicas]
        )

        # procura a primeira palavra disponível na ordem do ranking
        for palavra, distancia in top_20:

            if palavra == self.palavra_sorteada:
                continue

            if palavra in palavras_usadas:
                continue

            posicao = self.ranking.index((palavra, distancia)) + 1

            resultado = {
                "sucesso": True,
                "palavra": palavra,
                "posicao": posicao,
                "distancia": distancia
            }

            self.dicas.append(resultado)

            return resultado

        return {
            "sucesso": False,
            "mensagem": "Não há mais palavras disponíveis para dica."
        }

    #função de desistência que retorna a palavra alvo
    def desistir(self):
        # Converte lista de tuplas para lista de dicts (serialização segura via XML-RPC)
        top_ranking = [
            {"posicao": i, "palavra": p, "similaridade": f"{d:.4f}"}
            for i, (p, d) in enumerate(self.ranking[:100], start=1)
        ]
        return {
            "palavra_sorteada": str(self.palavra_sorteada),
            "top_ranking": top_ranking
        }