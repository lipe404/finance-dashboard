Um app simples e poderoso para organizar, visualizar e analisar suas finanças pessoais. Construído com Python, Streamlit, Pandas e Plotly, este projeto oferece visualizações interativas (linhas, barras, pizza) e cálculos úteis como evolução de saldo, fluxo de caixa, gastos por categoria, e mais.

**Principais Recursos**

* Interface web interativa com Streamlit, responsiva e de fácil uso
* Importação e gestão de dados financeiros (CSV/JSON)
* Cálculos automáticos:

  * Total de receitas e despesas
  * Saldo atual e evolução do saldo (com destaque para depósitos/saques)
  * Gastos por categoria e por período
  * Tendências (mensal, semanal)
* Visualizações com Plotly (tooltips, zoom/pan, modo escuro/claro):

  * Linha/área para evolução do saldo
  * Barras para gastos por categoria
  * Pizza/Donut para distribuição de despesas
* Estrutura de código modular:

  * DataManager: leitura/escrita de dados
  * FinanceCalculator: regras e agregações financeiras
  * FinanceVisualizations: construção dos gráficos em Plotly
* Fácil de executar localmente e pronto para deploy no Streamlit Community Cloud

**Estrutura do Projeto**

finance-dashboard/
├─ app.py
├─ calculations.py
├─ data_manager.py
├─ visualizations.py
├─ requirements.txt

**Pré-requisitos**

* Python 3.9+ (recomendado 3.10/3.11)
* Pip e virtualenv (ou Poetry/UV, se preferir)

**Clonar o repositório**

git clone https://github.com/SEU_USUARIO/finance-dashboard.git
cd finance-dashboard

**Criar e ativar o ambiente virtual**

macOS/Linux

python -m venv .venv
source .venv/bin/activate

Windows (PowerShell)

python -m venv .venv
.venv\Scripts\Activate.ps1

**Arquitetura e Responsabilidades**

* app.py
  * Configurações da página (título, ícone, layout)
  * Orquestra a interface: filtros, inputs, upload de dados, seleção de períodos/categorias
  * Chama os métodos do DataManager, FinanceCalculator e FinanceVisualizations
* data_manager.py (DataManager)
  * Leitura/escrita de dados (CSV/JSON)
  * Normalização de colunas e tipagem (datas, valores)
  * Métodos auxiliares para obter dados filtrados por período, tipo (receita/despesa), categoria, etc.
* calculations.py (FinanceCalculator)
  * Agregações: somas, médias, saldos, totais por categoria
  * Evolução do saldo (acumulado) com base em receitas/depósitos e despesas/saques
  * Projeções simples (ex.: saldo mensal, tendência)
* visualizations.py (FinanceVisualizations)
  * Criação de figuras Plotly (px e go)
  * Estilização: cores, títulos, tooltips, marcadores
  * Exemplos de charts: evolução do saldo, gastos por categoria, distribuição por tipo
