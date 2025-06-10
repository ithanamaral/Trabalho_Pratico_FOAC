import os #para importar arquivos
import re #para seprar os comandos Asssembly

''' O presente programa visa operar como um Montador da linguagem Assembly para linguagem de máquina(binário) '''

print('''
      
███╗░░░███╗░█████╗░███╗░░██╗████████╗░█████╗░██████╗░░█████╗░██████╗░
████╗░████║██╔══██╗████╗░██║╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗
██╔████╔██║██║░░██║██╔██╗██║░░░██║░░░███████║██║░░██║██║░░██║██████╔╝
██║╚██╔╝██║██║░░██║██║╚████║░░░██║░░░██╔══██║██║░░██║██║░░██║██╔══██╗
██║░╚═╝░██║╚█████╔╝██║░╚███║░░░██║░░░██║░░██║██████╔╝╚█████╔╝██║░░██║
╚═╝░░░░░╚═╝░╚════╝░╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝

░█████╗░░██████╗░██████╗███████╗███╗░░░███╗██████╗░██╗░░░░░██╗░░░██╗
██╔══██╗██╔════╝██╔════╝██╔════╝████╗░████║██╔══██╗██║░░░░░╚██╗░██╔╝
███████║╚█████╗░╚█████╗░█████╗░░██╔████╔██║██████╦╝██║░░░░░░╚████╔╝░
██╔══██║░╚═══██╗░╚═══██╗██╔══╝░░██║╚██╔╝██║██╔══██╗██║░░░░░░░╚██╔╝░░
██║░░██║██████╔╝██████╔╝███████╗██║░╚═╝░██║██████╦╝███████╗░░░██║░░░
╚═╝░░╚═╝╚═════╝░╚═════╝░╚══════╝╚═╝░░░░░╚═╝╚═════╝░╚══════╝░░░╚═╝░░░
      ''')


nome_arquivo = input("Digite o nome do arquivo sem sua extensão: ")

if os.path.isfile(f"{nome_arquivo}.asm"): #faz verificação da existência do arquivo .txt no repositório
    print("Exibindo conteúdo do arquivo\n")
    with open(f"{nome_arquivo}.asm", "r", encoding="utf-8") as arquivo: #faz leitura do arquivo
        conteudo = arquivo.read()
    print(conteudo)
else:
    print("Arquivo não existe no repositório.")

# Tabelas de opcodes e functs
OPCODES = {
    'lb':  '100000',
    'sb':  '101000',
    'ori': '001101',
    'beq': '000100',
    'sub': '000000',
    'and': '000000',
    'srl': '000000',
}

FUNCTS = {
    'sub': '100010',
    'and': '100100',
    'srl': '000010',
}

# Registradores 
REGISTROS = {
    '$zero': '00000',
    '$at':   '00001',
    '$v0':   '00010', '$v1': '00011',
    '$a0':   '00100', '$a1': '00101', '$a2': '00110', '$a3': '00111',
    '$t0':   '01000', '$t1': '01001', '$t2': '01010', '$t3': '01011',
    '$t4':   '01100', '$t5': '01101', '$t6': '01110', '$t7': '01111',
    '$s0':   '10000', '$s1': '10001', '$s2': '10010', '$s3': '10011',
    '$s4':   '10100', '$s5': '10101', '$s6': '10110', '$s7': '10111',
    '$t8':   '11000', '$t9': '11001',
    '$k0':   '11010', '$k1': '11011',
    '$gp':   '11100',
    '$sp':   '11101',
    '$fp':   '11110',
    '$ra':   '11111',
}

def reg_bin(reg): #verifica se o registrador selecionado está na lista
    if reg not in REGISTROS:
        raise ValueError(f"Registrador inválido: {reg}")
    return REGISTROS[reg]

def im_bin(valor, bits=16):
    return format((valor & ((1 << bits) - 1)), f'0{bits}b')

def montar_linha(linha):
    linha = linha.strip()
    if not linha or linha.startswith('#'):
        return None

    tokens = re.split(r'[,\s()]+', linha)
    instr = tokens[0]

    if instr in ['sub', 'and']:
        # sub rd, rs, rt
        rd, rs, rt = reg_bin(tokens[1]), reg_bin(tokens[2]), reg_bin(tokens[3])
        opcode = '000000'
        shamt = '00000'
        funct = FUNCTS[instr]
        return opcode + rs + rt + rd + shamt + funct

    elif instr == 'srl':
        # srl rd, rt, shamt
        rd, rt = reg_bin(tokens[1]), reg_bin(tokens[2])
        shamt = im_bin(int(tokens[3]), 5)
        rs = '00000'
        opcode = '000000'
        funct = FUNCTS['srl']
        return opcode + rs + rt + rd + shamt + funct

    elif instr in ['lb', 'sb']:
        # lb rt, offset(rs)
        rt = reg_bin(tokens[1])
        offset = int(tokens[2])
        rs = reg_bin(tokens[3])
        opcode = OPCODES[instr]
        return opcode + rs + rt + im_bin(offset, 16)

    elif instr == 'ori':
        # ori rt, rs, immediate
        rt = reg_bin(tokens[1])
        rs = reg_bin(tokens[2])
        imm = int(tokens[3])
        opcode = OPCODES[instr]
        return opcode + rs + rt + im_bin(imm, 16)

    elif instr == 'beq':
        # beq rs, rt, offset
        rs = reg_bin(tokens[1])
        rt = reg_bin(tokens[2])
        offset = int(tokens[3])  # Para simplificação
        opcode = OPCODES['beq']
        return opcode + rs + rt + im_bin(offset, 16)

    else:
        print(f"Instrução desconhecida: {instr}")
        return None

def montar_arquivo(nome_asm):
    with open(nome_asm, "r") as arq:
        linhas = arq.readlines()

    # 1ª passada – mapear labels
    labels = {}
    pc = 0
    for linha in linhas:
        linha_limpa = linha.strip()
        if linha_limpa.endswith(':'):
            label = linha_limpa[:-1]
            labels[label] = pc
        elif linha_limpa:  # só conta instruções
            pc += 1

    # 2ª passada – montar instruções com labels resolvidos
    binarios = []
    pc = 0
    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.endswith(':'):
            continue

        tokens = re.split(r'[,\s()]+', linha)
        instr = tokens[0]

        if instr == "beq" and not tokens[3].isdigit():
            # Se for label, calcula offset relativo
            rs = reg_bin(tokens[1])
            rt = reg_bin(tokens[2])
            destino = tokens[3]
            offset = labels[destino] - (pc + 1)
            opcode = OPCODES[instr]
            cod = opcode + rs + rt + im_bin(offset, 16)
        else:
            cod = montar_linha(linha)

        if cod:
            binarios.append(cod)
            pc += 1
    print("Você quer:")
    print("1 - Arquivo em Binário")
    print("2 - Binário no terminal")
    print("3 - Ambos")
    decisao= int(input("Digite sua decisão: "))
    print("\n")
    if decisao == 3:
        with open("saida.bin", "wb") as saida:
            for b in binarios:
                print(b)
                saida.write(int(b, 2).to_bytes(4, byteorder="big"))
            print("\nArquivo 'saida.bin' gerado e binário no terminal também !")
    elif decisao == 2:
            for b in binarios:
                print(b)
            print("\nBinário acima")
    elif decisao == 1:
        with open("saida.bin", "wb") as saida:
            for b in binarios:
                saida.write(int(b, 2).to_bytes(4, byteorder="big"))
        print("\nMontagem concluída! Arquivo 'saida.bin' gerado.")

    

if __name__ == "__main__":
    montar_arquivo(f"{nome_arquivo}.asm")