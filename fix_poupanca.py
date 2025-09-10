# fix_poupanca.py
import json
import os


def fix_data_structure():
    """Corrige a estrutura de dados se necessário"""
    data_file = 'finance_data.json'

    if os.path.exists(data_file):
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Verificar se a estrutura da poupança está correta
            if 'poupanca' in data:
                if 'historico' in data['poupanca']:
                    # Verificar se cada item do histórico tem as colunas necessárias
                    for item in data['poupanca']['historico']:
                        if 'saldo_atual' not in item and 'saldo' in item:
                            item['saldo_atual'] = item['saldo']
                            del item['saldo']

                # Salvar dados corrigidos
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                print("✅ Estrutura de dados corrigida com sucesso!")

        except Exception as e:
            print(f"❌ Erro ao corrigir dados: {e}")
    else:
        print("📁 Arquivo de dados não encontrado. Será criado na primeira execução.")


if __name__ == "__main__":
    fix_data_structure()
