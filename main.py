"""
Grupo 01 - Trabalho UNO - Projeto de Teste 2020.2
Jones Martins - DRE: 115149195
Felipe Menescal - DRE: 113282298
Larissa Galeno - DRE: 116083017
Leonardo Gonçalves - DRE: 111337097
"""

import itertools
from collections import deque, namedtuple
from typing import List, TypeVar, Deque, Tuple, Optional
import random
import pprint
import enum


QTD_CARTAS_INICIAIS = 7
JOGADORES = 3
CORES_VALIDAS = ('amarelo', 'azul', 'verde', 'vermelho')
topo_esta_ativo = False

R = TypeVar("R")


class Pilha(Deque[R]):
    def __init__(self, objs):
        super().__init__(objs)
        self.pilha = deque(objs)

    def __len__(self) -> int:
        return len(self.pilha)

    def topo(self):
        return self.pilha[0]

    # def empilhar(self, obj: R) -> Deque[R]:
    #     copia = self.pilha.copy()
    #     copia.appendleft(obj)
    #     return copia
    def empilhar(self, obj: R):
        self.pilha.appendleft(obj)

    def desempilhar(self) -> R:
        return self.pilha.popleft()

    def como_lista(self) -> List[R]:
        return list(self.pilha)


Carta = namedtuple('Carta', ['cor', 'tipo'])


def monta_listagem_de_cartas(cartas: List[Carta], numerar: bool = False) -> str:
    """
    Monta listagem de cartas.
    Exemplos:
        Se lista de cartas estiver vazia:
            Cartas: *vazio*
        Se numerar = False:
            Cartas:
                - Carta('azul', '1');
                - Carta('vermelho', '2');
        Se numerar = False:
            Cartas:
                1) Carta('azul', '1');
                2) Carta('vermelho', '2');

    :param cartas: Cartas a listar
    :param numerar: Numerar a listagem ou não?
    :return: String da listagem de cartas
    """
    listagem = 'Cartas: '
    if not cartas:
        listagem += '*vazio*'
    else:
        for i, carta in enumerate(cartas, start=1):
            inicio_de_linha = '-' if not numerar else '{i})'
            nova_linha = f'\n\t{inicio_de_linha} {carta};'
            listagem += nova_linha

    return listagem


