# detector/regras_fraude.py
import joblib
import pandas as pd
from django.conf import settings
import os
from .models import Transacao # <--- ADICIONE ESTA IMPORTAÇÃO NO TOPO
from django.db.models import Avg, Count

# --- Carregamento do Modelo de ML ---
# O caminho para o nosso modelo salvo
CAMINHO_MODELO = os.path.join(settings.BASE_DIR, 'modelo_fraude.joblib')
# Carregamos o modelo em memória uma única vez quando o Django inicia
MODELO_ML = joblib.load(CAMINHO_MODELO)
print("🤖 Modelo de Machine Learning carregado com sucesso!")
# --- Fim do Carregamento ---


def analisar_transacao_com_ml(transacao):
    """
    Analisa uma única transação usando o modelo de ML treinado
    e buscando o histórico do cliente no banco de dados.
    """
    # 1. Buscar o histórico do cliente no banco de dados
    id_cliente = transacao.id_cliente
    # Pega todas as transações do cliente, exceto a atual que estamos analisando
    historico_cliente = Transacao.objects.filter(id_cliente=id_cliente).exclude(pk=transacao.pk)

    if historico_cliente.exists():
        # Se o cliente tem histórico, calcula as estatísticas
        agregados = historico_cliente.aggregate(media=Avg('valor'), contagem=Count('id'))
        media_valor_cliente = agregados['media']
        total_transacoes_cliente = agregados['contagem']
    else:
        # Se for um cliente novo, usamos 0 como base
        media_valor_cliente = 0
        total_transacoes_cliente = 0

    # 2. Criar um DataFrame para a predição com as mesmas 4 features do treinamento
    dados = {
        'valor': [float(transacao.valor)],
        'hora': [transacao.timestamp.hour],
        'media_valor_cliente': [media_valor_cliente],
        'total_transacoes_cliente': [total_transacoes_cliente]
    }
    transacao_df = pd.DataFrame(dados)

    # 3. Usar o modelo para fazer a predição (o resto é igual a antes)
    predicao = MODELO_ML.predict(transacao_df)

    if predicao[0] == -1:
        score_anomalia = MODELO_ML.decision_function(transacao_df)
        score_final = min(abs(score_anomalia[0]) * 200, 100)
        motivo = f"Anomalia detectada pelo modelo de IA (Score de Anomalia: {score_anomalia[0]:.2f})"
        return score_final, [motivo]

    return 0, []

# Você pode manter a função antiga (analisar_transacao) aqui se quiser, para comparar