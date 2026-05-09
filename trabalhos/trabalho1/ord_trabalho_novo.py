from sys import argv
import os
from struct import pack,unpack,calcsize

formato_lstInvertida = '3i'                      # 3 inteiros de 4 bytes (12 bytes)
sizef_lstInvertida = calcsize(formato_lstInvertida)    # mostra que o tamanho do registro é 12 bytes


def main():
    if len(argv) > 3:
        raise TypeError("Número incorreto de argumentos\nModo de uso: 'programa.py -b' ou 'programa.py -e arquivo.txt'")
    flag = argv[1]
    if flag == "-b":
        le_e_organiza_dados(flag)
    if flag == "-e":
        operacoes(flag, argv[2])
    # if flag == "-c":
    #     compactacao(flag)

def le_e_organiza_dados(flag: str):
    with open('games.dat','rb') as entrada:
        lst_invertida = []
        generos:list[str,int] = []
        publicadoras:list[str,int] = []
        ind_primario:list[tuple[int,int]] = []

        tamanho = entrada.read(2)
        tamanho_int = int.from_bytes(tamanho,'little')
        byoff = 0
        while(tamanho_int != 0):
            reg = entrada.read(tamanho_int)
            reg_str = reg.decode()
            reg_lst = reg_str.split(sep='|')
            id = int(reg_lst[0])
            gen = reg_lst[3]
            pub = reg_lst[4]
            ind_primario.append([id,byoff])
            
            aux = [id,-1,-1]
            lst_invertida.append(aux)
            pos_gen_lst = 1
            pos_pub_lst = 2
            organiza_lst_invertida(id, gen, generos, lst_invertida,pos_gen_lst)
            organiza_lst_invertida(id, pub, publicadoras, lst_invertida,pos_pub_lst)

            byoff += tamanho_int + 2
            entrada.seek(byoff, os.SEEK_SET)
            tamanho = entrada.read(2)
            tamanho_int = int.from_bytes(tamanho,'little')
        
        ind_primario.sort()
        generos.sort()
        publicadoras.sort()

        arq_generos = "genero.ind"
        arq_publicadoras = "publicadora.ind"

        grava_primario(ind_primario)
        grava_secundario(generos,arq_generos)
        grava_secundario(publicadoras,arq_publicadoras)
        grava_lst_invertida(lst_invertida)

        print(generos)
        print("\n", publicadoras)
        print("\n",lst_invertida)
        print("\n", ind_primario)

def organiza_lst_invertida(id:int, id_sec:str, lst_sec: list, lst_invertida: list, r: int):
    if id_sec not in (s[0] for s in lst_sec):
        pos = len(lst_invertida)-1
        lst_sec.append([id_sec,pos])
    
    else:
        for s in lst_sec:
            if s[0] == id_sec: 
                p = s[1]
                if lst_invertida[p][0] > id:
                    for i in range(len(lst_invertida)):
                        if lst_invertida[i][0] == id:
                            s[1] = i
                            lst_invertida[i][r] = p
                else:
                    x = lst_invertida[p][r]

                    if x != -1:
                        y = lst_invertida[x][0]
                        z = lst_invertida[x][r]
                        while(y<id and z != -1):
                            x = z
                            y = lst_invertida[x][0]
                            z = lst_invertida[x][r]
                        if y > id:
                            for i in range(len(lst_invertida)):
                                if lst_invertida[i][0] == id:
                                    for c in range(len(lst_invertida)):
                                        if lst_invertida[c][r] == x:
                                            lst_invertida[c][r] = i
                                    lst_invertida[i][r] = x
                        else:
                            for i in range(len(lst_invertida)):
                                if lst_invertida[i][0] == id:
                                    for c in range(len(lst_invertida)):
                                        if lst_invertida[c][0] == y:
                                            lst_invertida[c][r] = i
                    else:
                        if lst_invertida[p][0] < id:
                            for i in range(len(lst_invertida)):
                                if lst_invertida[i][0] == id:
                                    lst_invertida[p][r] = i

def grava_primario(lista: list):
    with open('primario.ind','wb') as saida:
        cabecalho = len(lista)
        saida.write(cabecalho.to_bytes(4,'little'))
        for n in lista:
            id:int = n[0]
            byoff:int = n[1]
            saida.write(id.to_bytes(4,'little'))
            saida.write(byoff.to_bytes(4,'little'))

