import time

from processamento import Processamento

import random

class Jogo:

    def __init__(self):
        inicio = time.time()

        self.vocabulario, self.embeddings = Processamento.carregar_dados()

        print("Carregamento:", time.time() - inicio, "segundos")

        self.palavra_sorteada = None
        self.tentativas = []
        self.dicas = []
        self.ranking = []

    def iniciar_jogo(self):
        inicio = time.time()

        self.palavra_sorteada = Processamento.sorteio_palavra(
            self.vocabulario
        )

        print("Sorteio:", time.time() - inicio, "segundos")

        self.tentativas = []
        self.dicas = []

        inicio = time.time()

        distancias = Processamento.calculo_distancias(
            self.palavra_sorteada,
            self.vocabulario,
            self.embeddings
        )

        print("Cálculo das distâncias:", time.time() - inicio, "segundos")

        inicio = time.time()

        self.ranking = Processamento.criacao_ranking(distancias)

        print("Criação do ranking:", time.time() - inicio, "segundos")

        return True

    def tentar_palavra(self, palavra):
        palavra = palavra.lower().strip()

        if palavra not in self.vocabulario:
            return {
                "sucesso": False,
                "mensagem": "Palavra não encontrada no vocabulário."
            }

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

                self.tentativas.append(resultado)

                return resultado

    def pedir_dica(self):
        top_20 = self.ranking[:20]

        palavras_usadas = (
            [tentativa["palavra"] for tentativa in self.tentativas]
            + [dica["palavra"] for dica in self.dicas]
        )

        palavras_disponiveis = [
            item
            for item in top_20
            if item[0] != self.palavra_sorteada
            and item[0] not in palavras_usadas
        ]

        if not palavras_disponiveis:
            return {
                "sucesso": False,
                "mensagem": "Não há mais palavras disponíveis para dica."
            }

        palavra, distancia = random.choice(palavras_disponiveis)

        posicao = self.ranking.index((palavra, distancia)) + 1

        resultado = {
            "sucesso": True,
            "palavra": palavra,
            "posicao": posicao,
            "distancia": distancia
        }

        self.dicas.append(resultado)

        return resultado

    def desistir(self):
        return {
            "palavra_sorteada": self.palavra_sorteada,
            "ranking": self.ranking
        }