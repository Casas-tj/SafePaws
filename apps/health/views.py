from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.core.decorators import permisos_requeridos, requiere_permiso
from apps.health.services.health_services import HealthService
from apps.animales.models import Animal


@permisos_requeridos('health.view_medicalevent')
def health(request):

    events = HealthService.list_events()

    animals = HealthService.list_animals()

    return render(request, 'health/health.html', {
        'events': events,
        'animals': animals,
        'headertitle': 'Historial Médico',
        'headersubtitle': 'Eventos médicos por animal',
        'btn_nuevo': 'Nuevo Registro Médico',
        'form_url': 'health_form',
        'nuevo_perm': "health.add_medicalevent",
        'btn_back': 'Volver',
        'back_url': 'home',
    })


@permisos_requeridos('health.view_medicalevent')
def health_detail(request, animal_id):
    """
    Muestra las atenciones médicas de un animal específico.
    Parámetro ?show=all → muestra todas. Por defecto: 5 más recientes.
    """
    animal = Animal.objects.select_related('owner').filter(
        id=animal_id
    ).first()

    if not animal:
        return redirect('health')

    show_all = request.GET.get('show') == 'all'

    events = HealthService.list_events_by_animal(animal_id, show_all=show_all)

    owner_display = (
        f"{animal.owner.name} {animal.owner.last_name}".strip()
        if animal.owner else "—"
    )

    return render(request, 'health/health_detail.html', {
        'animal': animal,
        'events': events,
        'show_all': show_all,
        'owner_display': owner_display,
        'headertitle': f'Atenciones de {animal.name}',
        'headersubtitle': f'{animal.species} · {owner_display}',
        'btn_back': 'Volver',
        'back_url': 'health',
    })


@login_required
def health_form_edit(request, event_id=None):
    """
    Crea o edita una atención médica.
    Si viene con ?animal_id en la URL GET, pre-selecciona el animal.
    Si viene con event_id, carga el evento para editar.
    Al guardar redirige a health_detail si hay animal, o a health si es general.
    """

    # =========================
    # 📋 GET → mostrar formulario
    # =========================
    if request.method == "GET":

        if event_id:
            requiere_permiso(request, 'health.change_medicalevent')
        else:
            requiere_permiso(request, 'health.add_medicalevent')

        event = None
        preselected_animal = None

        if event_id:
            event = HealthService.get_event_by_id(event_id)

            if not event:
                return redirect('health')

        animal_id_param = request.GET.get('animal_id')
        if animal_id_param:
            preselected_animal = Animal.objects.filter(
                id=animal_id_param, is_active=True
            ).first()

        animals = Animal.objects.filter(is_active=True).order_by('name')

        return render(request, 'health/health_form.html', {
            'event': event,
            'animals': animals,
            'preselected_animal': preselected_animal,
            'headertitle': 'Historial Médico',
            'headersubtitle': 'Editar Registro Médico' if event else 'Nuevo Registro Médico',
            'btn_back': 'Cancelar',
            'back_url': 'health',
        })

    # =========================
    # 💾 POST → guardar
    # =========================
    if request.method == 'POST':

        if event_id:
            requiere_permiso(request, 'health.change_medicalevent')
        else:
            requiere_permiso(request, 'health.add_medicalevent')

        animal_id = request.POST.get('animal_id')
        event_type = request.POST.get('event_type')
        description = request.POST.get('description')
        incident_date = request.POST.get('incident_date')

        data = {
            'animal_id': animal_id,
            'event_type': event_type,
            'description': description,
            'incident_date': incident_date,
        }

        if event_id:
            event = HealthService.update_event(event_id, **data)
            # Tras editar, volver al detalle del animal
            return redirect('health_detail', animal_id=event.animal_id if event else animal_id)
        else:
            HealthService.create_event(**data)
            # Si venía de un animal concreto, volver a su detalle
            if animal_id:
                return redirect('health_detail', animal_id=animal_id)
            return redirect('health')


# ❌ ELIMINAR EVENTO MÉDICO
@permisos_requeridos('health.delete_medicalevent')
def health_delete(request, event_id):
    """
    Soft delete de una atención médica.
    Redirige de vuelta al detalle del animal.
    """
    if request.method == 'POST':
        # Guardar animal_id antes de eliminar para redirigir correctamente
        event = HealthService.get_event_by_id(event_id)
        animal_id = event.animal_id if event else None

        HealthService.delete_event(event_id)

        if animal_id:
            return redirect('health_detail', animal_id=animal_id)

    return redirect('health')
