import os 
import re 

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
nome_arquivo = input("Digite o nome do arquivo sem extensão: ")

if not os.path.isfile(f"{nome_arquivo}.asm"):
    print("Arquivo não existe no repositório.")
    exit()

with open(f"{nome_arquivo}.asm", "r", encoding="utf-8") as f:
    conteudo = f.read()

print("\nConteúdo do arquivo:\n")
print(conteudo)


OPCODES = {
    'lb':   '0000011',
    'sb':   '0100011',
    'ori':  '0010011',
    'beq':  '1100011',
    'sub':  '0110011',
    'and':  '0110011',
    'srl':  '0110011',
    'jal':  '1101111',
    'addi': '0010011',  
}

FUNCT3 = {
    'lb':  '000',
    'sb':  '000',
    'ori': '110',
    'beq': '000',
    'sub': '000',
    'and': '111',
    'srl': '101',
    'addi': '000',
}

FUNCT7 = {
    'sub': '0100000',
    'and': '0000000',
    'srl': '0000000',
}

REGISTROS = {
    'x0': '00000',
    'x1': '00001',
    'x2': '00010',
    'x3': '00011',
    'x4': '00100',
    'x5': '00101',
    'x6': '00110',
    'x7': '00111',
    'x8': '01000',
    'x9': '01001',
    'x10': '01010',
    'x11': '01011',
    'x12': '01100',
    'x13': '01101',
    'x14': '01110',
    'x15': '01111',
    'x16': '10000',
    'x17': '10001',
    'x18': '10010',
    'x19': '10011',
    'x20': '10100',
    'x21': '10101',
    'x22': '10110',
    'x23': '10111',
    'x24': '11000',
    'x25': '11001',
    'x26': '11010',
    'x27': '11011',
    'x28': '11100',
    'x29': '11101',
    'x30': '11110',
    'x31': '11111',
}

def reg_bin(r):
    if r not in REGISTROS:
        raise ValueError(f"Registrador inválido: {r}")
    return REGISTROS[r] #retorna valor do registrador

def im_bin(valor, bits):
    """Transforma o valor em bits pelo complemento de 2"""
    if valor < 0:
        valor = (1 << bits) + valor
    return format(valor, f'0{bits}b')

def montar_r_type(instr, rd, rs1, rs2):
    funct7 = FUNCT7.get(instr, '0000000') #se não tiver instrução devolve 0
    funct3 = FUNCT3[instr]
    opcode = OPCODES[instr]
    return funct7 + reg_bin(rs2) + reg_bin(rs1) + funct3 + reg_bin(rd) + opcode  #Concatena os funct e opcode com o valor de cada registrador correspondente

def montar_i_type(instr, rd, rs1, imm):
    funct3 = FUNCT3[instr]
    opcode = OPCODES[instr]
    imm_bin = im_bin(imm, 12) #transforma a constante em binário
    return imm_bin + reg_bin(rs1) + funct3 + reg_bin(rd) + opcode #monta o tipo, concatenando as strings 

def montar_s_type(instr, rs1, rs2, imm):
    funct3 = FUNCT3[instr]
    opcode = OPCODES[instr]
    imm_bin = im_bin(imm, 12)
    imm_11_5 = imm_bin[:7]  #Pega os bits da posição 11 a 5, logo 7 bits mais significativos
    imm_4_0 = imm_bin[7:]   #Pega os bits da posição 4 a 0, logo 5 bits menos significativos
    return imm_11_5 + reg_bin(rs2) + reg_bin(rs1) + funct3 + imm_4_0 + opcode #monta o tipo concatenando as string

def montar_b_type(instr, rs1, rs2, imm):
    funct3 = FUNCT3[instr]
    opcode = OPCODES[instr]
    imm_bin = im_bin(imm, 13) #os imediatos de tipo b utilizam 13 bits
    imm_12 = imm_bin[0] #extrai o bit mais significativo
    imm_10_5 = imm_bin[2:8] #extrai do bit 2 ao 8
    imm_4_1 = imm_bin[8:12] #extrai do bit 8 ao último (12)
    imm_11 = imm_bin[1] #extrai o segundo bit mais significativo
    return imm_12 + imm_10_5 + reg_bin(rs2) + reg_bin(rs1) + funct3 + imm_4_1 + imm_11 + opcode #monta o tipo concatenando as string

