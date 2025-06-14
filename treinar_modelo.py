# treinar_modelo.py
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

print("🚀 Iniciando o treinamento do modelo APRIMORADO...")

# 1. Carregar os dados históricos
try:
    df = pd.read_csv('transacoes.csv')
except FileNotFoundError:
    print("❌ Erro: Arquivo 'transacoes.csv' não foi encontrado.")
    exit()

# 2. Engenharia de Features Avançada
print("🧠 Calculando novas features baseadas no comportamento do cliente...")
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hora'] = df['timestamp'].dt.hour

# Usando a mágica do pandas para calcular estatísticas por cliente
# Para cada transação, ele vai adicionar a média de valor e a contagem de transações daquele cliente
df['media_valor_cliente'] = df.groupby('id_cliente')['valor'].transform('mean')
df['total_transacoes_cliente'] = df.groupby('id_cliente')['id_cliente'].transform('count')

# Nossas novas features para o modelo!
features = ['valor', 'hora', 'media_valor_cliente', 'total_transacoes_cliente']
X = df[features]

print(f"Features utilizadas no treinamento: {features}")
print(f"Foram encontradas {len(X)} transações para o treinamento.")

# 3. Criar e Treinar o Modelo
model = IsolationForest(n_estimators=100, contamination='auto', random_state=42)
model.fit(X)

# 4. Salvar o novo modelo treinado
joblib.dump(model, 'modelo_fraude.joblib')

print("✅ Treinamento APRIMORADO concluído com sucesso!")
print("🧠 Novo modelo salvo como 'modelo_fraude.joblib'")