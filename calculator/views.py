from django.shortcuts import render
from .models import Consumer
from .services.calculator_python import calculator
from .forms import ConsumerForm
from django.shortcuts import redirect
from django.db.models import Q

def calculate_savings(request):
    if request.method == 'POST':
        consumption1 = int(request.POST['consumption1'])
        consumption2 = int(request.POST['consumption2'])
        consumption3 = int(request.POST['consumption3'])
        distributor_tax = float(request.POST['distributor_tax'])
        tax_type = request.POST['tax_type']

        # Calcular economia usando a função da calculadora
        annual_savings, monthly_savings, applied_discount, coverage = calculator(
            [consumption1, consumption2, consumption3],
            distributor_tax,
            tax_type
        )

        return render(request, 'calculator/savings_result.html', {
            'annual_savings': round(annual_savings, 2),
            'monthly_savings': round(monthly_savings, 2),
            'applied_discount': applied_discount,
            'coverage': coverage
        })

    return render(request, 'calculator/calculator_form.html')

def list_consumers(request):
    """
    Recupera os consumidores do banco de dados, aplica os filtros e envia os dados para o template.
    """
    # Obter os parâmetros de filtro do request
    consumer_type = request.GET.get('consumer_type')
    consumption_range = request.GET.get('consumption_range')

    # Obter todos os consumidores
    consumers = Consumer.objects.all()

    # Aplicar filtros
    if consumer_type:
        consumers = consumers.filter(discount_rule__consumer_type=consumer_type)
    if consumption_range:
        # Para o intervalo de consumo, podemos usar a consulta Q para filtrar entre os valores
        min_consumption, max_consumption = map(int, consumption_range.split('-'))
        consumers = consumers.filter(consumption__gte=min_consumption, consumption__lte=max_consumption)

    # Preparar os dados para enviar ao template
    data = []
    for consumer in consumers:
        discount_value = consumer.discount_rule.discount_value
        annual_savings, _, _, _ = calculator([consumer.consumption]*3, consumer.distributor_tax, consumer.discount_rule.consumer_type)
        data.append({
            'consumer': consumer,
            'annual_savings': round(annual_savings, 2),
            'discount_value': discount_value,
        })

    return render(request, 'consumer/list_consumers.html', {'data': data})


def create_consumer(request):
    """
    Cria uma visualização para realizar a inclusão de consumidores.
    A visualização deve:
    - Receber uma solicitação POST com os dados para registrar
    - Se os dados forem válidos (validar documento), criar e salvar um novo objeto Consumer associado à regra de desconto correta
    - Redirecionar para o template que lista todos os consumidores
    """
    if request.method == 'POST':
        form = ConsumerForm(request.POST)
        if form.is_valid():
            consumer = form.save()
            return redirect('list_consumers')
    else:
        form = ConsumerForm()
    return render(request, 'consumer/create_consumer.html', {'form': form})