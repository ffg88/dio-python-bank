def criar_usuario():
    global usuarios
    print('\nCriação de usuário:')
    cpf = input('Digite o CPF do usuário (somente números): ')
    usuario = filtrar_usuario(cpf)

    if usuario:
        print('Erro. Já existe usuário cadastrado com este CPF.')
        print('Retornando ao menu inicial.\n')
        return
    
    nome = input('Digite o nome completo: ')
    data_nascimento = input('Digite a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Digite o endereço (logradouro, número - bairro - cidade/sigla estado): ')

    usuarios.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})
    print('Operação realizada com sucesso.\n')


def filtrar_usuario(cpf):
    global usuarios
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta():
    global usuarios
    global contas
    print('\nCriação de conta:')
    cpf = input('Digite o CPF do usuário (somente números): ')
    usuario = filtrar_usuario(cpf)

    if not usuario:
        print('Erro. Usuário não encontrado.')
        print('Retornando ao menu inicial.\n')
        return

    num_conta = len(contas) + 1
    contas.append({'agencia': AGENCIA, 'numero_conta': num_conta, "usuario": usuario})
    print('Operação realizada com sucesso.\n')


def listar_contas():
    pass


def depositar():
    global saldo
    global operacoes
    print('\nOperação de depósito:')
    entrada = input('Digite o valor do depósito em R$: ')

    try:
        valor_deposito = float(entrada)
        if valor_deposito > 0:
            saldo += valor_deposito
            operacoes += f'Depósito no valor de R$ {valor_deposito:.2f}\n'
            print('Operação realizada com sucesso.\n')
        else:
            print('A operação falhou. O valor digitado é inválido.')
            print('Retornando ao menu inicial.\n')
    except ValueError:
        print('A operação falhou. O valor digitado é inválido.')
        print('Retornando ao menu inicial.\n')


def sacar():
    global saldo
    global numero_saques
    global operacoes
    print('\nOperação de saque:')
    entrada = input('Digite o valor do saque em R$: ')

    try:
        valor_saque = float(entrada)
        if numero_saques < LIMITE_NUM_SAQUE:
            if valor_saque <= 0:
                print('A operação falhou. O valor digitado é inválido.')
                print('Retornando ao menu inicial.\n')
            elif valor_saque > LIMITE_VAL_SAQUE:
                print('A operação falhou. O valor do saque está acima do limite permitido.')
                print('Retornando ao menu inicial.\n')
            elif valor_saque > saldo:
                print('A operação falhou. Valor do saldo é insuficiente.')
                print('Retornando ao menu inicial.\n')
            else:
                saldo -= valor_saque
                numero_saques += 1
                operacoes += f'Saque no valor de R$ {valor_saque:.2f}\n'
                print('Operação realizada com sucesso.\n')
        else:
            print('A operação falhou. Número de saques diários excedido.')
            print('Retornando ao menu inicial.\n')
    except ValueError:
        print('A operação falhou. O valor digitado é inválido.')
        print('Retornando ao menu inicial.\n')

def exibir_extrato():
    global saldo
    global operacoes
    print('\n================ EXTRATO =================')
    print('Não foram realizadas movimentações.' if not operacoes else operacoes)
    print(f'Saldo: R$ {saldo:.2f}')
    print('==========================================\n')


def main():
    while True:
        print('PyBank - Menu de opções:')
        print('[d] Depositar')
        print('[s] Sacar')
        print('[e] Extrato')
        print('[nc] Cadastrar nova conta')
        print('[lc] Listar contas')
        print('[nu] Cadastrar novo usuario')
        print('[q] Sair')
        opcao_menu = input('>>')

        if opcao_menu.lower() == 'd':
            depositar()

        elif opcao_menu.lower() == 's':
            sacar()

        elif opcao_menu.lower() == 'e':
            exibir_extrato()

        elif opcao_menu.lower() == 'q':
            print('Obrigado por utilizar o PyBank. Até breve.')
            break

        elif opcao_menu.lower() == 'nc':
            criar_conta()

        elif opcao_menu.lower() == 'lc':
            listar_contas()

        elif opcao_menu.lower() == 'nu':
            criar_usuario()

        else:
            print('Opção inválida. Por favor, selecione uma opção do menu.\n')


# Constantes do banco
AGENCIA = '0001'
LIMITE_NUM_SAQUE = 3
LIMITE_VAL_SAQUE = 500

# Variáveis do banco
usuarios = []
contas = []

# Variáveis da conta
saldo = 0
numero_saques = 0
operacoes = ''

if __name__ == '__main__':
    main()
