from django.urls import path
from . import views

urlpatterns = [

    # 📋 Lista de donaciones
    path('donaciones', views.donaciones, name="donaciones"),

    # 🆕 Crear捐赠
    path('donaciones_form',
         views.donaciones_form, name="donaciones_form"),

    # ✏️ Editar donación
    path('donaciones_form/<int:donation_id>/',
         views.donaciones_form, name="donaciones_form_edit"),

    # 🔴 Eliminar donación
    path('donaciones_delete/<int:donation_id>/',
         views.donaciones_delete, name="donaciones_delete"),

    # 👁 Ver detalles
    path('donaciones_details/<int:donation_id>/',
         views.donaciones_details, name="donaciones_details"),
]
