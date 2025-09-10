import json
import pandas as pd
from datetime import datetime
import os


class DataManager:
    def __init__(self, data_file='finance_data.json'):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        """Carrega dados do arquivo JSON ou cria estrutura inicial"""
        default_data = {
            'rendimentos': [],
            'gastos': [],
            'poupanca': {
                'saldo_atual': 0.0,
                'historico': [],
                'taxa_cdi': 13.75
            },
            'objetivos': []
        }

        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Garantir que todas as chaves existam
                for key in default_data:
                    if key not in data:
                        data[key] = default_data[key]
                return data
            except (json.JSONDecodeError, FileNotFoundError):
                return default_data
        return default_data

    def save_data(self):
        """Salva dados no arquivo JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False

    def add_rendimento(self, fonte, valor, data, descricao=""):
        """Adiciona um novo rendimento"""
        rendimento = {
            'id': len(self.data['rendimentos']) + 1,
            'fonte': fonte,
            'valor': float(valor),
            'data': data.strftime('%Y-%m-%d'),
            'descricao': descricao,
            'timestamp': datetime.now().isoformat()
        }
        self.data['rendimentos'].append(rendimento)
        return self.save_data()

    def add_gasto(self, categoria, valor, data, descricao=""):
        """Adiciona um novo gasto"""
        gasto = {
            'id': len(self.data['gastos']) + 1,
            'categoria': categoria,
            'valor': float(valor),
            'data': data.strftime('%Y-%m-%d'),
            'descricao': descricao,
            'timestamp': datetime.now().isoformat()
        }
        self.data['gastos'].append(gasto)
        return self.save_data()

    def update_poupanca(self, operacao, valor, descricao=""):
        """Atualiza saldo da poupança (deposito ou saque)"""
        if operacao == 'deposito':
            self.data['poupanca']['saldo_atual'] += float(valor)
        elif operacao == 'saque':
            self.data['poupanca']['saldo_atual'] -= float(valor)

        historico_item = {
            'id': len(self.data['poupanca']['historico']) + 1,
            'operacao': operacao,
            'valor': float(valor),
            'saldo_anterior': self.data['poupanca']['saldo_atual'] - (float(valor) if operacao == 'deposito' else -float(valor)),
            'saldo_atual': self.data['poupanca']['saldo_atual'],
            'data': datetime.now().strftime('%Y-%m-%d'),
            'descricao': descricao,
            'timestamp': datetime.now().isoformat()
        }
        self.data['poupanca']['historico'].append(historico_item)
        return self.save_data()

    def update_taxa_cdi(self, nova_taxa):
        """Atualiza a taxa CDI"""
        self.data['poupanca']['taxa_cdi'] = float(nova_taxa)
        return self.save_data()

    def add_objetivo(self, nome, valor_meta, prazo_meses, descricao=""):
        """Adiciona um novo objetivo de poupança"""
        objetivo = {
            'id': len(self.data['objetivos']) + 1,
            'nome': nome,
            'valor_meta': float(valor_meta),
            'prazo_meses': int(prazo_meses),
            'descricao': descricao,
            'data_criacao': datetime.now().strftime('%Y-%m-%d'),
            'ativo': True
        }
        self.data['objetivos'].append(objetivo)
        return self.save_data()

    def get_rendimentos_df(self):
        """Retorna DataFrame dos rendimentos"""
        if not self.data['rendimentos']:
            return pd.DataFrame()
        return pd.DataFrame(self.data['rendimentos'])

    def get_gastos_df(self):
        """Retorna DataFrame dos gastos"""
        if not self.data['gastos']:
            return pd.DataFrame()
        return pd.DataFrame(self.data['gastos'])

    def get_poupanca_historico_df(self):
        """Retorna DataFrame do histórico da poupança"""
        if not self.data['poupanca']['historico']:
            return pd.DataFrame()
        return pd.DataFrame(self.data['poupanca']['historico'])

    def delete_rendimento(self, rendimento_id):
        """Remove um rendimento"""
        self.data['rendimentos'] = [
            r for r in self.data['rendimentos'] if r['id'] != rendimento_id]
        return self.save_data()

    def delete_gasto(self, gasto_id):
        """Remove um gasto"""
        self.data['gastos'] = [
            g for g in self.data['gastos'] if g['id'] != gasto_id]
        return self.save_data()
