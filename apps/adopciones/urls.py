from django.urls import path
from . import views

urlpatterns = [

    path('adopciones', views.adopciones, name='adopciones'),

    # 🆕 Crear adopción
    path('adopciones_form', views.adopciones_form, name='adopciones_form'),

    # ✏️ Editar adopción
    path('adopciones_form/<int:adoption_id>/',
         views.adopciones_form, name='adopciones_form_edit'),

    # 🔴 Eliminar adopción
    path('adopciones_delete/<int:adoption_id>/',
         views.adopciones_delete, name='adopciones_delete'),

    # 👁 Ver detalles
    path('adopciones_details/<int:adoption_id>/',
         views.adopciones_details, name='adopciones_details'),
]
