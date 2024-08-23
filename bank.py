from abc import ABC, abstractmethod
from datetime import date

class Cliente:
    def __init__(self, endereco: str) -> None:
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta: 'Conta', transacao: 'Transacao') -> None:
        transacao.registrar(conta)

    def adicionar_conta(self, conta: 'Conta') -> None:
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str) -> None:
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero: int, cliente: 'Cliente') -> None:
        self._saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()
    
    @property
    def saldo(self) -> float:
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: int) -> 'Conta':
        return cls(numero, cliente)

    def sacar(self, valor: float) -> bool:
        saldo = self.saldo
        
        if valor > 0 and valor <= saldo:
            self._saldo -= valor
            print('Operação realizada com sucesso.\n')
            return True
        
        elif valor > saldo:
            print('Erro. Saldo insuficiente para realizar a operação.\n')

        else:
            print('Erro. Valor inválido.\n')

        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print('Operação realizada com sucesso.\n')
            return True
        
        else:
            print('Erro. Valor inválido.\n')
            return False


class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: 'Cliente', limite=500, limite_saques=3) -> None:
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__]
        )

        if valor > self.limite:
            print('Erro. Limite de valor por saque excedido.\n')

        elif numero_saques >= self.limite_saques:
            print('Erro. Número de saques diários excedidos.\n')

        else:
            return super().sacar(valor)

        return False

    def __str__(self) -> str:
        return f'Agência: {self.agencia}\nConta: {self.numero}\nTitular: {self.cliente.nome}\nCPF Cliente: {self.cliente.cpf}'
    

class Historico:
    def __init__(self) -> None:
        self._transacoes = []

    @property
    def transacoes(self) -> list:
        return self._transacoes

    def adicionar_transacao(self, transacao: 'Transacao') -> None:
        self._transacoes.append({
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': date.today().strftime('%d/%m/%Y'),
            })


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> None:
        pass
    
    @classmethod
    @abstractmethod
    def registrar(self, conta: 'Conta') -> None:
        pass


class Saque(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: 'Conta') -> None:
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor: float) -> None:
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: 'Conta') -> None:
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def filtrar_cliente(cpf: str, clientes: list) -> Cliente | None:
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente: 'Cliente') -> Conta | None:
    if not cliente.contas:
        print('Erro. O cliente indicado não possui conta registrada.\n')
        return

    return cliente.contas[0]


def depositar(clientes: list) -> None:
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Erro. Cliente não encontrado.\n')
        return

    valor = float(input('Digite o valor do depósito em R$: '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes: list) -> None:
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Erro. Cliente não encontrado.\n')
        return

    valor = float(input('Digite o valor do saque em R$: '))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes: list) -> None:
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Erro. Cliente não encontrado.\n')
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print('\n================ EXTRATO =================')
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'Não foram realizadas movimentações.'
    else:
        for transacao in transacoes:
            extrato += f'\n{transacao['tipo']}: R$ {transacao['valor']:.2f}'

    print(extrato)
    print(f'\nSaldo: R$ {conta.saldo:.2f}\n')
    print('==========================================\n')


def criar_cliente(clientes: list) -> None:
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('Erro. Cliente já registrado.\n')
        return

    nome = input('Digite o nome completo: ')
    data_nascimento = input('Digite a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Digite o endereço (logradouro, número - bairro - cidade/sigla estado): ')

    cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)

    clientes.append(cliente)

    print('Cliente cadastrado com sucesso.\n')


def criar_conta(clientes: list, contas: list) -> None:
    cpf = input('Digite o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Erro. Cliente não encontrado.\n')
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('Conta criada com sucesso.\n')


def listar_contas(contas: list) -> None:
    if not contas:
        print('Não foram encontradas contas cadastradas.\n')
    for conta in contas:
        print("=" * 42)
        print(str(conta) + '\n')


def main() -> None:
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
            depositar(clientes)

        elif opcao_menu.lower() == 's':
            sacar(clientes)

        elif opcao_menu.lower() == 'e':
            exibir_extrato(clientes)

        elif opcao_menu.lower() == 'q':
            print('Obrigado por utilizar o PyBank. Até breve.')
            break

        elif opcao_menu.lower() == 'nc':
            criar_conta(clientes, contas)

        elif opcao_menu.lower() == 'lc':
            listar_contas(contas)

        elif opcao_menu.lower() == 'nu':
            criar_cliente(clientes)

        else:
            print('Opção inválida. Por favor, selecione uma opção do menu.\n')


clientes = []
contas = []


if __name__ == '__main__':
    main()
