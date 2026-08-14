"""
===============================================================================
ESTUDANTES: Maria Clara Corrêa // Leonardo Fernandes
DATA: 13/08/2026
DISCIPLINA: Linguagem de Programação II / Laboratório LP2

DESCRIÇÃO DO PROGRAMA:
  Aplicativo top para a Academia ACME que calcula a quantidade
  diária recomendada de água com base no peso corporal, nível de atividade física e 
  condições climáticas do dia 

FÓRMULAS E REGRAS DE NEGÓCIO:
  1. Consumo Base: base_ml = peso * ML_POR_KG (35 ml por kg de peso corporal).
  2. Fator de Atividade Física (multiplicativo):
     - Leve: FATOR_LEVE = 1.00 (sem acréscimo)
     - Moderado: FATOR_MODERADO = 1.15 (+15%)
     - Intenso: FATOR_INTENSO = 1.30 (+30%)
  3. Fator Climático (multiplicativo):
     - Dia normal: FATOR_CLIMA_NORMAL = 1.00
     - Dia quente ou muito seco: FATOR_CLIMA_QUENTE = 1.10 (+10%)
  4. Meta Total em Millilitros:
     meta_ml = peso * ML_POR_KG * fator_atividade * fator_clima
  5. Conversão e Copos:
     - meta_litros = meta_ml / ML_POR_LITRO (1000)
     - copos = math.ceil(meta_ml / CAPACIDADE_COPO_ML) (arredondado para cima)
===============================================================================
"""

import math
import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# --- CONSTANTES DE CONFIGURAÇÃO DE ARQUIVO ---
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(PASTA, "agua.glade")

# --- CONSTANTES DE NEGÓCIO (Evita números estranhos no código) ---
ML_POR_KG = 35.0
ML_POR_LITRO = 1000.0
CAPACIDADE_COPO_ML = 200.0

# Fatores de atividade física
FATORES_ATIVIDADE = {
    0: 1.00,  # Leve
    1: 1.15,  # Moderado
    2: 1.30,  # Intenso
}

# Fatores climáticos
FATOR_CLIMA_NORMAL = 1.00
FATOR_CLIMA_QUENTE = 1.10


class Aplicacao:
    """Classe principal que gerencia a interface gráfica e eventos."""

    def __init__(self):
        """Inicializa o Gtk.Builder, carrega o Glade, obtém as referências e conecta os sinais."""
        self.builder = Gtk.Builder()
        self.builder.add_from_file(ARQUIVO)

        # Mapea e conecta automático(ao_destruir, ao_calcular, ao_limpar)
        self.builder.connect_signals(self)

        # Referências salvas em atributos de instância (Apenas os componentes acessados/alterados pelo Python)
        self.spn_peso = self.builder.get_object("spn_peso")
        self.cmb_atividade = self.builder.get_object("cmb_atividade")
        self.chk_clima = self.builder.get_object("chk_clima")
        self.lbl_resultado = self.builder.get_object("lbl_resultado")
        self.jan_principal = self.builder.get_object("jan_principal")

        # Exibe a janela principal
        self.jan_principal.show_all()

    def fator_da_atividade(self) -> float:
        """Obtém o fator multiplicativo correspondente à opção selecionada

        Returns:
            float: Fator de atividade (1.00, 1.15 ou 1.30).
        """
        indice = self.cmb_atividade.get_active()
        return FATORES_ATIVIDADE.get(indice, 1.00)

    def calcular_meta(self, peso: float, fator_atividade: float, clima_quente: bool) -> float:
        """ Calcula a meta total diária de água em mililitros.

        Args:
            peso (float): Peso da pessoa em quilogramas.
            fator_atividade (float): Fator multiplicativo da atividade física.
            clima_quente (bool): Indica se o dia está quente ou muito seco.

        Returns:
            float: Meta diária calculada em ml.
        """
        fator_clima = FATOR_CLIMA_QUENTE if clima_quente else FATOR_CLIMA_NORMAL
        meta_ml = peso * ML_POR_KG * fator_atividade * fator_clima
        return meta_ml

    def contar_copos(self, meta_ml: float) -> int:
        """Calcula a quantidade aproximada de copos de 200 ml.

        Args:
            meta_ml (float): Meta diária em mililitros.

        Returns:
            int: Quantidade de copos arredondada para cima.
        """
        return math.ceil(meta_ml / CAPACIDADE_COPO_ML)

    # --- HANDLERS / TRATADORES DE EVENTOS ---

    def ao_calcular(self, widget):
        """Handler executado ao clicar no botão 'Calcular'.

        Lê os dados da GUI, chama os métodos de cálculo e exibe o resultado
        """
        peso = self.spn_peso.get_value()
        fator_atividade = self.fator_da_atividade()
        clima_quente = self.chk_clima.get_active()

        # Cálculo da regra de negócio
        meta_ml = self.calcular_meta(peso, fator_atividade, clima_quente)
        meta_litros = meta_ml / ML_POR_LITRO
        copos = self.contar_copos(meta_ml)

        # Atualização do label com marcações e arrumado bonitinho
        texto_resultado = (
            f"<big><b>{meta_litros:.2f} L por dia</b></big>\n"
            f"<small>Cerca de {copos} copos de 200 ml</small>"
        )
        self.lbl_resultado.set_markup(texto_resultado)

    def ao_limpar(self, widget):
        """Handler executado ao clicar no botão 'Limpar'.

        Restaura os valores padrão de todos os controles da interface.
        """
        self.spn_peso.set_value(70.0)
        self.cmb_atividade.set_active(0)
        self.chk_clima.set_active(False)
        self.lbl_resultado.set_label("")

    def ao_destruir(self, widget):
        """Handler do evento destroy da janela principal."""
        Gtk.main_quit()


if __name__ == "__main__":
    app = Aplicacao()
    Gtk.main()