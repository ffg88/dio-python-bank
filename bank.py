# Variáveis da conta
saldo = 0
numero_saques = 0
operacoes = ''

# Constantes do banco
LIMITE_NUM_SAQUE = 3
LIMITE_VAL_SAQUE = 500


def deposito():
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


def saque():
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

def extrato():
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
        print('[q] Sair')
        opcao_menu = input('>>')

        if opcao_menu.lower() == 'd':
            deposito()

        elif opcao_menu.lower() == 's':
            saque()

        elif opcao_menu.lower() == 'e':
            extrato()

        elif opcao_menu.lower() == 'q':
            print('Obrigado por utilizar o PyBank. Até breve.')
            break

        else:
            print('Opção inválida. Por favor, selecione uma opção do menu.\n')


if __name__ == '__main__':
    main()
