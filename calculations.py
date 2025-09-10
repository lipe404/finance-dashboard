import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class FinanceCalculator:

    @staticmethod
    def calcular_rendimento_poupanca(saldo_inicial, taxa_anual, meses):
        """Calcula rendimento da poupança com juros compostos"""
        taxa_mensal = (taxa_anual / 100) / 12
        saldo_final = saldo_inicial * ((1 + taxa_mensal) ** meses)
        return saldo_final

    @staticmethod
    def simular_crescimento_poupanca(saldo_inicial, aporte_mensal, taxa_anual, meses):
        """Simula crescimento da poupança com aportes mensais"""
        taxa_mensal = (taxa_anual / 100) / 12

        historico = []
        saldo_atual = saldo_inicial

        for mes in range(meses + 1):
            if mes > 0:
                # Aplica rendimento
                saldo_atual = saldo_atual * (1 + taxa_mensal)
                # Adiciona aporte
                saldo_atual += aporte_mensal

            historico.append({
                'mes': mes,
                'saldo': saldo_atual,
                'data': (datetime.now() + timedelta(days=30*mes)).strftime('%Y-%m-%d')
            })

        return pd.DataFrame(historico)

    @staticmethod
    def calcular_aporte_necessario(valor_meta, saldo_atual, taxa_anual, meses):
        """Calcula aporte mensal necessário para atingir meta"""
        if meses <= 0:
            return 0

        taxa_mensal = (taxa_anual / 100) / 12

        # Valor futuro do saldo atual
        valor_futuro_saldo = saldo_atual * ((1 + taxa_mensal) ** meses)

        # Valor que precisa ser acumulado com aportes
        valor_necessario = valor_meta - valor_futuro_saldo

        if valor_necessario <= 0:
            return 0

        # Fórmula para anuidade (aportes mensais)
        if taxa_mensal == 0:
            aporte_necessario = valor_necessario / meses
        else:
            aporte_necessario = valor_necessario * \
                taxa_mensal / (((1 + taxa_mensal) ** meses) - 1)

        return max(0, aporte_necessario)

    @staticmethod
    def calcular_resumo_mensal(rendimentos_df, gastos_df, mes_ano=None):
        """Calcula resumo financeiro mensal"""
        if mes_ano is None:
            mes_ano = datetime.now().strftime('%Y-%m')

        # Filtrar por mês/ano
        if not rendimentos_df.empty:
            rendimentos_mes = rendimentos_df[
                pd.to_datetime(rendimentos_df['data']).dt.strftime(
                    '%Y-%m') == mes_ano
            ]
            total_rendimentos = rendimentos_mes['valor'].sum()
        else:
            total_rendimentos = 0

        if not gastos_df.empty:
            gastos_mes = gastos_df[
                pd.to_datetime(gastos_df['data']).dt.strftime(
                    '%Y-%m') == mes_ano
            ]
            total_gastos = gastos_mes['valor'].sum()
        else:
            total_gastos = 0

        saldo_mensal = total_rendimentos - total_gastos

        return {
            'total_rendimentos': total_rendimentos,
            'total_gastos': total_gastos,
            'saldo_mensal': saldo_mensal,
            'mes_ano': mes_ano
        }

    @staticmethod
    def calcular_gastos_por_categoria(gastos_df):
        """Calcula gastos agrupados por categoria"""
        if gastos_df.empty:
            return pd.DataFrame()

        return gastos_df.groupby('categoria')['valor'].sum().reset_index()

    @staticmethod
    def calcular_rendimentos_por_fonte(rendimentos_df):
        """Calcula rendimentos agrupados por fonte"""
        if rendimentos_df.empty:
            return pd.DataFrame()

        return rendimentos_df.groupby('fonte')['valor'].sum().reset_index()
