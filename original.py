"""
Grupo 01 - Trabalho UNO - Projeto de Teste 2020.2
Jones Martins - DRE: 115149195
Felipe Menescal - DRE: 113282298
Larissa Galeno - DRE: 116083017
Leonardo Gonçalves - DRE: 111337097
"""

import itertools
from collections import deque
import typing as T
import random
import pprint
import enum


QTD_CARTAS_INICIAIS = 7
JOGADORES = 1
CORES_VALIDAS = ("amarelo", "azul", "verde", "vermelho")

R = T.TypeVar("R")


class Pilha(T.Deque[R]):
    def __init__(self, objs):
        super().__init__(objs)
        self.pilha = deque(objs)

    def __len__(self) -> int:
        return len(self.pilha)

    def topo(self):
        return self.pilha[0]

    def empilhar(self, obj: R):
        self.pilha.appendleft(obj)

    def desempilhar(self) -> R:
        return self.pilha.popleft()

    def como_lista(self) -> T.List[R]:
        return list(self.pilha)

class Carta:
    def __init__(self, cor: str, tipo: str):
        self.cor = cor
        self.tipo = tipo

    def __repr__(self):
        return f"Carta(cor={self.cor}, tipo={self.tipo})"


class CartaEspecial(Carta):
    def __init__(self, cor: str, tipo: str, esta_ativo: bool = False):
        super().__init__(cor, tipo)
        self.esta_ativo = esta_ativo

    def __repr__(self):
        return f"CartaEspecial(cor={self.cor}, tipo={self.tipo}, esta_ativo={self.esta_ativo})"


class Jogador:
    def __init__(self, cartas: T.List[Carta]):
        self.cartas = cartas

    def selecionar(self, topo_descarte: Carta) -> T.List[Carta]:
        """
        Seleciona as cartas na mão que podem ser jogadas.
        :param topo_descarte: Topo da pilha de descarte.
            É garantido que exista um topo.
        :return: Lista de cartas selecionáveis
        """

        def filtro(topo: Carta, carta: Carta) -> bool:
            """
            Verifica se cor bate ou se o número  bate.
            :param topo: Carta do topo do monte de descarte
            :param carta: Carta da mão para comparação
            :return: Cor é igual, tipo é igual ou é coringa
            """
            cor_bate = topo.cor == carta.cor
            tipo_bate = topo.tipo == carta.tipo
            eh_coringa = carta.cor == "*"
            return cor_bate or tipo_bate or eh_coringa

        selecionadas = [carta for carta in self.cartas if
                        filtro(topo_descarte, carta)]

        return selecionadas

    def comprar(
            self, quantidade: int, monte_compra: List[Carta]
    ):
        """
        Caso eu não consiga selecionar nenhuma carta,
        preciso comprar uma (ou mais).

        :param quantidade: Quantidade de cartas a comprar
        :param monte_compra: Monte de cartas de comprar
        """
        for _ in range(quantidade):
            carta_comprada = monte_compra.pop()
            self.cartas.append(carta_comprada)

        return monte_compra

    @staticmethod
    def escolher_carta_possivel(
            cartas_possiveis: T.List[Carta]
    ) -> T.Optional[Carta]:
        """
        Escolhe uma carta das várias cartas possíveis.
        Retorna None caso não tenham cartas, mas é esperado que se tenha.
        :param cartas_possiveis: Lista de cartas possíveis
        :return: Carta selecionada (ou None)
        """
        if not cartas_possiveis:
            return None

        idx_carta = None
        while idx_carta is None:
            idx_carta_str = input(
                f"Selecione a carta [0, {len(cartas_possiveis) - 1}]: "
            )

            eh_decimal = idx_carta_str.isdecimal()
            eh_valor_valido = idx_carta_str and 0 <= int(idx_carta_str) < len(
                cartas_possiveis
            )
            if eh_decimal and eh_valor_valido:
                return cartas_possiveis[int(idx_carta_str)]

            print(f"Dê um número de 0 a {len(cartas_possiveis) - 1}")

    def jogar(self, carta: Carta, monte_descarte: List[Carta]):
        """
        Tira uma carta da mão e coloca no monte de descarte.
        :param carta: Carta selecionada
        :param monte_descarte: Monte de descarte
        """
        self.cartas.remove(carta)
        monte_descarte.empilhar(carta)

    def escolher_cor_de_coringa(self):
        """
        Escolhe uma das 4 cores de coringa.
        :return: Cor escolhida
        """
        cor_escolhida = None
        while cor_escolhida not in CORES_VALIDAS:
            cor_escolhida = input("Escolha uma cor: ").lower()
            if cor_escolhida not in CORES_VALIDAS:
                print(
                    "Cor inválida.\n" f'Escolha uma entre {", ".join(CORES_VALIDAS)}.'
                )
        return cor_escolhida

    def _jogar(self, monte_compra, monte_descarte):
        """
        Função principal da mão.
        Seleciona uma carta da mão e joga.
        Se não for possível selecionar uma carta da mão,
        compra-se uma nova carta e tenta-se jogá-la novamente.
        :param monte_compra: Monte de compras
        :param monte_descarte: Monte de descarte
        """
        topo_descarte = monte_descarte.topo()
        print(f"Topo de descarte: {topo_descarte}")

        print("Sua mão:")
        pprint.pprint(sorted(self.cartas, key=lambda c: (c.cor, c.tipo)))

        cartas_possiveis = self.selecionar(topo_descarte)
        if not cartas_possiveis:
            print("Não há cartas possíveis de se jogar. Vamos comprar uma.")
            monte_compra, monte_descarte = self.comprar(monte_compra, monte_descarte, quantidade=1)

            # Nova tentativa
            cartas_possiveis = self.selecionar(topo_descarte)
            if not cartas_possiveis:
                print("Carta comprada incompatível.")
                return

        print("Cartas possíveis:")
        pprint.pprint(cartas_possiveis)

        carta_selecionada = self._seleciona_carta_possivel(cartas_possiveis)
        if isinstance(carta_selecionada, CartaEspecial):
            if carta_selecionada.tipo in ("coringa", "+4 coringa"):
                cor_coringa = self.seleciona_cor_de_coringa()
                carta_selecionada.cor = cor_coringa

            carta_selecionada.esta_ativa = True

        self._descartar(carta_selecionada, monte_descarte)
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
    if em_sentido_horario:
        return (idx_jogador_atual + 1) % quantidade_jogadores
    return abs(idx_jogador_atual - 1) % quantidade_jogadores