class Jogador:
    def __init__(self, cartas: List[Carta]):
        self.cartas = cartas

    def selecionar(self, topo_descarte: Carta) -> List[Carta]:
        """
        Seleciona as cartas na mão que podem ser jogadas.
        :param topo_descarte: Topo da pilha de descarte.
            É garantido que exista um topo.
        :return: Lista de cartas selecionáveis
        """

        def filtro(topo: Carta, carta: Carta) -> bool:
            """
            Verifica se cor bate ou se o número bate.
            :param topo: Carta do topo do monte de descarte
            :param carta: Carta da mão para comparação
            :return: Cor é igual, tipo é igual ou é coringa
            """
            cor_bate = topo.cor == carta.cor
            tipo_bate = topo.tipo == carta.tipo
            eh_coringa = carta.cor == "*"
            return cor_bate or tipo_bate or eh_coringa

        selecionadas = [carta for carta in self.cartas if filtro(topo_descarte, carta)]

        return selecionadas

    def comprar(
        self, monte_compra: Pilha[Carta], monte_descarte: Pilha[Carta], quantidade: int
    ):
        """
        Caso eu não consiga selecionar nenhuma carta,
        preciso comprar uma (ou mais).
        :param monte_compra: Monte de cartas de comprar
        :param monte_descarte: Monte de cartas de descarte
        :param quantidade: Quantidade de cartas a comprar
        """
        for _ in range(quantidade):
            
            if not monte_compra:
                print('Não há cartas a comprar. 1 momento...')
                monte_compra = Pilha(
                    random.sample(monte_descarte.como_lista(), len(monte_descarte))
                )
                monte_descarte = Pilha([monte_compra.desempilhar()])
                
            carta_comprada = monte_compra.desempilhar()
            self.cartas.append(carta_comprada)
        return monte_compra, monte_descarte

    def _escolhe_carta_possivel(
        self, cartas_possiveis: List[Carta]
    ) -> Optional[Carta]:
        """
        Escolhe uma carta das várias cartas possíveis.
        Retorna None caso não tenham cartas, mas é esperado que se tenha.
        :param cartas_possiveis: Lista de cartas possíveis
        :return: Carta selecionada (ou None)
        """
        if not cartas_possiveis:
            return None

        idx_carta = None
        listagem_de_cartas = monta_listagem_de_cartas(cartas_possiveis)
        while idx_carta is None:
            print(listagem_de_cartas)

            idx_carta_str = input(
                f'Selecione a carta [1, {len(cartas_possiveis)}]: '
            )

            eh_decimal = idx_carta_str.isdecimal()
            eh_valor_valido = idx_carta_str and 1 <= int(idx_carta_str) <= len(
                cartas_possiveis
            )
            if eh_decimal and eh_valor_valido:
                return cartas_possiveis[int(idx_carta_str) - 1]

    def _descartar(self, carta: Carta, monte_descarte: Pilha[Carta]):
        """
        Tira uma carta da mão e coloca no monte de descarte.
        :param carta: Carta selecionada
        :param monte_descarte: Monte de descarte
        """
        self.cartas.remove(carta)
        return monte_descarte.empilhar(carta)

    def escolhe_cor_de_coringa(self):
        """
        Escolhe uma das 4 cores de coringa.
        :return: Cor escolhida
        """
        cor_escolhida = None
        while cor_escolhida not in CORES_VALIDAS:
            cor_escolhida = input('Escolha uma cor: ').lower()
            if cor_escolhida not in CORES_VALIDAS:
                print(
                    'Cor inválida.\n' f'Escolha uma entre {", ".join(CORES_VALIDAS)}.'
                )
        return cor_escolhida

    def jogar(self, monte_compra: Pilha[Carta], monte_descarte: Pilha[Carta]):
        """
        Função principal da mão.
        Seleciona uma carta da mão e joga.
        Se não for possível selecionar uma carta da mão,
        compra-se uma nova carta e tenta-se jogá-la novamente.
        :param monte_compra: Monte de compras
        :param monte_descarte: Monte de descarte
        """
        global topo_esta_ativo

        topo_descarte = monte_descarte.topo()
        print(f'Topo de descarte: {topo_descarte}')

        print('Sua mão:')
        cartas_ordenadas = sorted(self.cartas)
        pprint.pprint(monta_listagem_de_cartas(cartas_ordenadas))

        cartas_possiveis = self.selecionar(topo_descarte)
        if not cartas_possiveis:
            print('Não há cartas possíveis de se jogar. Vamos comprar uma.')
            monte_compra, monte_descarte = self.comprar(monte_compra, monte_descarte, quantidade=1)

            # Nova tentativa
            cartas_possiveis = self.selecionar(topo_descarte)
            if not cartas_possiveis:
                print('Carta comprada incompatível.')
                return

        print('Cartas possíveis:')
        pprint.pprint(monta_listagem_de_cartas(self.cartas, numerar=True))

        carta_escolhida = self._escolhe_carta_possivel(cartas_possiveis)
        if eh_carta_especial(carta_escolhida):
            if carta_escolhida.tipo in ('coringa', '+4 coringa'):
                cor_coringa = self.escolhe_cor_de_coringa()
                carta_escolhida.cor = cor_coringa

            topo_esta_ativo = True

        self._descartar(carta_escolhida, monte_descarte)
        return monte_compra, monte_descarte

def selecionar_proximo_jogador(
    idx_jogador_atual: int, quantidade_jogadores: int, em_sentido_horario: bool
) -> int:
    """
    Seleciona o próximo jogador de acordo com o sentido.
    :param idx_jogador_atual: Índice do jogador atual
    :param quantidade_jogadores: Quantidade de jogadores
    :param em_sentido_horario: Sentido é horário ou não?
    :return: Índice do próximo jogador
    """
    print("Sentido ", em_sentido_horario)
    if em_sentido_horario:
        return (idx_jogador_atual + 1) % quantidade_jogadores
    return abs(idx_jogador_atual - 1) % quantidade_jogadores