def grava_secundario(lista: list, arq_saida: str):
    with open(arq_saida,'wb') as saida:
        cabecalho = len(lista)
        saida.write(cabecalho.to_bytes(4,'little'))
        for n in lista:
            id_sec:str = n[0]
            saida.write(id_sec.encode().ljust(40,b'\0'))
            pos:int = n[1]
            saida.write(pos.to_bytes(4,'little'))

def grava_lst_invertida(lista: list):
    with open('listaInvertida.lst','wb') as saida:
        cabecalho = len(lista)
        saida.write(cabecalho.to_bytes(4,'little'))
        for n in lista:
            id:int = n[0]
            prox_gen:int = n[1]
            prox_pub:int = n[2]

            saida.write(pack(formato_lstInvertida,id,prox_gen,prox_pub))

def operacoes(flag: str, arq_operacoes: str):
    with open('games.dat','r+b') as games:
        lista_ind_pri = []
        lista_generos = []
        lista_publics = []
        lista_invertida = []

        lista_ind_pri, lista_generos, lista_publics, lista_invertida = carrega_indices(lista_ind_pri, lista_generos, lista_publics, lista_invertida)

        with open(arq_operacoes,'r') as entrada:
            for linha in entrada:
                cmd, info = linha.strip().split(' ',1) # strip tira '\n' e split(' ',1) considera o primeiro espaço como separador

                if cmd == "bp":
                    id = int(info)
                    offset = busca_primario(id, lista_ind_pri)
                    games.seek(offset, os.SEEK_SET)
                    tamanho = games.read(2)
                    tamanho_reg = int.from_bytes(tamanho,'little')
                    reg = games.read(tamanho_reg)
                    reg_str = reg.decode()
                    print("\nRegistro de id",id)
                    print(reg_str)

                if cmd == "bs1":
                    genero = info
                    lista_ids = busca_secundario(genero,lista_generos,lista_invertida,1)

                    lista_offsets = []
                    for id in lista_ids:
                        byoff = busca_primario(id, lista_ind_pri)
                        lista_offsets.append(byoff)
                    
                    print("\nRegistros com o gênero",genero," total registros:",len(lista_ids))
                    for offset in lista_offsets:
                        games.seek(offset, os.SEEK_SET)
                        tamanho = games.read(2)
                        tamanho_reg = int.from_bytes(tamanho,'little')
                        reg = games.read(tamanho_reg)
                        reg_str = reg.decode()
                        print(reg_str)

                if cmd == "bs2":
                    publicadora = info
                    lista_ids = busca_secundario(publicadora,lista_publics,lista_invertida,2)

                    lista_offsets = []
                    for id in lista_ids:
                        byoff = busca_primario(id, lista_ind_pri)
                        lista_offsets.append(byoff)
                    
                    print("\nRegistros com publicadora",publicadora," total registros:",len(lista_ids))
                    for offset in lista_offsets:
                        games.seek(offset, os.SEEK_SET)
                        tamanho = games.read(2)
                        tamanho_reg = int.from_bytes(tamanho,'little')
                        reg = games.read(tamanho_reg)
                        reg_str = reg.decode()
                        print(reg_str)

                if cmd == "i":
                    registro = info
                    reg_lst = registro.split(sep='|')
                    id = int(reg_lst[0])
                    byoff = busca_primario(id, lista_ind_pri)
                    if byoff == None:
                        gen = reg_lst[3]
                        pub = reg_lst[4]
                        tamanho = len(registro)
                        games.seek(0, os.SEEK_END)
                        offset = games.tell()
                        lista_ind_pri.append([id,offset])
                        lista_ind_pri.sort()
                        games.write(tamanho.to_bytes(2,'little'))
                        games.write(registro.encode())
                        print("\nInserção do registro de id",id," tamanho =",tamanho,"bytes")
                        aux = (id,-1,-1)
                        lista_invertida.append(list(aux))
                        organiza_lst_invertida(id, gen, lista_generos, lista_invertida, 1)
                        organiza_lst_invertida(id, pub, lista_publics, lista_invertida, 2)
                    else:
                        print("\nEste ID já foi cadastrado.")

                if cmd == "r":
                    id = int(info)
                    byoff = busca_primario(id, lista_ind_pri)
                    if byoff != None:
                        games.seek(byoff, os.SEEK_SET)
                        tamanho = int.from_bytes(games.read(2),'little')
                        remove = '*'
                        games.write(remove.encode())
                        print("\nRemoção do registro de id",id," offset =",byoff)
                        #fazer remoção nos indices 
                    else:
                        print("\nRemoção do registro de id",id)
                        print("Registro não encontrado.")