def aplicar_carta_especial(
    maos: T.List[Mao],
    idx_jogador_anterior: int,
    idx_jogador_atual: int,
    carta_especial: CartaEspecial,
    monte_compra,
    monte_descarte,
    em_sentido_horario: bool,
) -> T.Tuple[int, int, bool]:
    """
    Aplica a carta especial dependendo de seu tipo:
     - Inverter: Troca o sentido da ordem dos jogadores.
     - Pular: Passa para o próximo
     - Mais dois: Compra duas cartas e passa para o próximo
     - Mais quatro coringa: Compra quatro cartas e passa para o próximo.
    :param maos:
    :param idx_jogador_anterior:
    :param idx_jogador_atual:
    :param carta_especial:
    :param monte_compra:
    :param monte_descarte:
    :param em_sentido_horario:
    :return:
    """
    if carta_especial.esta_ativo:
        if carta_especial.tipo == "inverter":
            em_sentido_horario = not em_sentido_horario
        else:
            idx_proximo_jogador = selecionar_proximo_jogador(
                idx_jogador_atual,
                quantidade_jogadores=len(maos),
                em_sentido_horario=em_sentido_horario,
            )
            proximo_jogador = maos[idx_proximo_jogador]

            if carta_especial.tipo == "pular":
                pass

            if carta_especial.tipo == "+2":
                monte_compra, monte_descarte = proximo_jogador.comprar(monte_compra, monte_descarte, quantidade=2)

            if carta_especial.tipo == "+4 coringa":
                monte_compra, monte_descarte = proximo_jogador.comprar(monte_compra, monte_descarte, quantidade=4)
            idx_jogador_anterior = idx_jogador_atual
            idx_jogador_atual = idx_proximo_jogador

        carta_especial.esta_ativo = False

    return idx_jogador_anterior, idx_jogador_atual, em_sentido_horario


def eh_carta_especial(carta: Carta) -> bool:
    return isinstance(carta, CartaEspecial)


