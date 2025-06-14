from django.contrib import admin
from .models import Transacao, Alerta

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('id_transacao_externo', 'valor', 'timestamp', 'id_cliente', 'pais_cliente', 'processada')
    list_filter = ('processada', 'pais_cliente')
    search_fields = ('id_transacao_externo', 'id_cliente')

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ('transacao', 'score_fraude', 'status', 'data_criacao')
    list_filter = ('status',)
    autocomplete_fields = ('transacao',)