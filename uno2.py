"""
Grupo 01 - Trabalho UNO - Projeto de Teste 2020.2
Jones Martins - DRE: 115149195
Felipe Menescal - DRE: 113282298
Larissa Galeno - DRE: 116083017
Leonardo Gonçalves - DRE: 111337097
"""

import itertools
from collections import deque
from typing import List, TypeVar, Deque, Tuple, Optional
import random

CORES_VALIDAS = ('amarelo', 'azul', 'verde', 'vermelho')

R = TypeVar("R")


class Pilha(Deque[R]):
    def __init__(self, objs):
        super().__init__(objs)
        self.pilha = deque(objs)

    def __len__(self) -> int:
        return len(self.pilha)

    def topo(self) -> R:
        return self.pilha[0]

    def empilhar(self, obj: R):
        copia = self.pilha.copy()
        copia.appendleft(obj)
        return Pilha(copia)

    def desempilhar(self):
        copia = self.pilha.copy()
        return copia.popleft(), Pilha(copia)

    def como_lista(self) -> List[R]:
        return list(self.pilha)


class Carta:
    def __init__(self, cor: str, tipo: str):
        self.cor = cor
        self.tipo = tipo

    def __eq__(self, other):
        return (self.cor, self.tipo) == (other.cor, other.tipo)

    def __repr__(self):
        return f"Carta(cor={self.cor}, tipo={self.tipo})"


