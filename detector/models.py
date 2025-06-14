# detector/models.py
from django.db import models
from django.utils import timezone

class Transacao(models.Model):
    id_transacao_externo = models.CharField(max_length=100, unique=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()
    id_cliente = models.CharField(max_length=100)
    ip_cliente = models.GenericIPAddressField(null=True, blank=True)
    cidade_cliente = models.CharField(max_length=100, null=True, blank=True)
    pais_cliente = models.CharField(max_length=100, null=True, blank=True)
    processada = models.BooleanField(default=False)

    def __str__(self):
        return self.id_transacao_externo

class Alerta(models.Model):
    STATUS_CHOICES = (
        ('Pendente', 'Pendente de Análise'),
        ('Confirmada', 'Fraude Confirmada'),
        ('Segura', 'Transação Segura'),
    )

    transacao = models.OneToOneField(Transacao, on_delete=models.CASCADE)
    motivo = models.TextField()
    score_fraude = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente')
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Alerta para {self.transacao.id_transacao_externo}"