def aplicar_carta_especial(
    jogadores: List[Jogador],
    idx_jogador_anterior: int,
    idx_jogador_atual: int,
    carta_especial: Carta,
    monte_compra: Pilha[Carta],
    monte_descarte: Pilha[Carta],
    em_sentido_horario: bool,
) -> Tuple[int, int, bool]:
    """
    Aplica a carta especial dependendo de seu tipo:
     - Inverter: Troca o sentido da ordem dos jogadores.
     - Pular: Passa para o próximo
     - Mais dois: Compra duas cartas e passa para o próximo
     - Mais quatro coringa: Compra quatro cartas e passa para o próximo.
    :param jogadores: 
    :param idx_jogador_anterior:
    :param idx_jogador_atual:
    :param carta_especial:
    :param monte_compra:
    :param monte_descarte:
    :param em_sentido_horario:
    :return:
    """
    global topo_esta_ativo

    print("Ativo ", topo_esta_ativo)

    if topo_esta_ativo:
        if carta_especial.tipo == 'inverter':
            em_sentido_horario = not em_sentido_horario
        else:
            idx_proximo_jogador = selecionar_proximo_jogador(
                idx_jogador_atual,
                quantidade_jogadores=len(jogadores),
                em_sentido_horario=em_sentido_horario,
            )
            proximo_jogador = jogadores[idx_proximo_jogador]

            if carta_especial.tipo == 'pular':
                pass

            if carta_especial.tipo == '+2':
                monte_compra, monte_descarte = proximo_jogador.comprar(monte_compra, monte_descarte, quantidade=2)

            if carta_especial.tipo == '+4 coringa':
                monte_compra, monte_descarte = proximo_jogador.comprar(monte_compra, monte_descarte, quantidade=4)

            idx_jogador_anterior = idx_jogador_atual
            idx_jogador_atual = idx_proximo_jogador

        topo_esta_ativo = False

    return idx_jogador_anterior, idx_jogador_atual, em_sentido_horario


def eh_carta_especial(carta: Carta) -> bool:
    return carta.tipo in ('inverter', 'pular', '+2', 'coringa', '+4 coringa')


def jogar_rodada(
    jogadores: List[Jogador],
    monte_compra: Pilha[Carta],
    monte_descarte: Pilha[Carta],
    idx_jogador_anterior: int,
    idx_jogador_atual: int,
    em_sentido_horario: bool,
) -> Tuple[int, int, bool, bool]:
    """
     - Um jogador é selecionado e ele joga sua carta;
     - Após jogar sua carta, verificamos se o jogo terminou ou UNO.
     - Caso não seja para ambos, verificamos se a carta jogada foi especial.
     - Dependendo do tipo de carta especial, e se quem jogou antes não for o jogador,
            nós a aplicamos.
     - Independentemente do jogo terminar ou não, nós passamos para o próximo jogador.

    :param jogadores: Jogadores
    :param monte_compra: Monte de compra
    :param monte_descarte: Monte de descarte
    :param idx_jogador_anterior: Índice do jogador anterior
    :param idx_jogador_atual: Índice do jogador atual
    :param em_sentido_horario: Sentido de rotação de jogadores
    :return: (
        Índice do jogador anterior, índice do jogador atual,
        Sentido horário?, Jogo terminou
    )
    """
    jogador = jogadores[idx_jogador_atual]
    monte_compra, monte_descarte = jogador.jogar(monte_compra, monte_descarte)
    terminou = False


    if not jogador.cartas:
        print(f'Jogador {idx_jogador_atual} venceu.')
        terminou = True
    elif len(jogador.cartas) == 1:
        print(f'Jogador {idx_jogador_atual}: UNO!')
    else:
        topo_descarte = monte_descarte.topo()
        if (
            eh_carta_especial(topo_descarte)
            and idx_jogador_anterior != idx_jogador_atual
        ):
            (
                idx_jogador_anterior,
                idx_jogador_atual,
                em_sentido_horario,
            ) = aplicar_carta_especial(
                jogadores,
                idx_jogador_anterior=idx_jogador_anterior,
                idx_jogador_atual=idx_jogador_atual,
                carta_especial=topo_descarte,
                monte_compra=monte_compra,
                monte_descarte=monte_descarte,
                em_sentido_horario=em_sentido_horario,
            )

    idx_jogador_anterior = idx_jogador_atual
    idx_jogador_atual = selecionar_proximo_jogador(
        idx_jogador_atual,
        quantidade_jogadores=len(jogadores),
        em_sentido_horario=em_sentido_horario,
    )

    return idx_jogador_anterior, idx_jogador_atual, em_sentido_horario, terminou


