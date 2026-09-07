from PyPDF2 import PdfReader
import nltk
from nltk import FreqDist
import unicodedata
from safetensors.numpy import load_file
import random
import math
import stanza
#stanza.download("pt")
pln = stanza.Pipeline("pt")
import json
import numpy as np
import os

class Processamento():

    def fazer_dowloads(): # executar somente na primeira vez
        nltk.download('punkt')
        nltk.download('punkt_tab')
        
    def ler_pdf(caminho):
        leitor = PdfReader(caminho)

        texto = ""

        for pagina in leitor.pages[5:]:
            texto += pagina.extract_text() + "\n"

        return texto

    def remover_acentos(tokens):
        tokens_sem_acentos = []

        for token in tokens:
            token = unicodedata.normalize("NFD", token)
            token = "".join(
                caractere
                for caractere in token
                if unicodedata.category(caractere) != "Mn"
            )

            tokens_sem_acentos.append(token)

        return tokens_sem_acentos

    def tokenizacao(caminho):
        tokens = nltk.word_tokenize(caminho, language='portuguese')
        tokens = [token.lower() for token in tokens]

        return tokens

    def tokenizacao_lematizacao(texto):
        doc = pln(texto)

        lemas = []

        for senteca in doc.sentences:
            for palavra in senteca.words:
                lemas.append(palavra.lemma)

        return lemas

    def remocao_stopwords(texto):
        lista_stopwords = [
            "a", "à", "ao", "aos", "as", "às",
        "até", "com", "como",
        "da", "das", "de", "dela", "dele", "do", "dos",
        "e", "ela", "elas", "ele", "eles", "em", "entre",
        "era", "essa", "essas", "esse", "esses",
        "esta", "estas", "este", "estes",
        "eu",
        "foi", "foram",
        "há",
        "isso", "isto",
        "já",
        "lhe", "lhes",
        "mais", "mas", "me", "mesmo",
        "na", "nas", "não", "nem", "no", "nos", "nós",
        "o", "os", "ou",
        "para", "pela", "pelas", "pelo", "pelos", "por",
        "qual", "quando", "que", "quem",
        "se", "sem", "ser", "seu", "sua",
        "também", "te", "tem", "têm",
        "um", "uma", "uns", "umas",
        ".", ",", ";", ":", "!", "?", 
        "(", ")", "[", "]", "{", "}",
        "\"", "'", "“", "”", "‘", "’",
        "-", "–", "—", "...",
        "é", "-se", "-lhe", "d.", "''", "nada", "tão", "ainda", "só", "depois", "outro",
        "porque", "por que", "estar", "estava", "estando", "disse", "tudo", "eram", "foi", "foram", "todos",
        "ter", "tido", "tinha", "tinham", "outra", "um", "uma", "dois", "duas", "pode", "podia", "mas", "mais",
        "menos", "coisa", "ia", "fora", "agora", "diz", "disse", "dizia", "seu", "seus", "logo",
        "assim", "outros", "outras", "toda", "fosse", "muito", "-lo", "ficou", "ver", "ate", "ai", "gozo", "vao", "vai",
        "4º", "pina", "catao", "-nos", "-los", "ve", "mucama", "mudou", "dada", "vos", "gil", "pediam", "haver",
        "alumiou", "quis", "tamanha", "vice-rei", "-as", "-os", "pos", "1", "2", "3", "4", "5", "d", "tanto", "sentiu",
        "ora", "nele", "deste", "ha", "-lhes", "tantos", "quanto", "ja", "sao", "si", "dar-lhes", "tomasse",
        "nosso", "nossos", "nossa", "nossas", "orates", "-o", "aquela", "pois", "portanto", "por que", "porque",
        "caucus", "propria", "proprio", "entao", "tambem", "sempre", "nunca", "enfim", "quase", "daqueles", 
        "aqueles", "tal", "he"
        ]

        texto_filtrado = []

        for token in texto:
            if token not in lista_stopwords:
                texto_filtrado.append(token)

        return texto_filtrado

    def contagem_filtragem_frequencia(texto):
        frequencia = dict(FreqDist(texto))

        f_min = 2
        f_max = 40

        vocabulario = {}

        for palavra, quantidade in frequencia.items():
            if f_min <= quantidade <= f_max:
                vocabulario[palavra] = quantidade

        return vocabulario

    def carregar_embedding():

        dados = load_file("embedding/embeddings.safetensors")

        vetores = dados["embeddings"]

        with open("embedding/vocab.txt", "r", encoding="utf-8") as arquivo:
            palavras = [linha.strip() for linha in arquivo]

        return palavras, vetores

    def criar_embeddings(vocabulario):

        palavras, vetores = Processamento.carregar_embedding()

        indice = {}

        for i, palavra in enumerate(palavras):
            indice[palavra] = i

        embeddings = {}

        for palavra in vocabulario:
            if palavra in indice:
                embeddings[palavra] = vetores[indice[palavra]]

        return embeddings

    def sorteio_palavra(vocabulario):
        palavra = random.choice(list(vocabulario.keys()))
        return palavra

    def distancia_euclidiana(v1, v2):
        soma = 0

        for i in range(len(v1)):
            soma += (v1[i] - v2[i]) ** 2

        return math.sqrt(soma)

    def calculo_distancias(palavra_sorteada, embeddings):
        resultados = {}

        v_alvo = embeddings[palavra_sorteada]

        for palavra in embeddings:
            if palavra != palavra_sorteada:
                v_palavra = embeddings[palavra]
                d = Processamento.distancia_euclidiana(v_alvo, v_palavra)
                resultados[palavra] = d

        return resultados

    def criacao_ranking(distancias):
        ranking = sorted(distancias.items(), key=lambda x: x[1])

        return ranking

    def salvar_dados(vocabulario, embeddings):
        os.makedirs("dados", exist_ok=True)

        dados_vocabulario = {}
        matriz_embeddings = []

        for indice, palavra in enumerate(embeddings):
            dados_vocabulario[palavra] = {
                "frequencia": vocabulario[palavra],
                "indice": indice
            }

            matriz_embeddings.append(embeddings[palavra])

        with open("dados/vocabulario.json", "w", encoding="utf-8") as arquivo:
            json.dump(
                dados_vocabulario,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

        matriz_embeddings = np.array(matriz_embeddings)

        np.save("dados/embeddings.npy", matriz_embeddings)

    def carregar_dados():
        with open("dados/vocabulario.json", "r", encoding="utf-8") as arquivo:
            vocabulario = json.load(arquivo)

        embeddings = np.load("dados/embeddings.npy")

        return vocabulario, embeddings