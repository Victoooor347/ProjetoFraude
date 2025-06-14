# detector/views.py
import csv
import io
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Transacao, Alerta
from .regras_fraude import analisar_transacao_com_ml
from .utils import processar_csv
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    # Lógica dos cards de estatísticas (continua a mesma)
    todos_alertas = Alerta.objects.all()
    stats = {
        'total_alertas': todos_alertas.count(),
        'pendentes': todos_alertas.filter(status='Pendente').count(),
        'confirmadas': todos_alertas.filter(status='Confirmada').count(),
        'seguras': todos_alertas.filter(status='Segura').count(),
    }

    alertas_pendentes = todos_alertas.filter(status='Pendente')

    # --- LÓGICA PARA GRÁFICO 1: TOP 5 ALERTAS ---
    top_alertas = alertas_pendentes.order_by('-score_fraude')[:5]
    top_alertas_labels = [alerta.transacao.id_transacao_externo for alerta in top_alertas]
    top_alertas_data = [round(alerta.score_fraude, 2) for alerta in top_alertas]
    # Invertemos para o gráfico mostrar o maior score no topo
    top_alertas_labels.reverse()
    top_alertas_data.reverse()

    # --- LÓGICA PARA GRÁFICO 2: DISTRIBUIÇÃO DE RISCO ---
    risco_alto = alertas_pendentes.filter(score_fraude__gte=90).count()
    risco_medio = alertas_pendentes.filter(score_fraude__gte=70, score_fraude__lt=90).count()
    risco_baixo = alertas_pendentes.filter(score_fraude__lt=70).count()
    distribuicao_data = [risco_alto, risco_medio, risco_baixo]

    # Tabela de Alertas Recentes (continua a mesma)
    alertas_recentes = alertas_pendentes.order_by('-data_criacao')[:10]

    contexto = {
        'stats': stats,
        'alertas': alertas_recentes,
        'top_alertas_labels': top_alertas_labels,
        'top_alertas_data': top_alertas_data,
        'distribuicao_data': distribuicao_data,
    }

    return render(request, 'detector/dashboard.html', contexto)


@login_required
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('arquivo_csv')
        if not csv_file or not csv_file.name.endswith('.csv'):
            messages.error(request, 'Este não é um arquivo CSV válido.')
            return redirect('upload_csv')

        csv_content_string = csv_file.read().decode('UTF-8')

        # A FORMA DE CHAMAR A TAREFA MUDOU
        processar_csv(csv_content_string) # Não precisa mais do .delay()

        messages.success(request, 'Arquivo recebido! O processamento foi agendado e acontecerá em segundo plano.')
        return redirect('dashboard')

    return render(request, 'detector/upload.html')


@login_required
def alerta_detalhe(request, alerta_id):
    alerta = get_object_or_404(Alerta, id=alerta_id)
    return render(request, 'detector/alerta_detalhe.html', {'alerta': alerta})

@login_required
def marcar_status_alerta(request, alerta_id, novo_status):
    if request.method == 'POST':
        alerta = get_object_or_404(Alerta, id=alerta_id)
        if novo_status in ['Confirmada', 'Segura']:
            alerta.status = novo_status
            alerta.save()
            messages.success(request, f'Alerta marcado como "{novo_status}".')
    return redirect('alerta_detalhe', alerta_id=alerta.id)







# # detector/views.py
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .tasks import processar_csv_task  # Importe a nossa nova tarefa

# # ... as outras views (dashboard, alerta_detalhe) continuam iguais ...

# def upload_csv(request):
#     if request.method == 'POST':
#         csv_file = request.FILES.get('arquivo_csv')

#         if not csv_file or not csv_file.name.endswith('.csv'):
#             messages.error(request, 'Este não é um arquivo CSV válido.')
#             return redirect('upload_csv')

#         # Lê o conteúdo do arquivo para uma string
#         csv_content_string = csv_file.read().decode('UTF-8')

#         # MÁGICA DO CELERY ACONTECE AQUI!
#         # Chama a tarefa para ser executada em segundo plano.
#         # O .delay() envia a tarefa para a fila e retorna imediatamente.
#         processar_csv_task.delay(csv_content_string)

#         messages.success(request, 'Arquivo recebido! O processamento foi iniciado em segundo plano. Os resultados aparecerão no dashboard em breve.')
#         return redirect('dashboard')

#     return render(request, 'detector/upload.html')