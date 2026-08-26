from PyPDF2 import PdfReader
import nltk
from nltk import FreqDist

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
        "menos", "coisa"
        ]

        texto_filtrado = []

        for token in texto:
            if token not in lista_stopwords:
                texto_filtrado.append(token)

        return texto_filtrado

    def contagem_frequencia(texto):
        frequencia = FreqDist(texto)

        print(frequencia.most_common(20))
