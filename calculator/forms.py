
from django import forms
from .models import Consumer

class ConsumerForm(forms.ModelForm):
    class Meta:
        model = Consumer
        fields = ['name', 'document', 'zip_code', 'city', 'state', 'consumption', 'distributor_tax', 'discount_rule']

    def clean_document(self):
        document = self.cleaned_data['document']
        # Implemente a lógica de validação do documento aqui, se necessário
        # Por exemplo, você pode verificar se o documento já está sendo usado por outro consumidor
        return document