def distribui_cartas(
    cartas: List[Carta], 
    cartas_por_jogador: int,
    quantidade_de_jogadores: int
) -> Tuple[List[Jogador], Pilha[Carta], Pilha[Carta]]:
    """
    Cria jogadores, distribuindo cartas para cada um.
    :param cartas: Cartas do UNO
    :param jogadores: Quantidade de jogadores
    :return: Jogadores, monte de compra e monte de descarte
    """
    cartas_embaralhadas = random.sample(cartas, len(cartas))

    jogadores = []
    for _ in range(quantidade_de_jogadores):
        cartas_jogador = cartas_embaralhadas[:cartas_por_jogador]
        cartas_embaralhadas = cartas_embaralhadas[cartas_por_jogador:]
        jogador = Jogador(cartas_jogador)
        jogadores.append(jogador)

    monte_compra = Pilha(cartas_embaralhadas)
    monte_descarte = Pilha([monte_compra.desempilhar()])

    return jogadores, monte_compra, monte_descarte


def cria_cartas() -> List[Carta]:
    """
    Cria cartas de UNO.
    :return: Cartas de UNO
    """
    cartas_comuns = []
    for cor in CORES_VALIDAS:
        for numero in itertools.chain(range(0, 10), range(1, 10)):
            carta_comum = Carta(cor, str(numero))
            cartas_comuns.append(carta_comum)

    pular = [
        Carta(cor, 'pular')
        for cor in CORES_VALIDAS
        for _ in range(2)
    ]

    inverter = [
        Carta(cor, 'inverter')
        for cor in CORES_VALIDAS
        for _ in range(2)
    ]

    mais_dois = [
        Carta(cor, '+2')
        for cor in CORES_VALIDAS
        for _ in range(2)
    ]

    coringas = [
        Carta('*', 'coringa')
        for _ in range(4)
    ]

    mais_quatro = [
        Carta('*', '+4 coringa')
        for _ in range(4)
    ]

    cartas_especiais = pular + inverter + mais_dois + coringas + mais_quatro

    return cartas_comuns + cartas_especiais


def main():
    cartas = cria_cartas()

    jogadores, monte_compra, monte_descarte = distribui_cartas(
        cartas, 
        cartas_por_jogador=QTD_CARTAS_INICIAIS, 
        quantidade_de_jogadores=JOGADORES
    )

    # Inicializando algumas variáveis
    idx_jogador_anterior = -1
    idx_jogador_atual = 0
    terminou = False
    em_sentido_horario = True

    # Se a primeira carta for coringa,
    # o primeiro jogador deve escolher a cor.
    if monte_descarte[idx_jogador_atual].cor == '*':
        print('A 1ª carta é coringa. O 1º jogador deve escolher sua cor:')
        cor_escolhida = jogadores[idx_jogador_atual].escolhe_cor_de_coringa()
        monte_descarte[idx_jogador_atual] = Carta(
            cor_escolhida, 
            monte_descarte[idx_jogador_atual].tipo
        )

    while not terminou:
        print('-' * 20)
        print(f'Vez do jogador {idx_jogador_atual}')

        resultado = jogar_rodada(
            jogadores,
            monte_compra,
            monte_descarte,
            idx_jogador_anterior,
            idx_jogador_atual,
            em_sentido_horario,
        )

        (
            idx_jogador_anterior,
            idx_jogador_atual,
            em_sentido_horario,
            terminou,
        ) = resultado


if __name__ == '__main__':
    main()