def montar_listagem_de_cartas(
        cartas: List[Carta],
        enumerar: bool = False,
) -> str:
    """
    Monta listagem de cartas numerada ou não.
    Exemplos:
        Se lista de cartas estiver vazia:
            *vazio*
        Se enumerar = False
            - Carta('azul', '1');
            - Carta('vermelho', '2');
        Se enumerar = False
            Suas cartas:
            1) Carta('azul', '1');
            2) Carta('vermelho', '2');

    :param cartas: Cartas a listar
    :param enumerar: Numerar a listagem ou não?
    :return: String da listagem de cartas
    """

    if not cartas:
        listagem = '*vazio*'
    else:
        listagem = ''
        for i, carta in enumerate(cartas, start=1):
            inicio_de_linha = '-' if not enumerar else f'{i})'
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
            eh_coringa = carta.cor == '*'
            return cor_bate or tipo_bate or eh_coringa

        selecionadas = [
            carta
            for carta in self.cartas
            if filtro(topo_descarte, carta)
        ]

        return selecionadas

    def comprar(
            self,
            monte_compra: Pilha[Carta],
            monte_descarte: Pilha[Carta],
            quantidade: int
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
                    random.sample(monte_descarte.como_lista(),
                                  len(monte_descarte))
                )
                topo_compra, monte_compra = monte_compra.desempilhar()
                monte_descarte = Pilha([topo_compra])

            carta_comprada, monte_compra = monte_compra.desempilhar()
            self.cartas.append(carta_comprada)

        return monte_compra, monte_descarte

    @staticmethod
    def escolhe_carta_possivel(
            cartas_possiveis: List[Carta]
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

        print('Cartas possíveis')
        listagem_de_cartas = montar_listagem_de_cartas(
            cartas_possiveis,
            enumerar=True
        )
        while idx_carta is None:
            print(listagem_de_cartas)

            idx_carta_str = input(
                f'Selecione a carta [1, {len(cartas_possiveis)}]: '
            )

            eh_decimal = idx_carta_str.isdecimal()
            eh_valor_valido = (
                    idx_carta_str and
                    1 <= int(idx_carta_str) <= len(cartas_possiveis)
            )
            if eh_decimal and eh_valor_valido:
                return cartas_possiveis[int(idx_carta_str) - 1]

    def jogar(self, carta: Carta, monte_descarte: Pilha[Carta]) -> Pilha[Carta]:
        """
        Tira uma carta da mão e coloca no monte de descarte.
        :param carta: Carta selecionada
        :param monte_descarte: Monte de descarte
        """
        self.cartas.remove(carta)
        monte_descarte = monte_descarte.empilhar(carta)
        return monte_descarte

    @staticmethod
    def escolhe_cor_de_coringa():
        """
        Escolhe uma das 4 cores de coringa.
        :return: Cor escolhida
        """
        cor_escolhida = None
        while cor_escolhida not in CORES_VALIDAS:
            cor_escolhida = input('Escolha uma cor: ').lower()
            if cor_escolhida not in CORES_VALIDAS:
                print(
                    'Cor inválida.\n' 
                    f'Escolha uma entre {", ".join(CORES_VALIDAS)}.'
                )
        return cor_escolhida

    def jogar_rodada(self, monte_compra, monte_descarte, topo_esta_ativo):
        topo_descarte = monte_descarte.topo()
        print(f'Topo de descarte: {topo_descarte}')

        cartas_ordenadas = sorted(
            self.cartas,
            key=lambda carta: (carta.cor, carta.tipo)
        )

        print('Suas cartas:')
        print(
            montar_listagem_de_cartas(
                cartas_ordenadas,
                enumerar=True
            )
        )

        cartas_possiveis = self.selecionar(topo_descarte)
        if not cartas_possiveis:
            print('Não há cartas possíveis de se jogar. Vamos comprar uma.')
            monte_compra, monte_descarte = self.comprar(monte_compra,
                                                        monte_descarte,
                                                        quantidade=1)

            # Nova tentativa
            cartas_possiveis = self.selecionar(topo_descarte)

        if not cartas_possiveis:
            print('Carta comprada incompatível.')
            return monte_compra, monte_descarte, topo_esta_ativo
        else:
            print('Cartas possíveis:')
            print(
                montar_listagem_de_cartas(
                    cartas_possiveis,
                    enumerar=True,
                )
            )

            carta_escolhida = self.escolhe_carta_possivel(cartas_possiveis)
            if eh_carta_especial(carta_escolhida):
                if carta_escolhida.tipo in ('coringa', '+4 coringa'):
                    cor_coringa = self.escolhe_cor_de_coringa()
                    carta_escolhida.cor = cor_coringa

                topo_esta_ativo = True

            monte_descarte = self.jogar(carta_escolhida, monte_descarte)

        return monte_compra, monte_descarte, topo_esta_ativo


def eh_carta_especial(carta):
    return carta.tipo in ('inverter', 'pular', '+2', 'coringa', '+4 coringa')


# def selecionar_proximo_jogador(
#         idx_jogador_atual: int, quantidade_jogadores: int,
#         em_sentido_horario: bool
# ) -> int:
#     """
#     Seleciona o próximo jogador de acordo com o sentido.
#     :param idx_jogador_atual: Índice do jogador atual
#     :param quantidade_jogadores: Quantidade de jogadores
#     :param em_sentido_horario: Sentido é horário ou não?
#     :return: Índice do próximo jogador
#     """
#     if em_sentido_horario:
#         return (idx_jogador_atual + 1) % quantidade_jogadores
#     return (idx_jogador_atual - 1) % quantidade_jogadores


# def aplicar_carta(
#         carta: Carta,
#         jogadores: List[Jogador],
#         monte_compra: Pilha[Carta],
#         monte_descarte: Pilha[Carta],
#         idx_jogador_anterior: int,
#         idx_jogador_atual: int,
#         em_sentido_horario: bool,
#         topo_esta_ativo: bool
# ) -> Tuple[Pilha[Carta], Pilha[Carta], int, int, bool, bool]:
#     """
#     Aplica a carta dependendo de seu tipo:
#      - Numeral: Não faz nada.
#      - Inverter: Troca o sentido da ordem dos jogadores.
#      - Pular: Pula uma vez.
#      - Mais dois: Compra duas cartas e passa para o próximo
#      - Mais quatro coringa: Compra quatro cartas e passa para o próximo.
#     :param carta: Carta selecionada
#     :param jogadores: Jogadores da partida
#     :param monte_compra: Monte de compra
#     :param monte_descarte: Monte de descarte
#     :param idx_jogador_anterior: Índice do jogador anterior
#     :param idx_jogador_atual: Índice do jogador atual
#     :param em_sentido_horario: Em sentido horário?
#     :param topo_esta_ativo: A carta do topo de descarte está ativa?
#     :return: (
#         monte de compra, monte de descarte,
#         índice do jogador anterior, índice do jogador atual,
#         em sentido horário?, topo está ativo?
#     )
#     """

#     idx_jogador_anterior = idx_jogador_atual

#     if eh_carta_especial(carta) and topo_esta_ativo:
#         if carta.tipo == 'inverter':
#             em_sentido_horario = not em_sentido_horario
#         elif carta.tipo == 'pular':
#             # Pula duas vezes. O primeiro pulo é aqui.
#             idx_jogador_atual = selecionar_proximo_jogador(
#                 idx_jogador_atual,
#                 quantidade_jogadores=len(jogadores),
#                 em_sentido_horario=em_sentido_horario
#             )
#         elif carta.tipo == 'coringa':
#             pass  # A seleção de cor já aconteceu.
#         elif carta.tipo == '+2':
#             monte_compra, monte_descarte = jogadores[idx_jogador_atual].comprar(
#                 monte_compra,
#                 monte_descarte,
#                 quantidade=2
#             )
#         elif carta.tipo == '+4 coringa':
#             monte_compra, monte_descarte = jogadores[idx_jogador_atual].comprar(
#                 monte_compra,
#                 monte_descarte,
#                 quantidade=4
#             )
#         else:
#             raise ValueError("Tipo de carta desconhecido.")

#         topo_esta_ativo = False

#     idx_jogador_atual = selecionar_proximo_jogador(
#         idx_jogador_atual,
#         quantidade_jogadores=len(jogadores),
#         em_sentido_horario=em_sentido_horario,
#     )

#     return (
#         monte_compra, monte_descarte,
#         idx_jogador_anterior, idx_jogador_atual,
#         em_sentido_horario, topo_esta_ativo
#     )


# def executar_rodada(
#         jogadores: List[Jogador],
#         monte_compra: Pilha[Carta],
#         monte_descarte: Pilha[Carta],
#         idx_jogador_anterior: int,
#         idx_jogador_atual: int,
#         em_sentido_horario: bool,
#         topo_esta_ativo: bool
# ) -> Tuple[Pilha[Carta], Pilha[Carta], int, int, bool, bool, bool]:
#     """
#      - Um jogador é selecionado e ele joga sua carta;
#      - Após jogar sua carta, verificamos se o jogo terminou, foi UNO ou continua.
#      - Após isso aplicamos o efeito da carta. Se for uma carta comum,
#         nós apenas passamos para o próximo jogador.

#     :param jogadores: Jogadores
#     :param monte_compra: Monte de compra
#     :param monte_descarte: Monte de descarte
#     :param idx_jogador_anterior: Índice do jogador anterior
#     :param idx_jogador_atual: Índice do jogador atual
#     :param em_sentido_horario: Sentido de rotação de jogadores
#     :param topo_esta_ativo: A carta do topo de descarte está ativa?
#     :return: (
#         monte de compra, monte de descarte,
#         índice do jogador anterior, índice do próximo jogador,
#         em sentido horário?, topo está ativo?, jogo terminou?
#     )
#     """
#     jogador = jogadores[idx_jogador_atual]

#     monte_compra, monte_descarte, topo_esta_ativo = jogador.jogar_rodada(
#         monte_compra,
#         monte_descarte,
#         topo_esta_ativo
#     )

#     terminou = False

#     if not jogador.cartas:
#         print(f'Jogador {idx_jogador_atual} venceu!')
#         terminou = True

#     elif len(jogador.cartas) == 1:
#         print(f'Jogador {idx_jogador_atual}: UNO!')

#     topo_descarte = monte_descarte.topo()

#     (
#         monte_compra, monte_descarte,
#         idx_jogador_anterior, idx_jogador_atual,
#         em_sentido_horario, topo_esta_ativo
#     ) = aplicar_carta(
#             topo_descarte,
#             jogadores=jogadores,
#             monte_compra=monte_compra,
#             monte_descarte=monte_descarte,
#             idx_jogador_anterior=idx_jogador_anterior,
#             idx_jogador_atual=idx_jogador_atual,
#             em_sentido_horario=em_sentido_horario,
#             topo_esta_ativo=topo_esta_ativo
#     )

#     return (
#         monte_compra, monte_descarte,
#         idx_jogador_anterior, idx_jogador_atual,
#         em_sentido_horario, topo_esta_ativo,
#         terminou
#     )


# def distribui_cartas(
#         cartas: List[Carta],
#         cartas_por_jogador: int,
#         quantidade_de_jogadores: int
# ) -> Tuple[List[Jogador], Pilha[Carta], Pilha[Carta]]:
#     """
#     Cria jogadores, distribuindo cartas para cada um.
#     :param cartas: Cartas do UNO
#     :param cartas_por_jogador: Quantidade de cartas por jogador
#     :param quantidade_de_jogadores: Quantidade de jogadores
#     :return: Jogadores, monte de compra e monte de descarte
#     """
#     cartas_embaralhadas = random.sample(cartas, len(cartas))

#     jogadores = []
#     for _ in range(quantidade_de_jogadores):
#         cartas_jogador = cartas_embaralhadas[:cartas_por_jogador]
#         cartas_embaralhadas = cartas_embaralhadas[cartas_por_jogador:]
#         jogador = Jogador(cartas_jogador)
#         jogadores.append(jogador)

#     monte_compra = Pilha(cartas_embaralhadas)
#     topo_de_compra, monte_compra = monte_compra.desempilhar()

#     monte_descarte = Pilha([topo_de_compra])

#     return jogadores, monte_compra, monte_descarte


# def cria_cartas() -> List[Carta]:
#     """
#     Cria cartas de UNO.
#     :return: Cartas de UNO
#     """
#     cartas_comuns = []
#     for cor in CORES_VALIDAS:
#         for numero in itertools.chain(range(0, 10), range(1, 10)):
#             carta_comum = Carta(cor, str(numero))
#             cartas_comuns.append(carta_comum)

#     pular = [
#         Carta(cor, 'pular')
#         for cor in CORES_VALIDAS
#         for _ in range(2)
#     ]

#     inverter = [
#         Carta(cor, 'inverter')
#         for cor in CORES_VALIDAS
#         for _ in range(2)
#     ]

#     mais_dois = [
#         Carta(cor, '+2')
#         for cor in CORES_VALIDAS
#         for _ in range(2)
#     ]

#     coringas = [
#         Carta('*', 'coringa')
#         for _ in range(4)
#     ]

#     mais_quatro = [
#         Carta('*', '+4 coringa')
#         for _ in range(4)
#     ]

#     cartas_especiais = pular + inverter + mais_dois + coringas + mais_quatro

#     return cartas_comuns + cartas_especiais


# def executar(
#         quantidade_de_jogadores: int,
#         quantidade_inicial_de_cartas_por_jogador: int
# ):
#     """
#     Função principal inicializa todas as variáveis e todas as cartas
#     para executar o jogo automaticamente.
#     """

#     topo_esta_ativo = False

#     cartas = cria_cartas()

#     jogadores, monte_compra, monte_descarte = distribui_cartas(
#         cartas,
#         quantidade_de_jogadores=quantidade_de_jogadores,
#         cartas_por_jogador=quantidade_inicial_de_cartas_por_jogador,
#     )

#     # Inicializando algumas variáveis
#     idx_jogador_anterior = -1  # Só é necessário para jogos de 1 usuário
#     idx_jogador_atual = 0
#     terminou = False
#     em_sentido_horario = True

#     # Se a primeira carta for coringa,
#     # o primeiro jogador deve escolher a cor.
#     if monte_descarte[idx_jogador_atual].cor == '*':
#         print('A 1ª carta é coringa. O 1º jogador deve escolher sua cor:')
#         cor_escolhida = jogadores[idx_jogador_atual].escolhe_cor_de_coringa()
#         monte_descarte[idx_jogador_atual].cor = cor_escolhida

#     while not terminou:
#         print('-' * 20)
#         print(f'Vez do jogador {idx_jogador_atual}')

#         (
#             monte_compra, monte_descarte,
#             idx_jogador_anterior, idx_jogador_atual,
#             em_sentido_horario, topo_esta_ativo,
#             terminou
#         ) = executar_rodada(
#                 jogadores,
#                 monte_compra=monte_compra,
#                 monte_descarte=monte_descarte,
#                 idx_jogador_anterior=idx_jogador_anterior,
#                 idx_jogador_atual=idx_jogador_atual,
#                 topo_esta_ativo=topo_esta_ativo,
#                 em_sentido_horario=em_sentido_horario,
#         )


# if __name__ == '__main__':
#     executar(
#         quantidade_de_jogadores=3,
#         quantidade_inicial_de_cartas_por_jogador=7
#     )
