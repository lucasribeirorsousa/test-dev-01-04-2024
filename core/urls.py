from django.contrib import admin
from django.urls import path
from calculator.views import (
    calculate_savings, 
    list_consumers, 
    create_consumer,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('calculate/', calculate_savings, name='calculate_savings'),
    path("list_consumers/", list_consumers, name="list_consumers"),
    path('create_consumer/', create_consumer, name='create_consumer'),
]
