# signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Consumer, DiscountRule
import pandas as pd

@receiver(post_migrate)
def populate_consumers_from_excel(sender, **kwargs):
    if sender.name == 'calculator':
        consumers_data = pd.read_excel('consumers.xlsx')

        for index, row in consumers_data.iterrows():
            name = row['Nome']
            document = row['Documento']
            city = row['Cidade']
            state = row['Estado']
            consumption = row['Consumo(kWh)']
            consumer_type = row['Tipo']
            cover_value = row['Cobertura(%)']
            distributor_tax = row['Tarifa da Distribuidora']

            # Associar o consumidor com a regra de desconto correta
            discount_rule, _ = DiscountRule.objects.get_or_create(
                consumer_type=consumer_type,
                cover_value=cover_value,
                defaults={
                    'discount_value': 0  # Supondo que o desconto seja opcional
                }
            )

            consumer, _ = Consumer.objects.get_or_create(
                document=document,
                defaults={
                    'name': name,
                    'city': city,
                    'state': state,
                    'consumption': consumption,
                    'distributor_tax': distributor_tax,
                    'discount_rule': discount_rule
                }
            )

            print(f"Consumer {name} created/updated successfully!")
