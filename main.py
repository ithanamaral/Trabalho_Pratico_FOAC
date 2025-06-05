import os 
''' O presente programa visa operar como um Montador da linguagem Assembly para linguagem de máquina(binário) '''

nome_arquivo = input("Digite o nome do arquivo sem sua extensão: ")

if os.path.isfile(f"{nome_arquivo}.txt"): #faz verificação da existência do arquivo .txt no repositório
    print("Arquivo encontrado! Lendo conteúdo...\n")
    with open(f"{nome_arquivo}.txt", "r", encoding="utf-8") as arquivo: #faz leitura do arquivo
        conteudo = arquivo.read()
    print(conteudo)
else:
    print("Arquivo não existe no repositório.")


