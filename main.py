listaDados = []
from datetime import datetime

def lerArquivo():
    arquivo = open('dados.txt', 'r')
    for i in arquivo.readlines():
        cliente = []
        info = i.split("!")
        for j in info:
            cliente.append(j)
        if cliente:
            cliente[3] = float(cliente[3])
            cliente[6] = float(cliente[6])
            extrato = cliente[4].split(",")
            cliente[4] = extrato
            listaDados.append(cliente)

lerArquivo()

def salvarArquivo():
    arquivo = open('dados.txt', 'w')
    for i in listaDados:
        arquivo.write(f"{str(i[0])}!{str(i[1])}!{str(i[2])}!{str(i[3])}!{str(i[4])}!{str(i[5])}!{str(i[6])}\n")

#Função criar novo cliente
def novoCliente():
    cliente = []
    rSocial = input("Razão social: ")
    cliente.append(rSocial)
    cnpj = input("CNPJ: ")
    cliente.append(cnpj)
    tipoConta = input("Tipo de conta (comum / plus): ")
    cliente.append(tipoConta)
    saldo = float(input("Valor inicial da conta: "))
    cliente.append(saldo)
    senha = int(input("Digite sua senha: "))
    extrato = []
    cliente.append(extrato)
    pf = False
    cliente.append(pf)
    valorPF = 0
    cliente.append(valorPF)
    listaDados.append(cliente)
    salvarArquivo()


#Função apagar cliente
def apagaCliente():
    cnpj = input("CNPJ: ")
    for i in range(len(listaDados)):
        if listaDados[i][1] == cnpj:
            print(f"Você está apagando o cliente: {listaDados[i][0]}")
            listaDados.remove(listaDados[i])
            break
    else:
        print("CNPJ não encontrado")
    salvarArquivo()

#Função listar clientes
def listarClientes():
    for i in listaDados:
        print(f"Razão Social: {i[0]} CNPJ: {i[1]} Tipo da Conta: {i[2]} Saldo: {i[3]}")

#Função debitar valor do cliente
def debito():
    data = datetime.now()
    cnpj = input("CNPJ: ")
    senha = int(input("Digite sua senha: "))
    valor = float(input("Valor do débito: "))
    for i in range(len(listaDados)):
        if listaDados[i][1] == cnpj:
            if listaDados[i][2] == "comum":
                saldo = -1000
                taxa = 1.05
            else:
                saldo = -5000
                taxa = 1.03
            if (listaDados[i][3] - (valor*taxa)) < saldo:
                print("Saldo insuficiente")
            else:
                listaDados[i][3] -= (valor*taxa)
                print(f"Novo saldo da conta {listaDados[i][0]}: {listaDados[i][3]}")
                infoExtrato = f"Data: {data.day}/{data.month}/{data.year} {data.hour}:{data.minute}:{data.second} -{valor*taxa} Tarifa: {(valor*(taxa-1)):.2f} Saldo: {listaDados[i][3]}"
                listaDados[i][4].append(infoExtrato)
            break
    else:
        print("CNPJ não encontrado")
    salvarArquivo()

#Função depositar valor pro cliente
def deposito():
    data = datetime.now()
    cnpj = input("CNPJ: ")
    valor = float(input("Valor do depósito: "))
    for i in range(len(listaDados)):
        if listaDados[i][1] == cnpj:
            listaDados[i][3] += valor
            print(f"Novo saldo da conta {listaDados[i][0]}: {listaDados[i][3]}")
            infoExtrato = f"Data: {data.day}/{data.month}/{data.year} {data.hour}:{data.minute}:{data.second} +{valor} Tarifa: 0.00 Saldo: {listaDados[i][3]}"
            listaDados[i][4].append(infoExtrato)
            break
    else:
        print("CNPJ não encontrado")
    salvarArquivo()


