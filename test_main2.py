#MUTANTE
""""
Grupo 01 - Trabalho UNO - Projeto de Teste 2020.2
Jones Martins - DRE: 115149195
Felipe Menescal - DRE: 113282298
Larissa Galeno - DRE: 116083017
Leonardo Gonçalves - DRE: 111337097
"""
import unittest
from unittest.mock import patch

from main2 import Jogador, Pilha, Carta
import main2


class TestUno(unittest.TestCase):
    def setUp(self):
        main2.topo_esta_ativo = False

    # All combinations
    def test_selecionar_CT1(self):
        # CT1
        """
        CT1 = {c1b1, c2b1} = {Carta(“vermelho”, “7”), len(cartas) = 0}
        Resultado esperado: 0 cartas selecionadas
        """
        cartas_iniciais = []
        mao = Jogador(cartas_iniciais)
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
        mao = Jogador(cartas_iniciais)
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
        mao = Jogador(cartas_iniciais)
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
          Carta('vermelho', '+2')
        ]
        mao = Jogador(cartas_iniciais)
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
          Carta('verde', 'pular'),          
          Carta('vermelho', '+2')
        ]
        mao = Jogador(cartas_iniciais)
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
        mao = Jogador(cartas_iniciais)
        cartas_selecionadas = mao.selecionar(
            topo_descarte=Carta('verde', 'pular')
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
        mao = Jogador(cartas_iniciais)
        cartas_selecionadas = mao.selecionar(
            topo_descarte=Carta('vermelho', 'coringa')
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
          Carta('verde', 'inverter'),
          Carta('azul','3'),
          Carta('vermelho','1')
        ]
        mao = Jogador(cartas_iniciais)
        cartas_selecionadas = mao.selecionar(
            topo_descarte=Carta('amarelo', 'inverter')
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
        mao = Jogador(cartas_iniciais)
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
          Carta('verde', '8')         
        ]
        mao = Jogador(cartas_iniciais)
        tamanho_cartas_anterior = len(mao.cartas)

        monte_compra = Pilha([
          Carta('amarelo', '7'),
          Carta('verde', 'inverter')
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
        mao = Jogador(cartas_iniciais)
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

        mao = Jogador(cartas_iniciais)

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
        mao = Jogador(cartas_iniciais)

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
        mao = Jogador(cartas_iniciais)

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
        mao = Jogador(cartas_iniciais)

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
      mao = Jogador(cartas_iniciais)
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
        mao = Jogador(conjunto_inicial)

        with self.assertRaises(IndexError):
            mao.jogar(
                monte_compra, 
                monte_descarte
            )

    @patch('builtins.input', side_effect=['1'])
    def test_jogar_CT2(self, mock_inputs):
        """
        CT2 = {c1b2, c2b2, c3b2, c4b2}
        {len(cartas_possiveis} = 2, len(cartas) = 2, len(monte_compras) = 4, len(monte_descarte) = 4}
        Resultado esperado: len(cartas) = 1; len(monte_compras) = 4; len(monte_descarte) = 5;
        """
        monte_compra = Pilha([
          Carta('vermelho', '3'),
          Carta('amarelo', '4'),
          Carta('azul', 'inverter'),
          Carta('amarelo', 'inverter')
        ])
        monte_descarte = Pilha([
          Carta('azul','3'),
          Carta('verde','pular'),
          Carta('vermelho','8'),
          Carta('azul','inverter')
        ])
        conjunto_inicial = [
          Carta('azul', '8'),
          Carta('azul', 'inverter')
        ]
        mao = Jogador(conjunto_inicial)

        monte_compra, monte_descarte = mao.jogar(
            monte_compra, 
            monte_descarte
        )

        self.assertEqual(len(monte_compra), 4)
        self.assertEqual(len(monte_descarte), 5)
        self.assertEqual(len(mao.cartas), 1)
    
    # segundo a pasta tes_html gerada pelo mutpy usando main2.py
    # metodos que o jogar chama : {
    # monta_listagem_cartas com 5 mutantes vivos 16, 17, 18, 19 e 28
    # escolhe_carta_possivel com 7 mutantes vivos 21, 30, 31, 32, 57, 58, 63
    # escolhe_cor_de_coringa com 3 mutantes vivos 22, 23 e 34 }
    # jogar com 5 mutantes vivos 24, 35, 36, 37 e 38
    # escrever casos de testes pro jogar, talvez usar outro criterio de combinaçao
    # escrever casos de testes pros outros metodos que o jogar chama
    # talvez desenvolve-los por partiçao de entrada e depois automação...nao sei, apenas
    # escrevi novos casos de testes

    #da linha 55 a 226 no arquivo main2.py tem toda a parte dos métodos que testamos antes
    # o resto acredito que não seja pra se preocupar, visto que o primeiro Trabalho
    # eram só alguns métodos do Jogador ao invés do jogo todo
    # total mutantes: 31 (linha 55 a 226)
    # com os testes que fiz abaixo consegui matar 27/31 mutantes => 87,09%
    

    #------JOGAR--------------------------------------------------
    # jogar com 5 mutantes vivos 24, 35, 36, 37 e 38
    @patch('builtins.input', side_effect=['1'])
    def test_jogar_CTM1(self,mock_inputs):
        """
        CTM1 = {c1b1, c2b2, c3b2, c4b2}
        {len(cartas_possiveis} = 0, len(cartas) = 2, len(monte_compras) = 4, len(monte_descarte) = 4}
        Resultado esperado: len(cartas) = 2; len(monte_compras) = 3; len(monte_descarte) = 5;
        testando quando nao há cartas possiveis a serem jogadas
        mata mutante 24 e 35
        """
        monte_compra = Pilha([
          Carta('vermelho', '3'),
          Carta('amarelo', '4'),
          Carta('azul', 'inverter'),
          Carta('amarelo', 'inverter')
        ])
        monte_descarte = Pilha([
          Carta('vermelho','0'),
          Carta('verde','pular'),
          Carta('vermelho','8'),
          Carta('azul','inverter')
        ])
        conjunto_inicial = [
          Carta('azul', '8'),
          Carta('azul', 'inverter')
        ]
        mao = Jogador(conjunto_inicial)

        monte_compra, monte_descarte = mao.jogar(
            monte_compra, 
            monte_descarte
        )

        self.assertEqual(len(monte_compra), 3)
        self.assertEqual(len(monte_descarte), 5)
        self.assertEqual(len(mao.cartas), 2)

    @patch('builtins.input', side_effect=['1'])
    def test_jogar_CTM2(self,mock_inputs):
        """
        CTM2 = {c1b2, c2b2, c3b2, c4b2}
        {len(cartas_possiveis} = 1, len(cartas) = 2, len(monte_compras) = 4, len(monte_descarte) = 4}
        Resultado esperado: len(cartas) = 2; len(monte_compras) = 3; len(monte_descarte) = 5;
        testando quando a carta jogada é especial, se sim entao o topo_esta_ativo = True
        mata mutante 36
        """
        monte_compra = Pilha([
          Carta('vermelho', '3'),
          Carta('amarelo', '4'),
          Carta('azul', 'inverter'),
          Carta('amarelo', 'inverter')
        ])
        monte_descarte = Pilha([
          Carta('vermelho','0'),
          Carta('verde','pular'),
          Carta('vermelho','8'),
          Carta('azul','inverter')
        ])
        conjunto_inicial = [
          Carta('vermelho', 'pular'),
          Carta('azul', 'inverter')
        ]
        mao = Jogador(conjunto_inicial)

        monte_compra, monte_descarte = mao.jogar(
            monte_compra, 
            monte_descarte
        )

        self.assertEqual(len(monte_compra), 4)
        self.assertEqual(len(monte_descarte), 5)
        self.assertEqual(len(mao.cartas), 1)
        self.assertTrue(main2.topo_esta_ativo)

    @patch('builtins.input', side_effect=['1','azul'])
    def test_jogar_CTM3(self,mock_inputs):
        """
        CTM3 = {c1b2, c2b2, c3b2, c4b2}
        {len(cartas_possiveis} = 1, len(cartas) = 2, len(monte_compras) = 4, len(monte_descarte) = 4}
        Resultado esperado: len(cartas) = 2; len(monte_compras) = 3; len(monte_descarte) = 5;
        testando quando a carta jogada é especial e coringa, se sim entao o topo_esta_ativo = True
        mata mutante 37 e 38
        """
        monte_compra = Pilha([
          Carta('vermelho', '3'),
          Carta('amarelo', '4'),
          Carta('azul', 'inverter'),
          Carta('amarelo', 'inverter')
        ])
        monte_descarte = Pilha([
          Carta('vermelho','0'),
          Carta('verde','pular'),
          Carta('vermelho','8'),
          Carta('azul','inverter')
        ])
        conjunto_inicial = [
          Carta('*', 'coringa'),
          Carta('azul', 'inverter')
        ]
        mao = Jogador(conjunto_inicial)

        monte_compra, monte_descarte = mao.jogar(
            monte_compra, 
            monte_descarte
        )

        self.assertEqual(len(monte_compra), 4)
        self.assertEqual(len(monte_descarte), 5)
        self.assertEqual(len(mao.cartas), 1)
        self.assertTrue(main2.topo_esta_ativo)
        

    #------ESCOLHE_COR_DE_CORINGA (ECDC) -------------------------------
    # escolhe_cor_de_coringa com 3 mutantes vivos 22, 23 e 34 
    @patch('builtins.input', side_effect=['azul'])
    def test_ECDC_CTM1(self,mock_inputs):
        """
        metodo chamado dentro de jogar
        Resultado esperado: cor escolhida é COR_VALIDA e diferente de None
        mata mutante 22
        """
        jogador = Jogador([])

        cor_escolhida = jogador.escolhe_cor_de_coringa()
        self.assertEqual(cor_escolhida, 'azul')
    
    @patch('builtins.input', side_effect=['invalido', 'azul'])
    def test_ECDC_CTM2(self,mock_inputs):
        """
        metodo chamado dentro de jogar
        Resultado esperado: cor escolhida é COR_VALIDA e diferente de None
        ver uma forma de matar mutante 23 34
         
         mutante 23:
        esperado - 182:  if cor_escolhida not in CORES_VALIDAS:
        mutante  - 182:  if cor_escolhida in CORES_VALIDAS:
         
         
         mutante 34:       
        esperado - 182:  if cor_escolhida not in CORES_VALIDAS:
        mutante  - 182:  if not (cor_escolhida not in CORES_VALIDAS):
        """
        jogador = Jogador([])
        cor_escolhida = jogador.escolhe_cor_de_coringa()
        self.assertEqual(cor_escolhida, 'azul')

    #------ESCOLHE_CARTA_POSSIVEL (ECC) -------------------------------
    # escolhe_carta_possivel com 7 mutantes vivos 21, 30, 31, 32, 57, 58, 63
    @patch('builtins.input', side_effect=['0', '1'])
    def test_ECC_CTM1(self,mock_inputs):
        """
        metodo chamado dentro de jogar
        indices vao de 1 até len(cartas_possiveis)
        Resultado esperado: para matar mutantes escolher indice errado pode ser uma estrategia
        mata todos mutantes gerados
        """
        monte_descarte = Pilha([
          Carta('azul','0'),
          Carta('verde','pular'),
          Carta('vermelho','8'),
          Carta('azul','inverter')
        ])

        conjunto_inicial = [
          Carta('azul', '1'),
          Carta('azul', 'inverter')
        ]
        mao = Jogador(conjunto_inicial)

        topo = monte_descarte.topo()
        cartas_possiveis = mao.selecionar(topo)
        # with self.assertRaises(StopIteration):
        #   mao._escolhe_carta_possivel(cartas_possiveis)
    
     #------MONTA_LISTAGEM_CARTAS (MLC) -------------------------------
     # monta_listagem_cartas com 5 mutantes vivos 16, 17, 18, 19 e 28
    def test_MLC_CTM1(self):
        """
        metodo chamado dentro de jogar
        recebe lista de cartas e um bool numerar
        retorna listagem -> uma string
        Resultado esperado: para matar mutante > com cartas, listagem_esperada = listagem
        mata mutantes 18 e 19 e 28
        """

        conjunto_inicial = [
          Carta('azul', '1'),
          Carta('azul', 'inverter')
        ]
        
        inicio = '-'
        listagem_esperada = f'Cartas: \n\t{inicio} {conjunto_inicial[0]};' + f'\n\t{inicio} {conjunto_inicial[1]};' 
        print(listagem_esperada)
        mao = Jogador(conjunto_inicial)
        listagem = main2.monta_listagem_de_cartas(mao.cartas)
        print(listagem)
        self.assertEqual(listagem, listagem_esperada)
        
    # def test_MLC_CTM2(self):
    #     """
    #     metodo chamado dentro de jogar
    #     recebe lista de cartas e um bool numerar
    #     retorna listagem -> uma string
    #     Resultado esperado: mutantes 16 17 dao timeout pq substituem operador += que pode ser
    #     usado para strings por -= que nao pode
    #     arranjar uma forma de testar isso 

    #     """

    #     lista = None  # mudou de [1, 2, 3] pra None

    #     lista.append(5)  # TypeError

    #     conjunto_inicial = []
    #     listagem_esperada = 'Cartas: *vazio*'
    #     print(listagem_esperada)
        
    #     with self.assertRaises(TypeError):
    #         listagem = main2.monta_listagem_de_cartas(conjunto_inicial)
        
    


if __name__ == '__main__':
    unittest.main()

# mut.py --target main2.py --unit-test test_main2.py -m -c --mutation-number NUMERO_MUTANTE

# mut.py --target main2.py --unit-test test_main2.py -m -c

# mut.py --target main2.py --unit-test test_main2.py -m -c --report-html tes.html