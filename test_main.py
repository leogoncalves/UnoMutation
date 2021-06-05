""""
Grupo 01 - Trabalho UNO - Projeto de Teste 2020.2
Jones Martins - DRE: 115149195
Felipe Menescal - DRE: 113282298
Larissa Galeno - DRE: 116083017
Leonardo Gonçalves - DRE: 111337097
"""
import unittest
from unittest.mock import patch

from main import Carta, CartaEspecial, Mao, Pilha


class TestUno(unittest.TestCase):
    
    # All combinations
    def test_selecionar_CT1(self):
        # CT1
        """
        CT1 = {c1b1, c2b1} = {Carta(“vermelho”, “7”), len(cartas) = 0}
        Resultado esperado: 0 cartas selecionadas
        """
        cartas_iniciais = []
        mao = Mao(cartas_iniciais)
        cartas_selecionadas = mao.selecionar(
            topo_descarte=Carta('vermelho', '7')
        )


        self.assertEqual(len(cartas_selecionadas), 0)

    def test_selecionar_CT2_0(self):
        # CT2
        """
        CT2 = {c1b1, c2b2}
        {Carta(“azul”, “2”), len(cartas) = 1}
        Resultado esperado: 0 ou 1 cartas selecionadas 
        """
        cartas_iniciais = [
          Carta('azul', '7')
        ]
        mao = Mao(cartas_iniciais)
        cartas_selecionadas = mao.selecionar(
            topo_descarte=Carta('azul', '2')
        )
        self.assertEqual(len(cartas_selecionadas), 1)
  
    def test_selecionar_CT2_1(self):
        # CT2
        """
        CT2 = {c1b1, c2b2}
        {Carta(“azul”, “2”), len(cartas) = 1}
        Resultado esperado: 0 ou 1 cartas selecionadas 
        """
        cartas_iniciais = [Carta('vermelho', '5')]
        mao = Mao(cartas_iniciais)
        cartas_selecionadas = mao.selecionar(
            topo_descarte=Carta('azul', '2')
        )
        self.assertEqual(len(cartas_selecionadas), 0)

    def test_selecionar_CT3_0(self):
        # CT3
        """
        CT3 = {c1b1, c2b3}
        {Carta(“verde”, “8”), len(cartas) = 5}
        Resultado esperado: 0 a 5 cartas selecionadas
        """
        cartas_iniciais = [
          Carta('verde', '2'),
          Carta('azul', '9'),
          Carta('vermelho', '5'),
          Carta('amarelo', '1'),
          Carta('verde', '8'),          
          CartaEspecial('vermelho', '+2')
        ]
        mao = Mao(cartas_iniciais)
        cartas_selecionadas = mao.selecionar(
            topo_descarte=Carta('verde', '8')
        )
        self.assertEqual(len(cartas_selecionadas), 2)
    
    def test_selecionar_CT3_1(self):
        # CT3
        """
        CT3 = {c1b1, c2b3}
        {Carta(“verde”, “8”), len(cartas) = 5}
        Resultado esperado: 0 a 5 cartas selecionadas
        """
        cartas_iniciais = [
          Carta('verde', '2'),
          Carta('azul', '9'),
          Carta('vermelho', '5'),
          Carta('amarelo', '1'),
          Carta('verde', '8'),          
          CartaEspecial('verde', 'pular'),          
          CartaEspecial('vermelho', '+2')
        ]
        mao = Mao(cartas_iniciais)
        cartas_selecionadas = mao.selecionar(
            topo_descarte=Carta('verde', '8')
        )
        self.assertEqual(len(cartas_selecionadas), 3)

    def test_selecionar_CT4(self):
        # CT4
        """
        CT4 = {c1b2, c2b1}
        {CartaEspecial(“verde”, “pular”), len(cartas) = 0 }
        Resultado esperado: 0 cartas selecionadas
        """
        cartas_iniciais = []
        mao = Mao(cartas_iniciais)
        cartas_selecionadas = mao.selecionar(
            topo_descarte=CartaEspecial('verde', 'pular')
        )
        self.assertEqual(len(cartas_selecionadas), 0)

    def test_selecionar_CT5(self):
        # CT5
        """
        CT5 = {c1b2, c2b2}
        {CartaEspecial(“vermelho”, “coringa”), len(cartas) = 1}
        Resultado esperado: 0 ou 1 carta selecionada
        """
        cartas_iniciais = [
          Carta('vermelho', '2')
        ]
        mao = Mao(cartas_iniciais)
        cartas_selecionadas = mao.selecionar(
            topo_descarte=CartaEspecial('vermelho', 'coringa')
        )
        self.assertEqual(len(cartas_selecionadas), 1)
    
    def test_selecionar_CT6(self):
        # CT6
        """
          CT6 = {c1b2, c2b3}
          {CartaEspecial(“amarelo”, “inverter”), len(cartas) = 4}
          Resultado esperado: 0 a 4 cartas selecionadas
        """
        cartas_iniciais = [
          Carta('amarelo', '7'),
          CartaEspecial('verde', 'inverter'),
          Carta('azul','3'),
          Carta('vermelho','1')
        ]
        mao = Mao(cartas_iniciais)
        cartas_selecionadas = mao.selecionar(
            topo_descarte=CartaEspecial('amarelo', 'inverter')
        )
        self.assertEqual(len(cartas_selecionadas), 2)
    
    # Pair-wise
    def test_comprar_CT1(self):
        """
        CT1 = {c1b1, c2b1, c3b1, c4b1} 
        {0, len(monte_compra)= 0, len(monte_descarte)= 0, len(cartas) = 0}
        Resultado esperado: len(cartas) = 0; len(monte_compra) = 0; len(monte_descarte) = 0;

        """
        cartas_iniciais = []
        mao = Mao(cartas_iniciais)
        tamanho_cartas_anterior = len(mao.cartas)

        monte_compra = Pilha([])
        tamanho_monte_compra_anterior = len(monte_compra)

        monte_descarte = Pilha([])
        tamanho_monte_descarte_anterior = len(monte_descarte)

        monte_compra, monte_descarte = mao.comprar(
            monte_compra,
            monte_descarte,
            quantidade=0
        )
        tamanho_monte_compra_atual = len(monte_compra)
        tamanho_monte_descarte_atual = len(monte_descarte)
        tamanho_cartas_atual = len(mao.cartas)

        self.assertEqual(
            tamanho_monte_compra_anterior,
            tamanho_monte_compra_atual
        )
        self.assertEqual(
            tamanho_monte_descarte_anterior,
            tamanho_monte_descarte_atual
        )
        self.assertEqual(
            tamanho_cartas_anterior,
            tamanho_cartas_atual
        )
    
    def test_comprar_CT2(self):
        """
        CT2 = {c1b1, c2b2, c3b2, c4b2} 
        {0, len(monte_compra) = 2, len(monte_descarte) = 2, len(cartas) = 2}
        Resultado esperado: len(cartas) = 2; len(monte_compra) = 2; len(monte_descarte) = 2
        """
        cartas_iniciais = [
          Carta('verde', '2'),
          Carta('verde', '8'),          
        ]
        mao = Mao(cartas_iniciais)
        tamanho_cartas_anterior = len(mao.cartas)

        monte_compra = Pilha([
          Carta('amarelo', '7'),
          CartaEspecial('verde', 'inverter'),
        ])
        tamanho_monte_compra_anterior = len(monte_compra)

        monte_descarte = Pilha([
            Carta('verde', '1'),
            Carta('azul', '1')
        ])
        tamanho_monte_descarte_anterior = len(monte_descarte)

        monte_compra, monte_descarte = mao.comprar(
            monte_compra,
            monte_descarte,
            quantidade=0
        )
        tamanho_monte_compra_atual = len(monte_compra)
        tamanho_monte_descarte_atual = len(monte_descarte)
        tamanho_cartas_atual = len(mao.cartas)

        self.assertEqual(
            tamanho_monte_compra_anterior,
            tamanho_monte_compra_atual
        )
        self.assertEqual(
            tamanho_monte_descarte_anterior,
            tamanho_monte_descarte_atual
        )
        self.assertEqual(
            tamanho_cartas_anterior,
            tamanho_cartas_atual
        )
    
    def test_comprar_CT3(self):
        """
        CT3 = {c1b2, c2b1, c3b1, c4b1}
        {2, len(monte_compra)= 0, len(monte_descarte)= 0, len(cartas) = 0}
        Resultado esperado: Inviável (retorna um erro)
        """
        cartas_iniciais = []
        mao = Mao(cartas_iniciais)
        tamanho_cartas_anterior = len(mao.cartas)

        monte_compra = Pilha([])
        tamanho_monte_compra_anterior = len(monte_compra)

        monte_descarte = Pilha([])
        tamanho_monte_descarte_anterior = len(monte_descarte)

        with self.assertRaises(IndexError):
            monte_compra, monte_descarte = mao.comprar(
                monte_compra,
                monte_descarte,
                quantidade=2
            )
    
    def test_comprar_CT4(self):
        """
        CT4 = {c1b2, c2b2, c3b2, c4b2}
        {1, len(monte_compra) = 4, len(monte_descarte)= 0, len(cartas) = 3}
        Resultado esperado: len(monte_compra) = 3; len(monte_descarte) = 0; len(cartas) = 4
        """        
        cartas_iniciais = [
          Carta('verde', '2'),
          Carta('azul', '8'),
          Carta('amarelo', '4')
        ]

        mao = Mao(cartas_iniciais)

        monte_compra = Pilha([
          Carta('verde', '2'),
          Carta('azul', '8'),
          Carta('amarelo', '4'),
          Carta('vermelho', '5')
        ])
        monte_descarte = Pilha([])

        monte_compra, monte_descarte = mao.comprar(
            monte_compra,
            monte_descarte,
            quantidade=1
        )
        tamanho_monte_compra_atual = len(monte_compra)
        tamanho_monte_descarte_atual = len(monte_descarte)
        tamanho_cartas_atual = len(mao.cartas)

        self.assertEqual(
            tamanho_monte_compra_atual,
            3
        )
        self.assertEqual(
            tamanho_monte_descarte_atual,
            0
        )
        self.assertEqual(
            tamanho_cartas_atual,
            4
        )
    
    def test_comprar_CT5(self):
        """
        CT5 = {c1b2, c2b1, c3b2, c4b1} 
        {2, len(monte_compra) = 0, len(monte_descarte) = 3, len(cartas) = 0}
        Resultado esperado: len(cartas) = 2; len(monte_compra) = 0; len(monte_descarte) = 1
        """
        cartas_iniciais = []
        mao = Mao(cartas_iniciais)

        monte_compra = Pilha([])

        monte_descarte = Pilha([
            Carta('azul', '9'),
            Carta('amarelo', '9'),
            Carta('amarelo', '1')
        ])

        monte_compra, monte_descarte = mao.comprar(
            monte_compra,
            monte_descarte,
            quantidade=2
        )
        tamanho_monte_compra_atual = len(monte_compra)
        tamanho_monte_descarte_atual = len(monte_descarte)
        tamanho_cartas_atual = len(mao.cartas)

        self.assertEqual(
            tamanho_monte_compra_atual,
            0
        )
        self.assertEqual(
            tamanho_monte_descarte_atual,
            1
        )
        self.assertEqual(
            tamanho_cartas_atual,
            2
        )
    
    def test_comprar_CT6(self):
        """
        CT6 = {c1b2, c2b2, c3b1, c4b2} 
        {2, len(monte_compra) = 0, len(monte_descarte) = 3, len(cartas) = 4}
        Resultado esperado: len(cartas) = 6; len(monte_compra) = 0; len(monte_descarte) = 1

        """
        cartas_iniciais = [
          Carta('verde', '1'),
          Carta('azul', '0'),
          Carta('amarelo', '5'),
          Carta('verde', '8')
        ]
        mao = Mao(cartas_iniciais)

        monte_compra = Pilha([])

        monte_descarte = Pilha([
            Carta('azul', '3'),
            Carta('verde', '1'),
            Carta('amarelo', '5')
        ])
        
        monte_compra, monte_descarte = mao.comprar(
            monte_compra,
            monte_descarte,
            quantidade=2
        )
        
        tamanho_monte_compra_atual = len(monte_compra)
        tamanho_monte_descarte_atual = len(monte_descarte)
        tamanho_cartas_atual = len(mao.cartas)

        self.assertEqual(
            tamanho_monte_compra_atual,
            0
        )
        self.assertEqual(
            tamanho_monte_descarte_atual,
            1
        )
        self.assertEqual(
            tamanho_cartas_atual,
            6
        )
    
    def test_comprar_CT7(self):
        """
        CT7 = {c1b2, c2b1, c3b2, c4b2} 
        {2, len(monte_compra) = 0, len(monte_descarte) = 3, len(cartas) = 3}
        Resultado esperado: len(cartas) = 5; len(monte_compra) = 0; len(monte_descarte) = 1
        """
        cartas_iniciais = [
          Carta('verde', '2'),
          Carta('azul', '8'),
          Carta('amarelo', '4'),  
        ]
        mao = Mao(cartas_iniciais)

        monte_compra = Pilha([])

        monte_descarte = Pilha([
            Carta('amarelo', '1'),
            Carta('verde', '7'),
            Carta('azul', '9')
        ])

        monte_compra, monte_descarte = mao.comprar(
            monte_compra,
            monte_descarte,
            quantidade=2
        )
        tamanho_monte_compra_atual = len(monte_compra)
        tamanho_monte_descarte_atual = len(monte_descarte)
        tamanho_cartas_atual = len(mao.cartas)

        self.assertEqual(
            tamanho_monte_compra_atual,
            0
        )
        self.assertEqual(
            tamanho_monte_descarte_atual,
            1
        )
        self.assertEqual(
            tamanho_cartas_atual,
            5
        )
    
    def test_comprar_CT8(self):
      """
      CT8 = {c1b2, c2b2, c3b2, c4b1} 
      {2, len(monte_compra) = 0, len(monte_descarte) = 3, len(cartas) = 0}
      Resultado esperado: len(cartas) = 2; len(monte_compra) = 0; len(monte_descarte) = 1

      """
      cartas_iniciais = []
      mao = Mao(cartas_iniciais)
      tamanho_cartas_anterior = len(mao.cartas)

      monte_compra = Pilha([])
      tamanho_monte_compra_anterior = len(monte_compra)

      monte_descarte = Pilha([
          Carta('verde', '1'),
          Carta('amarelo', '2'),
          Carta('vermelho', '5')
      ])
      tamanho_monte_descarte_anterior = len(monte_descarte)

      monte_compra, monte_descarte = mao.comprar(
          monte_compra,
          monte_descarte,
          quantidade=2
      )
      tamanho_monte_compra_atual = len(monte_compra)
      tamanho_monte_descarte_atual = len(monte_descarte)
      tamanho_cartas_atual = len(mao.cartas)

      self.assertEqual(
            tamanho_monte_compra_atual,
            0
      )
      self.assertEqual(
            tamanho_monte_descarte_atual,
            1
      )
      self.assertEqual(
            tamanho_cartas_atual,
            2
      )

    # Each choice
    def test_jogar_CT1(self):
        """
        CT1 = {c1b1, c2b1, c3b1, c4b1} = {len(cartas_possiveis) = 0, len(cartas) = 0, len(monte_compras) = 0, len(monte_descarte) = 0}
        Resultado esperado: Inviável retorna erro;
        """
        monte_compra = Pilha([])
        monte_descarte = Pilha([])
        conjunto_inicial = []
        mao = Mao(conjunto_inicial)

        with self.assertRaises(IndexError):
            mao.jogar(monte_compra, monte_descarte)

    @patch('builtins.input', side_effect=['0'])
    def test_jogar_CT2(self, mock_inputs):
        """
        CT2 = {c1b2, c2b2, c3b2, c4b2}
        {len(cartas_possiveis} = 2, len(cartas) = 2, len(monte_compras) = 4, len(monte_descarte) = 4}
        Resultado esperado: len(cartas) = 1; len(monte_compras) = 4; len(monte_descarte) = 5;
        """
        monte_compra = Pilha([
          Carta('vermelho', '3'),
          Carta('amarelo', '4'),
          CartaEspecial('azul', 'inverter'),
          CartaEspecial('amarelo', 'inverter')
        ])
        monte_descarte = Pilha([
          Carta('azul','3'),
          CartaEspecial('verde','pular'),
          Carta('vermelho','8'),
          CartaEspecial('azul','inverter')
        ])
        conjunto_inicial = [
          Carta('azul', '8'),
          CartaEspecial('azul', 'inverter'),
        ]
        mao = Mao(conjunto_inicial)

        monte_compra, monte_descarte = mao.jogar(monte_compra, monte_descarte)

        self.assertEqual(len(monte_compra), 4)
        self.assertEqual(len(monte_descarte), 5)
        self.assertEqual(len(mao.cartas), 1)


if __name__ == '__main__':
    unittest.main()
