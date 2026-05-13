from apps.donaciones.models import Donacion
from django.db import transaction


class DonationService:

    # =========================
    # 🟢 CREATE
    # =========================
    @staticmethod
    @transaction.atomic
    def create_donation(donante, donante_email='', donante_phone='',
                        date=None, donation_type=None, status='Pendiente',
                        amount=None, payment_method='', description=''):
        """
        Crea una nueva donación en el sistema.
        Soporta donaciones monetarias (con amount y payment_method) y materiales.
        """
        donation = Donacion.objects.create(
            donante=donante,
            donante_email=donante_email or '',
            donante_phone=donante_phone or '',
            date=date,
            donation_type=donation_type,
            status=status,
            amount=amount,
            payment_method=payment_method or '',
            description=description or '',
        )
        return donation

    # =========================
    # 🔵 READ (uno)
    # =========================
    @staticmethod
    def get_donation_by_id(donation_id):
        return Donacion.objects.filter(id=donation_id).first()

    # =========================
    # 🔵 READ (lista)
    # =========================
    @staticmethod
    def list_donaciones():
        """Devuelve todas las donaciones ordenadas por fecha descendente."""
        return Donacion.objects.filter(is_active=True).order_by("-date", "-created_at")

    # =========================
    # 🟡 UPDATE
    # =========================
    @staticmethod
    @transaction.atomic
    def update_donation(donation_id, **kwargs):
        """
        Actualiza una donación existente.
        Solo modifica los campos presentes en allowed_fields.
        """
        donation = Donacion.objects.filter(id=donation_id).first()

        if not donation:
            return None

        allowed_fields = [
            "donante",
            "donante_email",
            "donante_phone",
            "date",
            "donation_type",
            "status",
            "amount",
            "payment_method",
            "description",
        ]

        for attr, value in kwargs.items():
            if attr in allowed_fields:
                setattr(donation, attr, value)

        donation.save()
        return donation

    # =========================
    # 🔴 DELETE
    # =========================
    @staticmethod
    @transaction.atomic
    def delete_donation(donation_id):
        donation = Donacion.objects.filter(id=donation_id).first()
        if not donation:
            return False
        donation.is_active = False
        donation.save(update_fields=['is_active'])
        return True
