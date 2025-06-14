# detector/tasks.py
import csv
import io
from datetime import datetime
from background_task import background # <--- MUDANÇA NA IMPORTAÇÃO
from .models import Transacao, Alerta
from .regras_fraude import analisar_transacao_com_ml

# O DECORATOR MUDOU!
@background(schedule=1) # 'schedule=1' significa: "execute 1 segundo depois de ser chamado"
def processar_csv(csv_content_string):
    """
    Esta tarefa agora usa o django-background-tasks.
    """
    print("▶️ Background Task: Recebi a tarefa! Iniciando processamento de CSV...")

    # O RESTO DA LÓGICA DENTRO DA FUNÇÃO É EXATAMENTE A MESMA DE ANTES
    io_string = io.StringIO(csv_content_string)
    next(io_string)
    transacoes_criadas = 0
    alertas_gerados = 0
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        if Transacao.objects.filter(id_transacao_externo=column[0]).exists():
            continue
        transacao, created = Transacao.objects.update_or_create(
            id_transacao_externo=column[0],
            defaults={ 'valor': float(column[1]), 'timestamp': datetime.strptime(column[2], '%Y-%m-%d %H:%M:%S'), 'id_cliente': column[3], 'ip_cliente': column[4], 'cidade_cliente': column[5], 'pais_cliente': column[6], 'processada': True }
        )
        transacoes_criadas += 1
        score, motivos = analisar_transacao_com_ml(transacao)
        if motivos:
            Alerta.objects.create(transacao=transacao, motivo="\n".join(motivos), score_fraude=score)
            alertas_gerados += 1

    resultado = f"Processamento concluído: {transacoes_criadas} novas transações, {alertas_gerados} novos alertas."
    print(f"✅ Background Task: {resultado}")
    return resultado 