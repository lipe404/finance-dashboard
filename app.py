import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
from data_manager import DataManager
from calculations import FinanceCalculator
from visualizations import FinanceVisualizations

# Configuração da página
st.set_page_config(
    page_title="Dashboard Finanças Pessoais",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização


@st.cache_resource
def init_data_manager():
    return DataManager()


@st.cache_resource
def init_calculator():
    return FinanceCalculator()


@st.cache_resource
def init_visualizations():
    return FinanceVisualizations()


# Instâncias globais
data_manager = init_data_manager()
calculator = init_calculator()
visualizations = init_visualizations()


def main():
    # Header
    st.markdown('<h1 class="main-header">💰 Dashboard de Finanças Pessoais</h1>',
                unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("📋 Menu de Navegação")

    menu_options = [
        "🏠 Dashboard Principal",
        "💵 Rendimentos",
        "💸 Gastos",
        "🏦 Poupança",
        "🎯 Objetivos e Simulações",
        "📊 Relatórios"
    ]

    selected_option = st.sidebar.selectbox("Escolha uma seção:", menu_options)

    # Roteamento
    if selected_option == "🏠 Dashboard Principal":
        dashboard_principal()
    elif selected_option == "💵 Rendimentos":
        secao_rendimentos()
    elif selected_option == "💸 Gastos":
        secao_gastos()
    elif selected_option == "🏦 Poupança":
        secao_poupanca()
    elif selected_option == "🎯 Objetivos e Simulações":
        secao_objetivos_simulacoes()
    elif selected_option == "📊 Relatórios":
        secao_relatorios()


def dashboard_principal():
    st.header("🏠 Dashboard Principal")

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    # Calcular métricas
    rendimentos_df = data_manager.get_rendimentos_df()
    gastos_df = data_manager.get_gastos_df()
    saldo_poupanca = data_manager.data['poupanca']['saldo_atual']

    resumo_atual = calculator.calcular_resumo_mensal(rendimentos_df, gastos_df)

    with col1:
        st.metric(
            label="💵 Rendimentos do Mês",
            value=f"R\$ {resumo_atual['total_rendimentos']:,.2f}",
            delta=None
        )

    with col2:
        st.metric(
            label="💸 Gastos do Mês",
            value=f"R\$ {resumo_atual['total_gastos']:,.2f}",
            delta=None
        )

    with col3:
        st.metric(
            label="💰 Saldo do Mês",
            value=f"R\$ {resumo_atual['saldo_mensal']:,.2f}",
            delta=None
        )

    with col4:
        st.metric(
            label="🏦 Saldo Poupança",
            value=f"R\$ {saldo_poupanca:,.2f}",
            delta=None
        )

    st.divider()

    # Gráficos principais
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de gastos por categoria
        if not gastos_df.empty:
            gastos_categoria = calculator.calcular_gastos_por_categoria(
                gastos_df)
            fig_gastos = visualizations.plot_gastos_por_categoria(
                gastos_categoria)
            if fig_gastos:
                st.plotly_chart(fig_gastos, use_container_width=True)
        else:
            st.info("📊 Adicione gastos para visualizar o gráfico por categoria")

    with col2:
        # Gráfico de rendimentos por fonte
        if not rendimentos_df.empty:
            rendimentos_fonte = calculator.calcular_rendimentos_por_fonte(
                rendimentos_df)
            fig_rendimentos = visualizations.plot_rendimentos_por_fonte(
                rendimentos_fonte)
            if fig_rendimentos:
                st.plotly_chart(fig_rendimentos, use_container_width=True)
        else:
            st.info("📊 Adicione rendimentos para visualizar o gráfico por fonte")

    # Evolução da poupança
    historico_poupanca = data_manager.get_poupanca_historico_df()
    if not historico_poupanca.empty:
        fig_evolucao = visualizations.plot_evolucao_poupanca(
            historico_poupanca)
        if fig_evolucao:
            st.plotly_chart(fig_evolucao, use_container_width=True)


def secao_rendimentos():
    st.header("💵 Gestão de Rendimentos")

    tab1, tab2 = st.tabs(["➕ Adicionar Rendimento", "📋 Histórico"])

    with tab1:
        st.subheader("Cadastrar Novo Rendimento")

        col1, col2 = st.columns(2)

        with col1:
            fonte = st.text_input(
                "🏢 Fonte de Renda", placeholder="Ex: Salário, Freelance, Investimentos")
            valor = st.number_input("💰 Valor (R\$)", min_value=0.01, step=0.01)

        with col2:
            data_rendimento = st.date_input("📅 Data", value=date.today())
            descricao = st.text_area(
                "📝 Descrição (opcional)", placeholder="Detalhes adicionais...")

        if st.button("💾 Salvar Rendimento", type="primary"):
            if fonte and valor > 0:
                if data_manager.add_rendimento(fonte, valor, data_rendimento, descricao):
                    st.success("✅ Rendimento adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao salvar rendimento")
            else:
                st.error("❌ Preencha todos os campos obrigatórios")

    with tab2:
        st.subheader("Histórico de Rendimentos")

        rendimentos_df = data_manager.get_rendimentos_df()

        if not rendimentos_df.empty:
            # Filtros
            col1, col2 = st.columns(2)

            with col1:
                fontes_unicas = ['Todas'] + \
                    list(rendimentos_df['fonte'].unique())
                fonte_filtro = st.selectbox(
                    "🔍 Filtrar por Fonte", fontes_unicas)

            with col2:
                # Filtro por mês
                rendimentos_df['data'] = pd.to_datetime(rendimentos_df['data'])
                meses_unicos = [
                    'Todos'] + sorted(rendimentos_df['data'].dt.strftime('%Y-%m').unique(), reverse=True)
                mes_filtro = st.selectbox("📅 Filtrar por Mês", meses_unicos)

            # Aplicar filtros
            df_filtrado = rendimentos_df.copy()

            if fonte_filtro != 'Todas':
                df_filtrado = df_filtrado[df_filtrado['fonte'] == fonte_filtro]

            if mes_filtro != 'Todos':
                df_filtrado = df_filtrado[df_filtrado['data'].dt.strftime(
                    '%Y-%m') == mes_filtro]

            # Exibir tabela
            if not df_filtrado.empty:
                df_display = df_filtrado[[
                    'fonte', 'valor', 'data', 'descricao']].copy()
                df_display['valor'] = df_display['valor'].apply(
                    lambda x: f"R\$ {x:,.2f}")
                df_display['data'] = df_display['data'].dt.strftime('%d/%m/%Y')

                st.dataframe(
                    df_display,
                    column_config={
                        "fonte": "Fonte",
                        "valor": "Valor",
                        "data": "Data",
                        "descricao": "Descrição"
                    },
                    hide_index=True,
                    use_container_width=True
                )

                # Resumo
                total_filtrado = df_filtrado['valor'].sum()
                st.metric("💰 Total do Período", f"R\$ {total_filtrado:,.2f}")
            else:
                st.info("📊 Nenhum rendimento encontrado com os filtros aplicados")
        else:
            st.info("📊 Nenhum rendimento cadastrado ainda")


def secao_gastos():
    st.header("💸 Gestão de Gastos")

    tab1, tab2 = st.tabs(["➕ Adicionar Gasto", "📋 Histórico"])

    # Categorias predefinidas
    categorias_padrao = [
        "🏠 Moradia", "🍽️ Alimentação", "🚗 Transporte", "💊 Saúde",
        "🎓 Educação", "🎬 Lazer", "👕 Vestuário", "📱 Tecnologia",
        "💡 Utilidades", "🎁 Presentes", "📄 Documentos", "🔧 Outros"
    ]

    with tab1:
        st.subheader("Cadastrar Novo Gasto")

        col1, col2 = st.columns(2)

        with col1:
            categoria = st.selectbox("🏷️ Categoria", categorias_padrao)
            valor = st.number_input("💰 Valor (R\$)", min_value=0.01, step=0.01)

        with col2:
            data_gasto = st.date_input("📅 Data", value=date.today())
            descricao = st.text_area(
                "📝 Descrição (opcional)", placeholder="Detalhes do gasto...")

        if st.button("💾 Salvar Gasto", type="primary"):
            if categoria and valor > 0:
                if data_manager.add_gasto(categoria, valor, data_gasto, descricao):
                    st.success("✅ Gasto adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao salvar gasto")
            else:
                st.error("❌ Preencha todos os campos obrigatórios")

    with tab2:
        st.subheader("Histórico de Gastos")

        gastos_df = data_manager.get_gastos_df()

        if not gastos_df.empty:
            # Filtros
            col1, col2 = st.columns(2)

            with col1:
                categorias_unicas = ['Todas'] + \
                    list(gastos_df['categoria'].unique())
                categoria_filtro = st.selectbox(
                    "�� Filtrar por Categoria", categorias_unicas)

            with col2:
                # Filtro por mês
                gastos_df['data'] = pd.to_datetime(gastos_df['data'])
                meses_unicos = [
                    'Todos'] + sorted(gastos_df['data'].dt.strftime('%Y-%m').unique(), reverse=True)
                mes_filtro = st.selectbox("📅 Filtrar por Mês", meses_unicos)

            # Aplicar filtros
            df_filtrado = gastos_df.copy()

            if categoria_filtro != 'Todas':
                df_filtrado = df_filtrado[df_filtrado['categoria']
                                          == categoria_filtro]

            if mes_filtro != 'Todos':
                df_filtrado = df_filtrado[df_filtrado['data'].dt.strftime(
                    '%Y-%m') == mes_filtro]

            # Exibir tabela
            if not df_filtrado.empty:
                df_display = df_filtrado[['categoria',
                                          'valor', 'data', 'descricao']].copy()
                df_display['valor'] = df_display['valor'].apply(
                    lambda x: f"R\$ {x:,.2f}")
                df_display['data'] = df_display['data'].dt.strftime('%d/%m/%Y')

                st.dataframe(
                    df_display,
                    column_config={
                        "categoria": "Categoria",
                        "valor": "Valor",
                        "data": "Data",
                        "descricao": "Descrição"
                    },
                    hide_index=True,
                    use_container_width=True
                )

                # Resumo
                total_filtrado = df_filtrado['valor'].sum()
                st.metric("💸 Total do Período", f"R\$ {total_filtrado:,.2f}")
            else:
                st.info("📊 Nenhum gasto encontrado com os filtros aplicados")
        else:
            st.info("📊 Nenhum gasto cadastrado ainda")


def secao_poupanca():
    st.header("🏦 Gestão da Poupança")

    tab1, tab2, tab3 = st.tabs(
        ["💰 Saldo Atual", "📊 Movimentações", "⚙️ Configurações"])

    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Saldo Atual da Poupança")
            saldo_atual = data_manager.data['poupanca']['saldo_atual']
            st.metric("💰 Saldo", f"R\$ {saldo_atual:,.2f}")

            # Histórico de movimentações
            historico_df = data_manager.get_poupanca_historico_df()
            if not historico_df.empty:
                fig_evolucao = visualizations.plot_evolucao_poupanca(
                    historico_df)
                if fig_evolucao:
                    st.plotly_chart(fig_evolucao, use_container_width=True)

        with col2:
            st.subheader("Nova Movimentação")

            operacao = st.selectbox("🔄 Operação", ["deposito", "saque"])
            valor_operacao = st.number_input(
                "💰 Valor (R\$)", min_value=0.01, step=0.01)
            descricao_operacao = st.text_input(
                "📝 Descrição", placeholder="Motivo da operação...")

            if st.button("💾 Executar Operação", type="primary"):
                if valor_operacao > 0:
                    if operacao == "saque" and valor_operacao > saldo_atual:
                        st.error("❌ Saldo insuficiente para saque")
                    else:
                        if data_manager.update_poupanca(operacao, valor_operacao, descricao_operacao):
                            emoji = "📈" if operacao == "deposito" else "📉"
                            st.success(
                                f"✅ {emoji} {operacao.capitalize()} realizado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao executar operação")
                else:
                    st.error("❌ Valor deve ser maior que zero")

    with tab2:
        st.subheader("📊 Histórico de Movimentações")

        historico_df = data_manager.get_poupanca_historico_df()

        if not historico_df.empty:
            # Filtros
            col1, col2 = st.columns(2)

            with col1:
                operacoes_unicas = ['Todas'] + \
                    list(historico_df['operacao'].unique())
                operacao_filtro = st.selectbox(
                    "🔍 Filtrar por Operação", operacoes_unicas)

            with col2:
                historico_df['data'] = pd.to_datetime(historico_df['data'])
                meses_unicos = [
                    'Todos'] + sorted(historico_df['data'].dt.strftime('%Y-%m').unique(), reverse=True)
                mes_filtro = st.selectbox("📅 Filtrar por Mês", meses_unicos)

            # Aplicar filtros
            df_filtrado = historico_df.copy()

            if operacao_filtro != 'Todas':
                df_filtrado = df_filtrado[df_filtrado['operacao']
                                          == operacao_filtro]

            if mes_filtro != 'Todos':
                df_filtrado = df_filtrado[df_filtrado['data'].dt.strftime(
                    '%Y-%m') == mes_filtro]

            # Exibir tabela
            if not df_filtrado.empty:
                df_display = df_filtrado[[
                    'operacao', 'valor', 'saldo_atual', 'data', 'descricao']].copy()
                df_display['valor'] = df_display['valor'].apply(
                    lambda x: f"R\$ {x:,.2f}")
                df_display['saldo_atual'] = df_display['saldo_atual'].apply(
                    lambda x: f"R\$ {x:,.2f}")
                df_display['data'] = df_display['data'].dt.strftime('%d/%m/%Y')
                df_display['operacao'] = df_display['operacao'].apply(
                    lambda x: "📈 Depósito" if x == "deposito" else "�� Saque")

                st.dataframe(
                    df_display,
                    column_config={
                        "operacao": "Operação",
                        "valor": "Valor",
                        "saldo_atual": "Saldo Resultante",
                        "data": "Data",
                        "descricao": "Descrição"
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("📊 Nenhuma movimentação encontrada com os filtros aplicados")
        else:
            st.info("📊 Nenhuma movimentação registrada ainda")

    with tab3:
        st.subheader("⚙️ Configurações da Poupança")

        taxa_atual = data_manager.data['poupanca']['taxa_cdi']

        st.info(f"📊 Taxa CDI atual: {taxa_atual}% ao ano")

        nova_taxa = st.number_input(
            "🔧 Nova Taxa CDI (% ao ano)",
            min_value=0.01,
            max_value=50.0,
            value=taxa_atual,
            step=0.01
        )

        if st.button("💾 Atualizar Taxa CDI"):
            if data_manager.update_taxa_cdi(nova_taxa):
                st.success("✅ Taxa CDI atualizada com sucesso!")
                st.rerun()
            else:
                st.error("❌ Erro ao atualizar taxa CDI")


def secao_objetivos_simulacoes():
    st.header("🎯 Objetivos e Simulações")

    tab1, tab2, tab3 = st.tabs(
        ["🎯 Objetivos", "📈 Simulações", "🧮 Calculadora"])

    with tab1:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Cadastrar Novo Objetivo")

            nome_objetivo = st.text_input(
                "🎯 Nome do Objetivo", placeholder="Ex: Viagem, Carro, Casa...")
            valor_meta = st.number_input(
                "💰 Valor Meta (R\$)", min_value=1.0, step=100.0)
            prazo_meses = st.number_input(
                "📅 Prazo (meses)", min_value=1, max_value=600, step=1)
            descricao_objetivo = st.text_area(
                "📝 Descrição", placeholder="Detalhes do objetivo...")

            if st.button("💾 Salvar Objetivo"):
                if nome_objetivo and valor_meta > 0 and prazo_meses > 0:
                    if data_manager.add_objetivo(nome_objetivo, valor_meta, prazo_meses, descricao_objetivo):
                        st.success("✅ Objetivo adicionado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao salvar objetivo")
                else:
                    st.error("❌ Preencha todos os campos obrigatórios")

        with col2:
            st.subheader("Objetivos Cadastrados")

            objetivos = data_manager.data['objetivos']
            saldo_atual = data_manager.data['poupanca']['saldo_atual']
            taxa_cdi = data_manager.data['poupanca']['taxa_cdi']

            if objetivos:
                for objetivo in objetivos:
                    if objetivo['ativo']:
                        with st.expander(f"🎯 {objetivo['nome']}"):
                            col_a, col_b = st.columns(2)

                            with col_a:
                                st.write(
                                    f"💰 **Meta:** R\$ {objetivo['valor_meta']:,.2f}")
                                st.write(
                                    f"📅 **Prazo:** {objetivo['prazo_meses']} meses")
                                st.write(
                                    f"📝 **Descrição:** {objetivo['descricao']}")

                            with col_b:
                                # Calcular aporte necessário
                                aporte_necessario = calculator.calcular_aporte_necessario(
                                    objetivo['valor_meta'],
                                    saldo_atual,
                                    taxa_cdi,
                                    objetivo['prazo_meses']
                                )

                                st.write(
                                    f"💵 **Aporte mensal necessário:** R\$ {aporte_necessario:,.2f}")

                                # Progresso
                                progresso = min(
                                    (saldo_atual / objetivo['valor_meta']) * 100, 100)
                                st.progress(progresso / 100)
                                st.write(f"📊 **Progresso:** {progresso:.1f}%")
            else:
                st.info("🎯 Nenhum objetivo cadastrado ainda")

    with tab2:
        st.subheader("📈 Simulação de Crescimento")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.write("**Parâmetros da Simulação:**")

            saldo_inicial_sim = st.number_input(
                "💰 Saldo Inicial (R\$)",
                min_value=0.0,
                value=float(data_manager.data['poupanca']['saldo_atual']),
                step=100.0
            )

            aporte_mensal_sim = st.number_input(
                "💵 Aporte Mensal (R\$)",
                min_value=0.0,
                value=500.0,
                step=50.0
            )

            taxa_anual_sim = st.slider(
                "📊 Taxa Anual (%)",
                min_value=1.0,
                max_value=30.0,
                value=float(data_manager.data['poupanca']['taxa_cdi']),
                step=0.1
            )

            periodo_meses_sim = st.slider(
                "📅 Período (meses)",
                min_value=1,
                max_value=360,
                value=60,
                step=1
            )

        with col2:
            # Executar simulação
            simulacao_df = calculator.simular_crescimento_poupanca(
                saldo_inicial_sim,
                aporte_mensal_sim,
                taxa_anual_sim,
                periodo_meses_sim
            )

            # Gráfico da simulação
            fig_simulacao = visualizations.plot_simulacao_crescimento(
                simulacao_df)
            if fig_simulacao:
                st.plotly_chart(fig_simulacao, use_container_width=True)

            # Resultados
            saldo_final = simulacao_df['saldo'].iloc[-1]
            total_investido = saldo_inicial_sim + \
                (aporte_mensal_sim * periodo_meses_sim)
            rendimento_total = saldo_final - total_investido

            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.metric("💰 Saldo Final", f"R\$ {saldo_final:,.2f}")

            with col_b:
                st.metric("💵 Total Investido", f"R\$ {total_investido:,.2f}")

            with col_c:
                st.metric("📈 Rendimento", f"R\$ {rendimento_total:,.2f}")

    with tab3:
        st.subheader("🧮 Calculadora de Objetivos")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Calcular Aporte Necessário:**")

            valor_meta_calc = st.number_input(
                "🎯 Valor do Objetivo (R\$)", min_value=1.0, step=100.0, value=10000.0)
            saldo_atual_calc = st.number_input("💰 Saldo Atual (R\$)", min_value=0.0, step=100.0, value=float(
                data_manager.data['poupanca']['saldo_atual']))
            prazo_calc = st.number_input(
                "📅 Prazo (meses)", min_value=1, max_value=600, step=1, value=24)
            taxa_calc = st.number_input("📊 Taxa Anual (%)", min_value=0.1, max_value=50.0, step=0.1, value=float(
                data_manager.data['poupanca']['taxa_cdi']))

            if st.button("🧮 Calcular"):
                aporte_necessario = calculator.calcular_aporte_necessario(
                    valor_meta_calc,
                    saldo_atual_calc,
                    taxa_calc,
                    prazo_calc
                )

                st.success(
                    f"💵 **Aporte mensal necessário:** R\$ {aporte_necessario:,.2f}")

                # Verificar viabilidade
                total_aportes = aporte_necessario * prazo_calc
                rendimento_esperado = valor_meta_calc - saldo_atual_calc - total_aportes

                st.info(f"📊 **Total em aportes:** R\$ {total_aportes:,.2f}")
                st.info(
                    f"📈 **Rendimento esperado:** R\$ {rendimento_esperado:,.2f}")

        with col2:
            st.write("**Calcular Tempo Necessário:**")

            valor_meta_tempo = st.number_input(
                "🎯 Valor do Objetivo (R\$)", min_value=1.0, step=100.0, value=10000.0, key="tempo_meta")
            saldo_atual_tempo = st.number_input("💰 Saldo Atual (R\$)", min_value=0.0, step=100.0, value=float(
                data_manager.data['poupanca']['saldo_atual']), key="tempo_saldo")
            aporte_mensal_tempo = st.number_input(
                "💵 Aporte Mensal (R\$)", min_value=0.0, step=50.0, value=500.0, key="tempo_aporte")
            taxa_tempo = st.number_input("📊 Taxa Anual (%)", min_value=0.1, max_value=50.0, step=0.1, value=float(
                data_manager.data['poupanca']['taxa_cdi']), key="tempo_taxa")

            if st.button("⏰ Calcular Tempo"):
                # Calcular tempo necessário usando simulação
                tempo_necessario = 0
                saldo_simulado = saldo_atual_tempo
                taxa_mensal = (taxa_tempo / 100) / 12

                while saldo_simulado < valor_meta_tempo and tempo_necessario < 600:  # máximo 50 anos
                    saldo_simulado = saldo_simulado * \
                        (1 + taxa_mensal) + aporte_mensal_tempo
                    tempo_necessario += 1

                if tempo_necessario < 600:
                    anos = tempo_necessario // 12
                    meses = tempo_necessario % 12

                    if anos > 0:
                        tempo_str = f"{anos} ano(s) e {meses} mês(es)"
                    else:
                        tempo_str = f"{meses} mês(es)"

                    st.success(f"⏰ **Tempo necessário:** {tempo_str}")
                    st.info(f"📅 **Total de meses:** {tempo_necessario}")
                else:
                    st.error("❌ Meta muito alta ou aportes insuficientes")


def secao_relatorios():
    st.header("📊 Relatórios e Análises")

    tab1, tab2, tab3 = st.tabs(
        ["📈 Resumo Geral", "📊 Análise Mensal", "📋 Exportar Dados"])

    with tab1:
        st.subheader("�� Resumo Geral das Finanças")

        # Carregar dados
        rendimentos_df = data_manager.get_rendimentos_df()
        gastos_df = data_manager.get_gastos_df()
        historico_poupanca = data_manager.get_poupanca_historico_df()

        # Métricas gerais
        col1, col2, col3, col4 = st.columns(4)

        total_rendimentos = rendimentos_df['valor'].sum(
        ) if not rendimentos_df.empty else 0
        total_gastos = gastos_df['valor'].sum() if not gastos_df.empty else 0
        saldo_total = total_rendimentos - total_gastos
        saldo_poupanca = data_manager.data['poupanca']['saldo_atual']

        with col1:
            st.metric("💵 Total Rendimentos", f"R\$ {total_rendimentos:,.2f}")

        with col2:
            st.metric("💸 Total Gastos", f"R\$ {total_gastos:,.2f}")

        with col3:
            st.metric("💰 Saldo Líquido", f"R\$ {saldo_total:,.2f}")

        with col4:
            st.metric("🏦 Poupança", f"R\$ {saldo_poupanca:,.2f}")

        st.divider()

        # Gráficos de análise
        col1, col2 = st.columns(2)

        with col1:
            if not gastos_df.empty:
                gastos_categoria = calculator.calcular_gastos_por_categoria(
                    gastos_df)
                fig_gastos = visualizations.plot_gastos_por_categoria(
                    gastos_categoria)
                if fig_gastos:
                    st.plotly_chart(fig_gastos, use_container_width=True)

        with col2:
            if not rendimentos_df.empty:
                rendimentos_fonte = calculator.calcular_rendimentos_por_fonte(
                    rendimentos_df)
                fig_rendimentos = visualizations.plot_rendimentos_por_fonte(
                    rendimentos_fonte)
                if fig_rendimentos:
                    st.plotly_chart(fig_rendimentos, use_container_width=True)

        # Evolução da poupança
        if not historico_poupanca.empty:
            fig_evolucao = visualizations.plot_evolucao_poupanca(
                historico_poupanca)
            if fig_evolucao:
                st.plotly_chart(fig_evolucao, use_container_width=True)

    with tab2:
        st.subheader("📊 Análise Mensal Comparativa")

        # Calcular resumos mensais
        resumos_mensais = []

        if not rendimentos_df.empty or not gastos_df.empty:
            # Obter todos os meses únicos
            meses_rendimentos = set()
            meses_gastos = set()

            if not rendimentos_df.empty:
                rendimentos_df['data'] = pd.to_datetime(rendimentos_df['data'])
                meses_rendimentos = set(
                    rendimentos_df['data'].dt.strftime('%Y-%m'))

            if not gastos_df.empty:
                gastos_df['data'] = pd.to_datetime(gastos_df['data'])
                meses_gastos = set(gastos_df['data'].dt.strftime('%Y-%m'))

            todos_meses = sorted(meses_rendimentos.union(meses_gastos))

            for mes in todos_meses:
                resumo = calculator.calcular_resumo_mensal(
                    rendimentos_df, gastos_df, mes)
                resumos_mensais.append(resumo)

        if resumos_mensais:
            # Gráfico comparativo mensal
            fig_comparativo = visualizations.plot_comparativo_mensal(
                resumos_mensais)
            if fig_comparativo:
                st.plotly_chart(fig_comparativo, use_container_width=True)

            # Tabela de resumos mensais
            st.subheader("📋 Tabela Resumo Mensal")

            df_resumos = pd.DataFrame(resumos_mensais)
            df_resumos['total_rendimentos'] = df_resumos['total_rendimentos'].apply(
                lambda x: f"R\$ {x:,.2f}")
            df_resumos['total_gastos'] = df_resumos['total_gastos'].apply(
                lambda x: f"R\$ {x:,.2f}")
            df_resumos['saldo_mensal'] = df_resumos['saldo_mensal'].apply(
                lambda x: f"R\$ {x:,.2f}")

            st.dataframe(
                df_resumos,
                column_config={
                    "mes_ano": "Mês/Ano",
                    "total_rendimentos": "Rendimentos",
                    "total_gastos": "Gastos",
                    "saldo_mensal": "Saldo"
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("📊 Adicione rendimentos e gastos para ver a análise mensal")

    with tab3:
        st.subheader("�� Exportar Dados")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Exportar para CSV:**")

            if st.button("📥 Exportar Rendimentos"):
                if not rendimentos_df.empty:
                    csv_rendimentos = rendimentos_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download Rendimentos.csv",
                        data=csv_rendimentos,
                        file_name="rendimentos.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ Nenhum rendimento para exportar")

            if st.button("📥 Exportar Gastos"):
                if not gastos_df.empty:
                    csv_gastos = gastos_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download Gastos.csv",
                        data=csv_gastos,
                        file_name="gastos.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ Nenhum gasto para exportar")

            if st.button("📥 Exportar Histórico Poupança"):
                if not historico_poupanca.empty:
                    csv_poupanca = historico_poupanca.to_csv(index=False)
                    st.download_button(
                        label="💾 Download Poupanca.csv",
                        data=csv_poupanca,
                        file_name="historico_poupanca.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ Nenhum histórico para exportar")

        with col2:
            st.write("**Backup Completo:**")

            if st.button("📦 Gerar Backup JSON"):
                backup_data = data_manager.data
                backup_json = json.dumps(
                    backup_data, indent=2, ensure_ascii=False)

                st.download_button(
                    label="💾 Download Backup Completo",
                    data=backup_json,
                    file_name=f"backup_financas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

            st.write("**Restaurar Backup:**")

            uploaded_file = st.file_uploader(
                "📁 Escolher arquivo JSON", type=['json'])

            if uploaded_file is not None:
                if st.button("🔄 Restaurar Backup"):
                    try:
                        backup_data = json.load(uploaded_file)
                        data_manager.data = backup_data
                        if data_manager.save_data():
                            st.success("✅ Backup restaurado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao restaurar backup")
                    except json.JSONDecodeError:
                        st.error("❌ Arquivo JSON inválido")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")

# Sidebar com informações adicionais


def sidebar_info():
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Estatísticas Rápidas")

    # Estatísticas rápidas
    rendimentos_df = data_manager.get_rendimentos_df()
    gastos_df = data_manager.get_gastos_df()
    saldo_poupanca = data_manager.data['poupanca']['saldo_atual']

    if not rendimentos_df.empty:
        total_rendimentos = rendimentos_df['valor'].sum()
        st.sidebar.metric("�� Total Rendimentos",
                          f"R\$ {total_rendimentos:,.2f}")

    if not gastos_df.empty:
        total_gastos = gastos_df['valor'].sum()
        st.sidebar.metric("💸 Total Gastos", f"R\$ {total_gastos:,.2f}")

    st.sidebar.metric("🏦 Saldo Poupança", f"R\$ {saldo_poupanca:,.2f}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Sobre o App")
    st.sidebar.info(
        "Dashboard de Finanças Pessoais desenvolvido com Streamlit. "
        "Gerencie seus rendimentos, gastos e poupança de forma simples e intuitiva."
    )

    st.sidebar.markdown("### 🔧 Versão")
    st.sidebar.text("v1.0.0")


if __name__ == "__main__":
    # Executar sidebar info
    sidebar_info()

    # Executar aplicação principal
    main()