def montar_j_type(instr, rd, imm):
    opcode = OPCODES[instr]
    imm_bin = im_bin(imm, 21) #os imediatos de tipo j utilizam 21 bits
    imm_20 = imm_bin[0]
    imm_10_1 = imm_bin[10:20]
    imm_11 = imm_bin[9]
    imm_19_12 = imm_bin[1:9]
    return imm_20 + imm_19_12 + imm_11 + imm_10_1 + reg_bin(rd) + opcode

def montar_linha(linha, labels=None, pc=0):
    linha = linha.strip() #remove espaços
    if not linha or linha.startswith('#'):
        return None

    tokens = re.split(r'[,\s()]+', linha) #quebra a linha por vírgula ou caracter
    instr = tokens[0] #atribui a instr a instrução da linha quebrada, que é a primeira posição

    if instr == 'sub' or instr == 'and':
        rd, rs1, rs2 = tokens[1], tokens[2], tokens[3]
        return montar_r_type(instr, rd, rs1, rs2)

    elif instr == 'srl':
        rd, rs1, rs2 = tokens[1], tokens[2], tokens[3]
        return montar_r_type(instr, rd, rs1, rs2)

    elif instr == 'srli':
        rd, rs1, shamt = tokens[1], tokens[2], int(tokens[3])
        return montar_i_type('ori', rd, rs1, shamt)  # ou uma função dedicada

    elif instr == 'lb':
        rd = tokens[1]
        offset = int(tokens[2])
        rs1 = tokens[3]
        return montar_i_type(instr, rd, rs1, offset)

    elif instr == 'sb':
        rs2 = tokens[1]
        offset = int(tokens[2])
        rs1 = tokens[3]
        return montar_s_type(instr, rs1, rs2, offset)

    elif instr == 'ori':
        rd, rs1, imm = tokens[1], tokens[2], int(tokens[3])
        return montar_i_type(instr, rd, rs1, imm)

    elif instr == 'addi':
        rd, rs1, imm = tokens[1], tokens[2], int(tokens[3])
        return montar_i_type(instr, rd, rs1, imm)

    elif instr == 'beq':
        rs1, rs2, label = tokens[1], tokens[2], tokens[3]
        if labels and label in labels:
            offset = labels[label] - pc
            imm = offset
            return montar_b_type(instr, rs1, rs2, imm)
        else:
            imm = int(label)
            return montar_b_type(instr, rs1, rs2, imm)

    elif instr == 'jal':
        rd, label = tokens[1], tokens[2]
        if labels and label in labels:
            offset = labels[label] - pc
            return montar_j_type(instr, rd, offset)
        else:
            imm = int(label)
            return montar_j_type(instr, rd, imm)

    elif instr == 'li':
        rd, imm = tokens[1], int(tokens[2])
        return montar_i_type('addi', rd, 'x0', imm)

    else:
        print(f"Instrução desconhecida ou não suportada: {instr}")
        return None

def montar_arquivo(nome_asm):
    with open(nome_asm, "r") as arq:
        linhas = arq.readlines()

    labels = {}
    pc = 0
    for linha in linhas:
        linha_limpa = linha.strip()
        if linha_limpa.endswith(':'):
            label = linha_limpa[:-1]
            labels[label] = pc
        elif linha_limpa:
            pc += 1

    binarios = []
    pc = 0
    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.endswith(':'):
            continue
        cod = montar_linha(linha, labels, pc)
        if cod:
            binarios.append(cod)
            pc += 1

    print("Você quer:")
    print("1 - Arquivo em Binário")
    print("2 - Binário no terminal")
    print("3 - Ambos")
    decisao = int(input("Digite sua decisão: "))
    print("\n")

    if decisao == 3:
        with open("saida.bin", "wb") as saida:
            for b in binarios:
                print(b)
                saida.write(int(b, 2).to_bytes(4, byteorder="little"))
        print("\nArquivo 'saida.bin' gerado e binário no terminal também!")
    elif decisao == 2:
        for b in binarios:
            print(b)
        print("\nBinário acima")
    elif decisao == 1:
        with open("saida.bin", "wb") as saida:
            for b in binarios:
                saida.write(int(b, 2).to_bytes(4, byteorder="little"))
        print("\nMontagem concluída! Arquivo 'saida.bin' gerado.")

if __name__ == "__main__":
    montar_arquivo(f"{nome_arquivo}.asm")