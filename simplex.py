import numpy as np

# Gera uma matriz vazia com tamanho adequado para variáveis ​​e restrições.
def gen_matrix(var,cons):
    tab = np.zeros((cons+1, var+cons+2))
    return tab

# Verifica a coluna mais à direita em busca de valores negativos ACIMA da última linha. Se existirem valores negativos, outro pivô é necessário.
def next_round_r(table):
    m = min(table[:-1,-1])
    if m>= 0:
        return False
    else:
        return True

# Verifica se a linha inferior, excluindo a coluna final, apresenta valores negativos. Se existirem valores negativos, outro pivô é necessário.
def next_round(table):
    lr = len(table[:,0])
    m = min(table[lr-1,:-1])
    if m>=0:
        return False
    else:
        return True

# Semelhante à função next_round_r, mas retorna o índice de linha do elemento negativo na coluna mais à direita
def find_neg_r(table):
    # lc = numero de colunas, lr = numero de linhas
    lc = len(table[0,:])
    # pesquise cada linha (excluindo a última linha) na coluna final para o valor mínimo.
    m = min(table[:-1,lc-1])
    if m<=0:
        # n = índice de linha da localização m
        n = np.where(table[:-1,lc-1] == m)[0][0]
    else:
        n = None
    return n

#Retorna o índice da coluna do elemento negativo na linha inferior
def find_neg(table):
    lr = len(table[:,0])
    m = min(table[lr-1,:-1])
    if m<=0:
        # n = índice de linha para m
        n = np.where(table[lr-1,:-1] == m)[0][0]
    else:
        n = None
    return n

# Localiza o elemento pivô no tableu para remover o elemento negativo da coluna mais à direita.
def loc_piv_r(table):
        total = []
        # r = índice de linha de entrada negativa
        r = find_neg_r(table)
        # Localiza todos os elementos na linha, r, excluindo a coluna final
        row = table[r,:-1]
        # encontra o valor mínimo na linha (excluindo a última coluna)
        m = min(row)
        # c = índice de coluna para entrada mínima na linha
        c = np.where(row == m)[0][0]
        # todos os elementos na coluna
        col = table[:-1,c]
        # precisa passar por esta coluna para encontrar a menor razão positiva
        for i, b in zip(col,table[:-1,-1]):
            # i não pode ser igual a 0 e b/i deve ser positivo.
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                # espaço reservado para elementos que não atendem aos requisitos acima. Caso contrário, nosso número de índice estaria com defeito.
                total.append(0)
        element = max(total)
        for t in total:
            if t > 0 and t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index,c]
# processo semelhante, retorna um elemento de matriz específico para ser dinamizado.
def loc_piv(table):
    if next_round(table):
        total = []
        n = find_neg(table)
        for i,b in zip(table[:-1,n],table[:-1,-1]):
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                # espaço reservado para elementos que não atendem aos requisitos acima. Caso contrário, nosso número de índice estaria com defeito.
                total.append(0)
        element = max(total)
        for t in total:
            if t > 0 and t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index,n]

# Recebe a entrada de string e retorna uma lista de números a serem organizados no tableu
def convert(eq):
    eq = eq.split(',')
    if 'G' in eq:
        g = eq.index('G')
        del eq[g]
        eq = [float(i)*-1 for i in eq]
        return eq
    if 'L' in eq:
        l = eq.index('L')
        del eq[l]
        eq = [float(i) for i in eq]
        return eq

# A linha final do tabblue em um problema mínimo é o oposto de um problema de maximização, então os elementos são multiplicados por (-1)
def convert_min(table):
    table[-1,:-2] = [-1*i for i in table[-1,:-2]]
    table[-1,-1] = -1*table[-1,-1]
    return table

# gera x1,x2,...xn para o número variável de variáveis.
def gen_var(table):
    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    v = []
    for i in range(var):
        v.append('x'+str(i+1))
    return v

# gira o tableau de forma que os elementos negativos sejam removidos da última linha e da última coluna
def pivot(row,col,table):
    # numero de linhas
    lr = len(table[:,0])
    # numero de colunas
    lc = len(table[0,:])
    t = np.zeros((lr,lc))
    pr = table[row,:]
    if table[row,col]**2>0: #novo
        e = 1/table[row,col]
        r = pr*e
        for i in range(len(table[:,col])):
            k = table[i,:]
            c = table[i,col]
            if list(k) == list(pr):
                continue
            else:
                t[i,:] = list(k-r*c)
        t[row,:] = list(r)
        return t
    else:
        print('Cannot pivot on this element.')

# verifica se há espaço na matriz para adicionar outra restrição
def add_cons(table):
    lr = len(table[:,0])
    # deseja saber SE existem pelo menos 2 linhas de todos os elementos zero
    empty = []
    # iterar através de cada linha
    for i in range(lr):
        total = 0
        for j in table[i,:]:
            # use o valor ao quadrado para que (-x) e (+x) não se anulem
            total += j**2
        if total == 0:
            # anexar zero à lista APENAS se todos os elementos em uma linha forem zero
            empty.append(total)
    # Existem pelo menos 2 linhas com todos os elementos zero se o seguinte for verdadeiro
    if len(empty)>1:
        return True
    else:
        return False

