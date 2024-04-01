from django.db import models

class DiscountRule(models.Model):
    CONSUMER_TYPES = (
        ('Residencial', 'Residencial'),
        ('Comercial', 'Comercial'),
        ('Industrial', 'Industrial'),
    )

    CONSUMPTION_RANGES = (
        ('< 10.000 kWh', '< 10.000 kWh'),
        ('>= 10.000 kWh e <= 20.000 kWh', '>= 10.000 kWh e <= 20.000 kWh'),
        ('> 20.000 kWh', '> 20.000 kWh'),
    )

    consumer_type = models.CharField("Tipo de Consumidor", max_length=20, choices=CONSUMER_TYPES)
    consumption_range = models.CharField("Faixa de Consumo", max_length=30, choices=CONSUMPTION_RANGES)
    cover_value = models.FloatField("Valor de Cobertura")
    discount_value = models.FloatField("Valor de Desconto")

    def __str__(self):
        return f"{self.consumer_type} - {self.consumption_range}"
    
    
class Consumer(models.Model):
    name = models.CharField("Nome do Consumidor", max_length=128)
    document = models.CharField("Documento(CPF/CNPJ)", max_length=14, unique=True)
    zip_code = models.CharField("CEP", max_length=8, null=True, blank=True)
    city = models.CharField("Cidade", max_length=128)
    state = models.CharField("Estado", max_length=128)
    consumption = models.IntegerField("Consumo(kWh)", blank=True, null=True)
    distributor_tax = models.FloatField(
        "Tarifa da Distribuidora", blank=True, null=True
    )
    discount_rule = models.ForeignKey(DiscountRule, on_delete=models.CASCADE)


# TODO: You must populate the consumer table with the data provided in the file consumers.xlsx
#  and associate each one with the correct discount rule
