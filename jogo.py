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

    def pedir_dica(self):

        #faz uma lista de palavras já usadas em dicas ou palpites
        palavras_usadas = (
            [tentativa["palavra"] for tentativa in self.tentativas]
            + [dica["palavra"] for dica in self.dicas]
        )

        #faz uma lista de palavras disponíveis para dica sem serem palavras usadas
        palavras_disponiveis = [
            item
            for item in self.ranking
            if item[0] != self.palavra_sorteada
            and item[0] not in palavras_usadas
        ]

        if not palavras_disponiveis:
            return {
                "sucesso": False,
                "mensagem": "Não há palavras disponíveis para dica."
            }

        #faz uma lista de palavras já usadas novamente
        palavras_conhecidas = self.tentativas + self.dicas

        if not palavras_conhecidas:
            palavra, distancia = random.choice(palavras_disponiveis) #sorteia uma dica dentre palavras não usadas caso seja a primeira dica sem tentativas

        else: 
            #encontra a melhor palavra dentre as já usadas
            melhor_palavra = min(
                palavras_conhecidas,
                key=lambda palavra: palavra["distancia"]
            )

            distancia_melhor_palavra = melhor_palavra["distancia"]

            #as palavras disponíveis para dica são agora entre o alvo e a melhor palavra
            palavras_disponiveis = [
                item
                for item in palavras_disponiveis
                if item[1] < distancia_melhor_palavra
            ]

            if not palavras_disponiveis:
                return {
                    "sucesso": False,
                    "mensagem": "Não há palavras disponíveis entre o melhor resultado e a palavra alvo."
                }

            palavra, distancia = random.choice(palavras_disponiveis) #sorteia a dica

        posicao = self.ranking.index((palavra, distancia)) + 1

        resultado = {
            "sucesso": True,
            "palavra": palavra,
            "posicao": posicao,
            "distancia": distancia
        }

        self.dicas.append(resultado)

        return resultado

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