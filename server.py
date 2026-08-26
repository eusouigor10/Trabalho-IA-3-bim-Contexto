from PyPDF2 import PdfReader
import nltk

def fazer_dowloads(): # executar somente na primeira vez
    nltk.download('punkt')
    nltk.download('punkt_tab')

def ler_livro(caminho):
    leitor = PdfReader(caminho)

    texto = ""

    for pagina in leitor.pages[4:]:
        texto += pagina.extract_text() + "\n"

    return texto

texto = ler_livro("O Alienista.pdf")

# tokenização
tokens = nltk.word_tokenize(texto, language='portuguese')
tokens = [token.lower() for token in tokens]

def remocao_stopwords(tokens):
    lista_stopwords = []
    for token in tokens:


