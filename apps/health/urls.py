from django.urls import path
from . import views

urlpatterns = [

    path('', views.health, name='health'),

    # 🆕 Crear evento médico
    path('health_form/', views.health_form_edit, name='health_form'),

    # 👁️ Ver detalles del animal
    path('health_details/<int:animal_id>/',
         views.health_detail, name='health_detail'),

    # ✏️ Editar evento médico
    path('health_form/<int:event_id>/',
         views.health_form_edit, name='health_form_edit'),

    # 🔴 Eliminar evento médico
    path('health_delete/<int:event_id>/',
         views.health_delete, name='health_delete'),
]
