from django.urls import path
from . import views

urlpatterns = [
    path('', views.owners, name='owners'),

    #  Crear propietario
    path('owners_form/',
         views.owners_form_edit, name="owners_form"),

    # ✏️ Editar propietario
    path('owners_form/<int:owner_id>/',
         views.owners_form_edit, name="owners_form_edit"),

    # Eliminar propietario
    path('owners_delete/<int:owner_id>/',
         views.owners_delete, name="owners_delete"),

    # 👁 Ver detalles
    path('owners_details/<int:owner_id>/',
         views.owners_details, name="owners_details"),
]
