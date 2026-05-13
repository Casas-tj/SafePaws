from apps.health.models import MedicalEvent
from apps.animales.models import Animal
from django.db import transaction
from django.db.models import Count, Q


class HealthService:

    # =========================
    # 🟢 CREATE
    # =========================
    @staticmethod
    @transaction.atomic
    def create_event(animal_id, event_type, description, incident_date):
        event = MedicalEvent.objects.create(
            animal_id=animal_id,
            event_type=event_type,
            description=description,
            incident_date=incident_date,
        )
        return event

    # =========================
    # 🔵 READ (un evento)
    # =========================
    @staticmethod
    def get_event_by_id(event_id):
        event = MedicalEvent.objects.select_related('animal__owner').filter(
            id=event_id, is_active=True
        ).first()
        if event:
            HealthService._add_labels(event)
        return event

    # =========================
    # 🔵 READ (todos los eventos activos)
    # =========================
    @staticmethod
    def list_events():
        events = MedicalEvent.objects.select_related('animal__owner').filter(
            is_active=True
        ).order_by('-incident_date')
        for e in events:
            HealthService._add_labels(e)
        return events

    # ===========================================
    # 🔵 READ (eventos de un animal - Vista 2)
    # ===========================================
    @staticmethod
    def list_events_by_animal(animal_id, show_all=False):
        """
        Devuelve las atenciones de un animal.
        Por defecto devuelve las 5 más recientes.
        Con show_all=True devuelve todas.
        """
        qs = MedicalEvent.objects.filter(
            animal_id=animal_id,
            is_active=True
        ).order_by('-incident_date')

        if not show_all:
            qs = qs[:5]

        events = list(qs)
        for e in events:
            HealthService._add_labels(e)
        return events

    # ====================================
    # 🔵 READ (animales para Vista 1)
    # ====================================
    @staticmethod
    def list_animals():
        """
        Devuelve la lista de animales activos para la Vista 1 (lista de animales).
        Añade el número de atenciones médicas registradas a cada animal.
        """
        from django.db.models import Count

        animals = Animal.objects.filter(is_active=True).select_related(
            'owner'
        ).annotate(
            total_atenciones=Count(
                'medical_events',
                filter=Q(medical_events__is_active=True)
            )
        ).order_by('name')

        for animal in animals:
            animal.owner_display = (
                f"{animal.owner.name} {animal.owner.last_name}".strip()
                if animal.owner else "—"
            )

        return animals

    # =========================
    # 🟡 UPDATE
    # =========================
    @staticmethod
    @transaction.atomic
    def update_event(event_id, **kwargs):
        event = MedicalEvent.objects.filter(
            id=event_id, is_active=True).first()
        if not event:
            return None

        allowed = ['animal_id', 'event_type', 'description', 'incident_date']
        for key, value in kwargs.items():
            if key in allowed:
                setattr(event, key, value)
        event.save()
        return event

    # =========================
    # 🔴 DELETE
    # =========================
    @staticmethod
    @transaction.atomic
    def delete_event(event_id):

        event = MedicalEvent.objects.filter(id=event_id).first()

        if not event:
            return False

        event.is_active = False
        event.save(update_fields=['is_active'])
        return True

    # =========================
    # 🏷️ LABELS
    # =========================
    @staticmethod
    def _add_labels(event):
        """Añade atributos de presentación a un evento sin tocar el modelo."""

        event.type_label = dict(MedicalEvent.TYPE_CHOICES).get(
            event.event_type, event.event_type
        )

        event.status_label = "Activo" if event.is_active else "Eliminado"

        event.owner_display = (
            f"{event.animal.owner.name} {event.animal.owner.last_name}".strip()
            if event.animal.owner else "—"
        )
