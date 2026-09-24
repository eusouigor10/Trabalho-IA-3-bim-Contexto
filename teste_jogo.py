from jogo import Jogo


jogo = Jogo()

print("=== INICIANDO JOGO ===")

jogo.iniciar_jogo()

print("Palavra sorteada:", jogo.palavra_sorteada)

print("\n=== VERIFICANDO RANKING ===")

print("Primeira posição:", jogo.ranking[0])

if jogo.ranking[0][0] == jogo.palavra_sorteada:
    print("OK: palavra sorteada está na posição 1.")
else:
    print("ERRO: palavra sorteada não está na posição 1.")


print("\n=== TESTANDO PALAVRA VÁLIDA ===")

palavra_teste = jogo.ranking[1][0]

resultado = jogo.tentar_palavra(palavra_teste)

print(resultado)


print("\n=== TESTANDO PALAVRA INVÁLIDA ===")

resultado = jogo.tentar_palavra("palavrainexistente")

print(resultado)


print("\n=== TESTANDO DICAS ===")

for i in range(5):
    dica = jogo.pedir_dica()
    print(f"Dica {i + 1}:", dica)


print("\n=== VERIFICANDO REPETIÇÃO DAS DICAS ===")

palavras_dicas = [dica["palavra"] for dica in jogo.dicas]

print("Palavras sorteadas como dica:", palavras_dicas)

if len(palavras_dicas) == len(set(palavras_dicas)):
    print("OK: nenhuma dica foi repetida.")
else:
    print("ERRO: houve repetição de dica.")


print("\n=== TESTANDO DESISTÊNCIA ===")

resultado = jogo.desistir()

print("Palavra sorteada:", resultado["palavra_sorteada"])
print("Quantidade de palavras no ranking:", len(resultado["ranking"]))