from textwrap import dedent

AGENCIA_PADRAO = "0001"
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500.00

# -------------------- Operações financeiras -------------------- #

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Keyword-only.
    Retorna (saldo, extrato, numero_saques) após tentar o saque.
    """
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    elif valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    return saldo, extrato, numero_saques


def depositar(saldo, valor, extrato, /):
    """
    Positional-only.
    Retorna (saldo, extrato) após tentar o depósito.
    """
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    print("Depósito realizado com sucesso!")
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    """
    Positional + keyword-only.
    """
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato, end="")
    print(f"Saldo: R$ {saldo:.2f}")
    print("=========================================\n")

# -------------------- Usuários e Contas -------------------- #

def limpar_cpf(cpf: str) -> str:
    return "".join(filter(str.isdigit, cpf))


def encontrar_usuario(usuarios, cpf):
    cpf = limpar_cpf(cpf)
    return next((u for u in usuarios if u["cpf"] == cpf), None)


def criar_usuario(usuarios):
    print("\n=== Cadastro de Usuário ===")
    cpf = limpar_cpf(input("CPF (apenas números ou qualquer formato): "))
    if encontrar_usuario(usuarios, cpf):
        print("Já existe usuário com esse CPF.")
        return

    nome = input("Nome completo: ").strip()
    nasc = input("Data de nascimento (dd/mm/aaaa): ").strip()
    logradouro = input("Logradouro: ").strip()
    nro = input("Número: ").strip()
    bairro = input("Bairro: ").strip()
    cidade = input("Cidade: ").strip()
    uf = input("UF: ").strip().upper()

    endereco = f"{logradouro}, {nro} - {bairro} - {cidade}/{uf}"

    usuarios.append({
        "nome": nome,
        "nascimento": nasc,
        "cpf": cpf,
        "endereco": endereco,
    })
    print("Usuário criado com sucesso!")


def criar_conta(agencia, numero_conta, usuarios, contas):
    print("\n=== Abertura de Conta ===")
    cpf = limpar_cpf(input("Informe o CPF do titular: "))
    usuario = encontrar_usuario(usuarios, cpf)
    if not usuario:
        print("Usuário não encontrado. Cadastre o usuário primeiro.")
        return

    conta = {
        "agencia": agencia,
        "numero": numero_conta,
        "usuario": usuario,       # referência ao dict do usuário
        "saldo": 0.0,
        "extrato": "",
        "saques": 0
    }
    contas.append(conta)
    print(f"Conta {numero_conta:04d} criada para {usuario['nome']}.")


def listar_contas(contas):
    if not contas:
        print("\nNão há contas cadastradas.\n")
        return
    print("\n=== Contas Cadastradas ===")
    for c in contas:
        print(f"Agência: {c['agencia']}  |  Conta: {c['numero']:04d}  |  Titular: {c['usuario']['nome']}")
    print()


def selecionar_conta(contas):
    if not contas:
        print("Não há contas. Crie uma conta primeiro.")
        return None

    try:
        numero = int(input("Informe o número da conta: "))
    except ValueError:
        print("Número inválido.")
        return None

    conta = next((c for c in contas if c["numero"] == numero), None)
    if not conta:
        print("Conta não encontrada.")
    return conta

# -------------------- UI / Loop principal -------------------- #

def menu():
    return dedent("""
    [nu] Novo usuário
    [nc] Nova conta
    [lc] Listar contas
    [d ] Depositar
    [s ] Sacar
    [e ] Extrato
    [q ] Sair
    => """).strip()


def main():
    usuarios = []
    contas = []
    proximo_numero_conta = 1

    while True:
        opcao = input(menu()).strip().lower()

        if opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            criar_conta(AGENCIA_PADRAO, proximo_numero_conta, usuarios, contas)
            proximo_numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "d":
            conta = selecionar_conta(contas)
            if conta:
                try:
                    valor = float(input("Valor do depósito: R$ "))
                except ValueError:
                    print("Valor inválido.")
                    continue
                conta["saldo"], conta["extrato"] = depositar(conta["saldo"], valor, conta["extrato"])

        elif opcao == "s":
            conta = selecionar_conta(contas)
            if conta:
                try:
                    valor = float(input("Valor do saque: R$ "))
                except ValueError:
                    print("Valor inválido.")
                    continue
                saldo, extrato, saques = sacar(
                    saldo=conta["saldo"],
                    valor=valor,
                    extrato=conta["extrato"],
                    limite=LIMITE_VALOR_SAQUE,
                    numero_saques=conta["saques"],
                    limite_saques=LIMITE_SAQUES,
                )
                conta["saldo"], conta["extrato"], conta["saques"] = saldo, extrato, saques

        elif opcao == "e":
            conta = selecionar_conta(contas)
            if conta:
                exibir_extrato(conta["saldo"], extrato=conta["extrato"])

        elif opcao == "q":
            print("Encerrando. Até logo!")
            break

        else:
            print("Operação inválida, tente novamente.")


if __name__ == "__main__":
    main()
