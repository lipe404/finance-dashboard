import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


class FinanceVisualizations:

    @staticmethod
    def plot_evolucao_poupanca(historico_df):
        """Gráfico de evolução da poupança"""
        if historico_df.empty:
            return None

        # Usar 'saldo_atual' em vez de 'saldo'
        fig = px.line(
            historico_df,
            x='data',
            y='saldo_atual',  # Corrigido aqui
            title='📈 Evolução do Saldo da Poupança',
            # Corrigido aqui
            labels={'saldo_atual': 'Saldo (R\$)', 'data': 'Data'}
        )

        fig.update_layout(
            xaxis_title="Data",
            yaxis_title="Saldo (R\$)",
            hovermode='x unified'
        )

        return fig

    @staticmethod
    def plot_gastos_por_categoria(gastos_por_categoria):
        """Gráfico de pizza dos gastos por categoria"""
        if gastos_por_categoria.empty:
            return None

        fig = px.pie(
            gastos_por_categoria,
            values='valor',
            names='categoria',
            title='💰 Distribuição de Gastos por Categoria'
        )

        fig.update_traces(textposition='inside', textinfo='percent+label')

        return fig

    @staticmethod
    def plot_rendimentos_por_fonte(rendimentos_por_fonte):
        """Gráfico de barras dos rendimentos por fonte"""
        if rendimentos_por_fonte.empty:
            return None

        fig = px.bar(
            rendimentos_por_fonte,
            x='fonte',
            y='valor',
            title='💵 Rendimentos por Fonte',
            labels={'valor': 'Valor (R\$)', 'fonte': 'Fonte de Renda'}
        )

        fig.update_layout(
            xaxis_title="Fonte de Renda",
            yaxis_title="Valor (R\$)"
        )

        return fig

    @staticmethod
    def plot_simulacao_crescimento(simulacao_df):
        """Gráfico de simulação de crescimento da poupança"""
        if simulacao_df.empty:
            return None

        fig = px.line(
            simulacao_df,
            x='mes',
            y='saldo',
            title='🎯 Simulação de Crescimento da Poupança',
            labels={'saldo': 'Saldo Projetado (R\$)', 'mes': 'Meses'}
        )

        fig.update_layout(
            xaxis_title="Meses",
            yaxis_title="Saldo Projetado (R\$)",
            hovermode='x unified'
        )

        return fig

    @staticmethod
    def plot_comparativo_mensal(resumos_mensais):
        """Gráfico comparativo de rendimentos vs gastos mensais"""
        if not resumos_mensais:
            return None

        df = pd.DataFrame(resumos_mensais)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Rendimentos',
            x=df['mes_ano'],
            y=df['total_rendimentos'],
            marker_color='green'
        ))

        fig.add_trace(go.Bar(
            name='Gastos',
            x=df['mes_ano'],
            y=df['total_gastos'],
            marker_color='red'
        ))

        fig.update_layout(
            title='📊 Comparativo Mensal: Rendimentos vs Gastos',
            xaxis_title='Mês/Ano',
            yaxis_title='Valor (R\$)',
            barmode='group'
        )

        return fig

    @staticmethod
    def plot_objetivo_progresso(saldo_atual, valor_meta, nome_objetivo):
        """Gráfico de progresso do objetivo"""
        progresso = min((saldo_atual / valor_meta) * 100,
                        100) if valor_meta > 0 else 0

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=progresso,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"🎯 Progresso: {nome_objetivo}"},
            delta={'reference': 100},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))

        return fig

    @staticmethod
    def plot_evolucao_poupanca_melhorado(historico_df):
        """Gráfico melhorado de evolução da poupança com marcadores de operações"""
        if historico_df.empty:
            return None

        # Converter data para datetime se necessário
        if 'data' in historico_df.columns:
            historico_df['data'] = pd.to_datetime(historico_df['data'])

        # Criar gráfico base
        fig = go.Figure()

        # Linha principal do saldo
        fig.add_trace(go.Scatter(
            x=historico_df['data'],
            y=historico_df['saldo_atual'],
            mode='lines+markers',
            name='Saldo da Poupança',
            line=dict(color='blue', width=2),
            marker=dict(size=6)
        ))

        # Marcar depósitos
        depositos = historico_df[historico_df['operacao'] == 'deposito']
        if not depositos.empty:
            fig.add_trace(go.Scatter(
                x=depositos['data'],
                y=depositos['saldo_atual'],
                mode='markers',
                name='Depósitos',
                marker=dict(color='green', size=10, symbol='triangle-up')
            ))

        # Marcar saques
        saques = historico_df[historico_df['operacao'] == 'saque']
        if not saques.empty:
            fig.add_trace(go.Scatter(
                x=saques['data'],
                y=saques['saldo_atual'],
                mode='markers',
                name='Saques',
                marker=dict(color='red', size=10, symbol='triangle-down')
            ))

        fig.update_layout(
            title='📈 Evolução do Saldo da Poupança',
            xaxis_title='Data',
            yaxis_title='Saldo (R\$)',
            hovermode='x unified',
            showlegend=True
        )

        return fig