def jogar_rodada(
    maos: T.List[Mao],
    monte_compra,
    monte_descarte,
    idx_jogador_anterior: int,
    idx_jogador_atual: int,
    em_sentido_horario: bool,
) -> T.Tuple[int, int, bool, bool]:
    """
     - Um jogador é selecionado e ele joga sua carta;
     - Após jogar sua carta, verificamos se o jogo terminou ou UNO.
     - Caso não seja para ambos, verificamos se a carta jogada foi especial.
     - Dependendo do tipo de carta especial, e se quem jogou antes não for o jogador,
            nós a aplicamos.
     - Independentemente do jogo terminar ou não, nós passamos para o próximo jogador.

    :param maos: Mãos dos jogadores
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
    mao = maos[idx_jogador_atual]
    monte_compra, monte_descarte = mao.jogar(monte_compra, monte_descarte)
    terminou = False

    if not mao.cartas:
        print(f"Jogador {idx_jogador_atual} venceu.")
        terminou = True
    elif len(mao.cartas) == 1:
        print(f"Jogador {idx_jogador_atual}: UNO!")
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
                maos,
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
        quantidade_jogadores=len(maos),
        em_sentido_horario=em_sentido_horario,
    )

    return idx_jogador_anterior, idx_jogador_atual, em_sentido_horario, terminou


def distribui_cartas(
    cartas: T.List[Carta], cartas_por_jogador: int,
    jogadores: int
):
    """
    Cria jogadores, distribuindo cartas para cada um.
    :param cartas: Cartas do UNO
    :param jogadores: Quantidade de jogadores
    :return: Mãos, monte de compra e monte de descarte
    """
    cartas_embaralhadas = random.sample(cartas, len(cartas))

    maos = []
    for _ in range(jogadores):
        cartas_mao = cartas_embaralhadas[:cartas_por_jogador]
        cartas_embaralhadas = cartas_embaralhadas[cartas_por_jogador:]
        mao = Mao(cartas_mao)
        maos.append(mao)

    monte_compra = Pilha(cartas_embaralhadas)
    monte_descarte = Pilha([monte_compra.desempilhar()])

    return maos, monte_compra, monte_descarte


def cria_cartas() -> T.List[Carta]:
    """
    Cria cartas de UNO.
    :return: Cartas de UNO
    """
    cartas_comuns = []
    for cor in CORES_VALIDAS:
        for numero in itertools.chain(range(0, 10), range(1, 10)):
            carta_comum = Carta(cor, str(numero))
            cartas_comuns.append(carta_comum)

    pular = 2 * [
        CartaEspecial("amarelo", "pular"),
        CartaEspecial("azul", "pular"),
        CartaEspecial("verde", "pular"),
        CartaEspecial("vermelho", "pular"),
    ]

    inverter = 2 * [
        CartaEspecial("amarelo", "inverter"),
        CartaEspecial("azul", "inverter"),
        CartaEspecial("verde", "inverter"),
        CartaEspecial("vermelho", "inverter"),
    ]

    mais_dois = 2 * [
        CartaEspecial("amarelo", "+2"),
        CartaEspecial("azul", "+2"),
        CartaEspecial("verde", "+2"),
        CartaEspecial("vermelho", "+2"),
    ]

    coringas = 4 * [CartaEspecial("*", "coringa"), CartaEspecial("*", "+4 coringa")]

    cartas_especiais = pular + inverter + mais_dois + coringas

    return cartas_comuns + cartas_especiais


def main():
    cartas = cria_cartas()
    maos, monte_compra, monte_descarte = distribui_cartas(cartas, QTD_CARTAS_INICIAIS, JOGADORES)

    idx_jogador_anterior = -1
    idx_jogador_atual = 0
    terminou = False
    em_sentido_horario = True

    # Se a primeira carta for coringa,
    # o primeiro jogador deve escolher a cor.
    if monte_descarte[0].cor == "*":
        cor_selecionada = maos[0].seleciona_cor_de_coringa()
        monte_descarte[0].cor = cor_selecionada

    while not terminou:
        print("-" * 20)
        print(f"Vez do jogador {idx_jogador_atual}")

        resultado = jogar_rodada(
            maos,
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


if __name__ == "__main__":
    main()
