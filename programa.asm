lb x1, 0(x0)         # x1 = MEM[0] (suponha que seja 5, por exemplo)
sub x2, x1, x1       # x2 = x1 - x1 = 0
and x3, x1, x1       # x3 = x1 & x1 = x1 (ainda 5)
ori x4, x3, 15       # x4 = x3 | 0x0F => 5 | 15 = 15
srl x5, x4, x2       # x5 = x4 >> 0 => 15 >> 0 = 15
beq x5, x2, igual    # 15 == 0? Não, então não salta
sb x5, 0(x0)         # MEM[0] = 15

igual:
# não faz nada 