def carrega_indices(ind_pri:list, generos:list, publicadoras:list, listaInvertida:list):
    with open('primario.ind','rb') as pri:
        total_reg = int.from_bytes(pri.read(4),'little')
        for i in range(total_reg):
            id = int.from_bytes(pri.read(4),'little')
            byoffset = int.from_bytes(pri.read(4),'little')
            ind_pri.append([id,byoffset])
    
    with open('genero.ind','rb') as sec:
        total_reg = int.from_bytes(sec.read(4),'little')
        for i in range(total_reg):
            pos = sec.tell()
            gen = sec.read(40)
            tamanho = 0
            for g in gen:
                if g!=0:
                    tamanho+=1
            sec.seek(pos)
            genero = (sec.read(tamanho)).decode()
            sec.read(40-tamanho)
            primeira_pos = int.from_bytes(sec.read(4),'little')
            generos.append([genero,primeira_pos])
    
    with open('publicadora.ind','rb') as sec:
        total_reg = int.from_bytes(sec.read(4),'little')
        for i in range(total_reg):
            pos = sec.tell()
            pub = sec.read(40)
            tamanho = 0
            for p in pub:
                if p!=0:
                    tamanho+=1
            sec.seek(pos)
            publicadora = (sec.read(tamanho)).decode()
            sec.read(40-tamanho)
            primeira_pos = int.from_bytes(sec.read(4),'little')
            publicadoras.append([publicadora,primeira_pos])
    
    with open('listaInvertida.lst','rb') as lista_inv:
        total_reg = int.from_bytes(lista_inv.read(4),'little')
        for i in range(total_reg):
            reg = lista_inv.read(12)
            tupla = unpack(formato_lstInvertida,reg)
            listaInvertida.append(list(tupla))
    
    return ind_pri, generos, publicadoras, listaInvertida

def busca_primario(id:int, ind_pri:list) -> int | None:
    ultimo = len(ind_pri)
    primeiro = 0

    while primeiro<=ultimo:
        meio = (ultimo+primeiro)//2

        if ind_pri[meio][0] == id:
            return ind_pri[meio][1]
        elif ind_pri[meio][0] > id:
            ultimo = meio - 1
        elif ind_pri[meio][0] < id:
            primeiro = meio + 1
        else:
            return None

def busca_secundario(id_sec:str, lista_sec:list, lista_invertida:list, r:int) -> list:
    lista = []
    ultimo = len(lista_sec)
    primeiro = 0
    teste = False
    primeira_pos = 0

    while primeiro<=ultimo and teste==False:
        meio = (ultimo+primeiro)//2

        if lista_sec[meio][0] == id_sec:
            primeira_pos = lista_sec[meio][1]
            teste = True
        elif lista_sec[meio][0] > id_sec:
            ultimo = meio - 1
        elif lista_sec[meio][0] < id_sec:
            primeiro = meio + 1
        else:
            print("\nNenhum registro foi encontrado.")
            return []
    
    primeiro_id = lista_invertida[primeira_pos][0]
    lista.append(primeiro_id)
    prox_pos = lista_invertida[primeira_pos][r]
    
    while prox_pos != -1:
        id = lista_invertida[prox_pos][0]
        lista.append(id)
        prox_pos = lista_invertida[prox_pos][r]
    return lista



# def compactacao(flag: str):
#     with open('games.dat','rb') as entrada:
#         saida = open('games_novo.dat','wb')
#         tamanho = int.from_bytes(entrada.read(2),'little')
#         while tamanho != 0:
#             ponteiro = entrada.tell()
#             verifica = (entrada.read(1)).decode()
#             if verifica == '*':
#                 entrada.seek(ponteiro)
#                 entrada.read(tamanho)
#             else:
#                 saida.write(tamanho.to_bytes(2,'little'))
#                 entrada.seek(ponteiro)
#                 saida.write(entrada.read(tamanho))
#             tamanho = int.from_bytes(entrada.read(2),'little')
#     saida.close()

if __name__ == "__main__":
    main()
