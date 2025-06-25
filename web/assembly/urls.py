from django.urls import path
from .views import assembly_to_c

urlpatterns = [
    path('decompile/', assembly_to_c, name='decompile'),
]