#Função mostrar extrato
def extrato():
    cnpj = input("CNPJ: ")
    senha = int(input("Digite sua senha: "))
    for i in listaDados:
        if i[1] == cnpj:
            print(f"Razão Social: {i[0]}")
            print(f"CNPJ: {i[1]}")
            print(f"Conta: {i[2]}")
            for i in i[4]:
                i = i.replace("[","")
                i = i.replace("]", "")
                i = i.replace("'", "")
                print(i)

#Função transferir valor entre contas
def transferenciaContas():
    data = datetime.now()
    pass1 = False
    pass2 = False
    cnpjorigem = input("CNPJ (Origem): ")
    cnpjdestino = input("CNPJ (Destino): ")
    valor = float(input("Valor da transferência: "))
    senhaorigem = int(input("Digite sua senha: "))
    for i in listaDados:
        if i[1] == cnpjorigem:
            contaorigem = i
            if i[2] == "comum":
                saldo = -1000
                taxa = 1.05
            else:
                saldo = -5000
                taxa = 1.03
            c1 = i[1]
            v1 = i[3]
            if (i[3] - (valor*taxa)) < saldo:
                print("Saldo insuficiente")
            else:
                pass1 = True
            break
    else:
        print("CNPJ Não encontrado")
    if pass1 == True:
        for i in listaDados:
            if i[1] == cnpjdestino:
                contadestino = i
                c2 = i[1]
                v2 = i[3]
                pass2 = True
                break
        else:
            print("CNPJ Não encontrado")
    if pass1 and pass2:
        contaorigem[3] -= (valor*taxa)
        contadestino[3] += valor
        print(f"Novo saldo da conta {c1}: {contaorigem[3]}")
        print(f"Novo saldo da conta {c2}: {contadestino[3]}")
        infoExtrato = f"Data: {data.day}/{data.month}/{data.year} {data.hour}:{data.minute}:{data.second} +{valor*taxa} Tarifa: {(valor*(taxa-1)):.2f} Saldo: {contadestino[3]}"
        infoExtrato2 = f"Data: {data.day}/{data.month}/{data.year} {data.hour}:{data.minute}:{data.second} -{valor * taxa} Tarifa: {(valor * (taxa - 1)):.2f} Saldo: {contaorigem[3]}"
        contaorigem[4].append(infoExtrato2)
        contadestino[4].append(infoExtrato)
    salvarArquivo()

#Função operacao livre
def operacaoLivre():
    print("1. Cadastrar novo funcionário")
    print("2. Remover funcionário")
    print("3. Listar funcionários")
    entrada = input("")
    if entrada == "1":
        cnpj = input("CNPJ do funcionário: ")
        valor = int(input("Valor do pagamento mensal: "))
        for i in listaDados:
            if i[1] == cnpj:
                i[5] = 'True'
                i[6] = valor
                break
        else:
            print("CNPJ não encontrado")
    if entrada == "2":
        cnpjremover = input("CNPJ do funcionário: ")
        for i in listaDados:
            if i[1] == cnpjremover:
                i[5] = 'False'
                print("Funcionario removido")
                break
        else:
            print("CNPJ não encontrado")
    if entrada == "3":
        for i in range(len(listaDados)):
            if listaDados[i][5] == 'True':
                print(f"Razão Social: {listaDados[i][0]} Valor do pagamento: {listaDados[i][6]}")
    salvarArquivo()


# Listagem de opções e checagem do input
while True:
    print("1. Novo cliente")
    print("2. Apaga cliente")
    print("3. Listar clientes")
    print("4. Débito")
    print("5. Depósito")
    print("6. Extrato")
    print("7. Transferência entre contas")
    print("8. Pagamento de funcionários")
    print("9. Sair")
    opcao = int(input("Digite uma opção: "))
    if opcao == 1:
        novoCliente()
    elif opcao == 2:
        apagaCliente()
    elif opcao == 3:
        listarClientes()
    elif opcao == 4:
        debito()
    elif opcao == 5:
        deposito()
    elif opcao == 6:
        extrato()
    elif opcao == 7:
        transferenciaContas()
    elif opcao == 8:
        operacaoLivre()
    elif opcao == 9:
        break
    else:
        print("Opção inválida")

