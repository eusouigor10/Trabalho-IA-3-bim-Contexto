from PyPDF2 import PdfReader
import nltk
from nltk import FreqDist
import unicodedata
from safetensors.numpy import load_file
import random
import math

class server():

    def fazer_dowloads(): # executar somente na primeira vez
        nltk.download('punkt')
        nltk.download('punkt_tab')

    def ler_pdf(caminho):
        leitor = PdfReader(caminho)

        texto = ""

        for pagina in leitor.pages[4:]:
            texto += pagina.extract_text() + "\n"

        return texto

    def remover_acentos(texto):
        return ''.join(
            caractere
            for caractere in unicodedata.normalize('NFD', texto)
            if unicodedata.category(caractere) != 'Mn'
        )

    def tokenizacao(caminho):
        tokens = nltk.word_tokenize(caminho, language='portuguese')
        tokens = [token.lower() for token in tokens]

        return tokens

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
        "nosso", "nossos", "nossa", "nossas", "orates", "-o"
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

        palavras, vetores = server.carregar_embedding()

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
                d = server.distancia_euclidiana(v_alvo, v_palavra)
                resultados[palavra] = d

        return resultados

    