# adiciona uma restrição à matriz
def constrain(table,eq):
    if add_cons(table) == True:
        lc = len(table[0,:])
        lr = len(table[:,0])
        var = lc - lr -1
        # configure o contador para iterar pelo comprimento total das linhas
        j = 0
        while j < lr:
            # Iterar por linha
            row_check = table[j,:]
            # total será a soma das entradas na linha
            total = 0
            # Encontre a primeira linha com todas as 0 entradas
            for i in row_check:
                total += float(i**2)
            if total == 0:
                # Encontramos a primeira linha com todas as entradas zero
                row = row_check
                break
            j +=1

        eq = convert(eq)
        i = 0
        # iterar por todos os termos na função de restrição, excluindo o último
        while i<len(eq)-1:
            # atribuir valores de linha de acordo com a equação
            row[i] = eq[i]
            i +=1
        row[-1] = eq[-1]

        # adicione variável de folga de acordo com a localização no tableau.
        row[var+j] = 1
    else:
        print('Cannot add another constraint.')

# verifica para determinar se uma função objetivo pode ser adicionada à matriz
def add_obj(table):
    lr = len(table[:,0])
    # quero saber SE exatamente uma linha de todos os elementos zero existe
    empty = []
    # iterar através de cada linha
    for i in range(lr):
        total = 0
        for j in table[i,:]:
            # use o valor ao quadrado para que (-x) e (+x) não se anulem
            total += j**2
        if total == 0:
            # anexar zero à lista APENAS se todos os elementos em uma linha forem zero
            empty.append(total)
    # Existe exatamente uma linha com todos os elementos zero se o seguinte for verdadeiro
    if len(empty)==1:
        return True
    else:
        return False

# adiciona a função objetiva à matriz.
def obj(table,eq):
    if add_obj(table)==True:
        eq = [float(i) for i in eq.split(',')]
        lr = len(table[:,0])
        row = table[lr-1,:]
        i = 0
    # iterar por todos os termos na função de restrição, excluindo o último
        while i<len(eq)-1:
            # atribuir valores de linha de acordo com a equação
            row[i] = eq[i]*-1
            i +=1
        row[-2] = 1
        row[-1] = eq[-1]
    else:
        print('You must finish adding constraints before the objective function can be added.')

# resolve o problema de maximização para a solução ótima, retorna o dicionário com as chaves x1,x2...xn e max.
def maxz(table, output='summary'):
    while next_round_r(table)==True:
        table = pivot(loc_piv_r(table)[0],loc_piv_r(table)[1],table)
    while next_round(table)==True:
        table = pivot(loc_piv(table)[0],loc_piv(table)[1],table)

    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    i = 0
    val = {}
    for i in range(var):
        col = table[:,i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc,-1]
        else:
            val[gen_var(table)[i]] = 0
    val['max'] = table[-1,-1]
    for k,v in val.items():
        val[k] = round(v,6)
    if output == 'table':
        return table
    else:
        return val

# resolve problemas de minimização para solução ótima, retorna o dicionário com as chaves x1,x2...xn e min.
def minz(table, output='summary'):
    table = convert_min(table)

    while next_round_r(table)==True:
        table = pivot(loc_piv_r(table)[0],loc_piv_r(table)[1],table)
    while next_round(table)==True:
        table = pivot(loc_piv(table)[0],loc_piv(table)[1],table)

    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    i = 0
    val = {}
    for i in range(var):
        col = table[:,i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc,-1]
        else:
            val[gen_var(table)[i]] = 0
    val['min'] = table[-1,-1]*-1
    for k,v in val.items():
        val[k] = round(v,6)
    if output == 'table':
        return table
    else:
        return val

if __name__ == "__main__":

    m = gen_matrix(5,9)
    constrain(m,'0.7,0.4,0.4,0.6,0.6,L,1200')
    constrain(m,'0.16,0.22,0.32,0.19,0.23,L,460')
    constrain(m,'0.25,0.33,0.33,0.4,0.47,L,650')
    constrain(m,'0.05,0.12,0.09,0.04,0.16,L,170')
    constrain(m,'1,0,0,0,0,G,320')
    constrain(m,'0,1,0,0,0,G,380')
    constrain(m,'0,0,1,0,0,G,450')
    constrain(m,'0,0,0,1,0,G,240')
    constrain(m,'0,0,0,0,1,G,180')
    obj(m,'0.8,0.7,1.15,1.3,0.7,0')
    print(maxz(m))

    m = gen_matrix(5,9)
    constrain(m,'0.7,0.4,0.4,0.6,0.6,L,1200')
    constrain(m,'0.16,0.22,0.32,0.19,0.23,L,460')
    constrain(m,'0.25,0.33,0.33,0.4,0.47,L,650')
    constrain(m,'0.05,0.12,0.09,0.04,0.16,L,170')
    constrain(m,'1,0,0,0,0,G,320')
    constrain(m,'0,1,0,0,0,G,380')
    constrain(m,'0,0,1,0,0,G,450')
    constrain(m,'0,0,0,1,0,G,240')
    constrain(m,'0,0,0,0,1,G,180')
    obj(m,'0.8,0.7,1.15,1.3,0.7,0')
    print(minz(m))
