from django.db.models import Sum, Count
from django.utils import timezone
from datetime import date
import json


class DashboardService:
    """
    Servicio centralizado para el dashboard de SafePaws.
    Agrega datos reales de todas las apps del sistema.
    """

    # ─────────────────────────────────────────────────────
    # 📊 PANEL PRINCIPAL — contadores para las métricas
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_panel_stats():
        from apps.animales.models import Animal
        from apps.adopciones.models import Adopcion
        from apps.donaciones.models import Donacion
        from apps.owners.models import Owner
        from apps.inventario.models import Product

        today = timezone.now().date()
        primer_dia_mes = today.replace(day=1)

        # ── Animales ─────────────────────────────
        total_animales = Animal.objects.filter(is_active=True).count()
        nuevos_mes = Animal.objects.filter(
            is_active=True,
            admission_date__gte=primer_dia_mes
        ).count()

        # ── Voluntarios ───────────────────────────
        total_voluntarios = Owner.objects.filter(
            is_volunteer=True, is_active=True
        ).count()

        # ── Donaciones monetarias confirmadas ─────
        total_donaciones = Donacion.objects.filter(
            is_active=True,
            donation_type='Monetaria',
            status__in=['Recibida', 'Procesada']
        ).aggregate(total=Sum('amount'))['total'] or 0

        donaciones_mes = Donacion.objects.filter(
            is_active=True,
            donation_type='Monetaria',
            status__in=['Recibida', 'Procesada'],
            date__gte=primer_dia_mes
        ).aggregate(total=Sum('amount'))['total'] or 0

        # ── Adopciones ────────────────────────────
        total_adopciones = Adopcion.objects.filter(is_active=True).count()
        adopciones_mes = Adopcion.objects.filter(
            is_active=True,
            adoption_date__gte=primer_dia_mes
        ).count()

        # ── Stock bajo (umbral ≤ 5) ───────────────
        stock_bajo = Product.objects.filter(
            is_active=True, quantity__lte=5
        ).count()

        return {
            'total_animales':    total_animales,
            'nuevos_mes':        nuevos_mes,
            'total_voluntarios': total_voluntarios,
            'total_donaciones':  total_donaciones,
            'donaciones_mes':    donaciones_mes,
            'total_adopciones':  total_adopciones,
            'adopciones_mes':    adopciones_mes,
            'stock_bajo':        stock_bajo,
        }

    # ─────────────────────────────────────────────────────
    # ❤️ ADOPCIONES RECIENTES
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_recent_adoptions(limit=3):
        from apps.adopciones.models import Adopcion
        return Adopcion.objects.select_related(
            'animal', 'owner'
        ).filter(is_active=True).order_by('-created_at')[:limit]

    # ─────────────────────────────────────────────────────
    # 💰 DONACIONES RECIENTES
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_recent_donations(limit=3):
        from apps.donaciones.models import Donacion
        return Donacion.objects.filter(
            is_active=True
        ).order_by('-date')[:limit]

    # ─────────────────────────────────────────────────────
    # ⚠️ ALERTAS DE STOCK BAJO
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_stock_alerts(limit=3):
        from apps.inventario.models import Product
        return Product.objects.filter(
            is_active=True, quantity__lte=5
        ).order_by('quantity')[:limit]

    # ─────────────────────────────────────────────────────
    # 🏥 ÚLTIMOS EVENTOS MÉDICOS
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_recent_medical_full(limit=5):
        from apps.health.models import MedicalEvent
        return MedicalEvent.objects.select_related('animal').filter(
            is_active=True
        ).order_by('-incident_date')[:limit]

    # ─────────────────────────────────────────────────────
    # 👥 VOLUNTARIOS: listas para tablas
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_volunteers_list(limit=5):
        from apps.owners.models import Owner
        return Owner.objects.filter(is_volunteer=True, is_active=True).order_by('-created_at')[:limit]

    @staticmethod
    def get_all_owners(limit=5):
        from apps.owners.models import Owner
        return Owner.objects.filter(is_active=True).order_by('-created_at')[:limit]

    # ─────────────────────────────────────────────────────
    # 📋 INCIDENCIAS: listas para tablas
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_open_medical_events(limit=5):
        from apps.health.models import MedicalEvent
        return MedicalEvent.objects.select_related('animal').filter(
            is_active=True
        ).order_by('-incident_date')[:limit]

    @staticmethod
    def get_recent_resolved_events(limit=5):
        from apps.health.models import MedicalEvent
        return MedicalEvent.objects.select_related('animal').filter(
            is_active=True, status='Resolved'
        ).order_by('-incident_date')[:limit]

    # ─────────────────────────────────────────────────────
    # 🐾 CHART: distribución por especie (doughnut)
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_species_chart_data():
        from apps.animales.models import Animal
        data = Animal.objects.filter(is_active=True).values(
            'species'
        ).annotate(total=Count('id')).order_by('-total')

        labels = [d['species'] for d in data]
        values = [d['total'] for d in data]
        return json.dumps({'labels': labels, 'values': values})

    # ─────────────────────────────────────────────────────
    # 📅 CHART: adopciones últimos 6 meses (line)
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_monthly_adoptions_chart():
        from apps.adopciones.models import Adopcion
        today = timezone.now().date()
        meses_es = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        labels, values = [], []

        for i in range(5, -1, -1):
            m = today.month - i
            y = today.year
            while m <= 0:
                m += 12
                y -= 1
            primer_dia = date(y, m, 1)
            ultimo_dia = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)

            count = Adopcion.objects.filter(
                is_active=True,
                adoption_date__gte=primer_dia,
                adoption_date__lt=ultimo_dia
            ).count()

            labels.append(meses_es[m - 1])
            values.append(count)

        return json.dumps({'labels': labels, 'values': values})

    # ─────────────────────────────────────────────────────
    # 💵 CHART: donaciones monetarias últimos 6 meses (bar)
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_monthly_donations_chart():
        from apps.donaciones.models import Donacion
        today = timezone.now().date()
        meses_es = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        labels, values = [], []

        for i in range(5, -1, -1):
            m = today.month - i
            y = today.year
            while m <= 0:
                m += 12
                y -= 1
            primer_dia = date(y, m, 1)
            ultimo_dia = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)

            total = Donacion.objects.filter(
                is_active=True,
                donation_type='Monetaria',
                status__in=['Recibida', 'Procesada'],
                date__gte=primer_dia,
                date__lt=ultimo_dia
            ).aggregate(t=Sum('amount'))['t'] or 0

            labels.append(meses_es[m - 1])
            values.append(float(total))

        return json.dumps({'labels': labels, 'values': values})

    # ─────────────────────────────────────────────────────
    # 🏥 EVENTOS MÉDICOS RECIENTES (alias)
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_recent_medical_events(limit=2):
        """Alias para get_recent_medical_full"""
        from apps.health.models import MedicalEvent
        return MedicalEvent.objects.select_related('animal').filter(
            is_active=True
        ).order_by('-incident_date')[:limit]

    # ─────────────────────────────────────────────────────
    # 🐾 VISTA ANIMALES: estadísticas
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_animales_stats():
        from apps.animales.models import Animal
        
        today = timezone.now().date()
        primer_dia_mes = today.replace(day=1)
        
        total = Animal.objects.filter(is_active=True).count()
        nuevos_mes = Animal.objects.filter(
            is_active=True, admission_date__gte=primer_dia_mes
        ).count()
        disponibles = Animal.objects.filter(is_active=True, status='Disponible').count()
        en_tratamiento = Animal.objects.filter(is_active=True, status='En Tratamiento').count()
        criticos = Animal.objects.filter(is_active=True, status='Critico').count()

        return {
            'total': total,
            'nuevos_mes': nuevos_mes,
            'disponibles': disponibles,
            'en_tratamiento': en_tratamiento,
            'criticos': criticos,
        }

    @staticmethod
    def get_recent_animals(limit=5):
        from apps.animales.models import Animal
        return Animal.objects.filter(is_active=True).order_by('-admission_date')[:limit]

    @staticmethod
    def get_animals_by_species():
        from apps.animales.models import Animal
        data = Animal.objects.filter(is_active=True).values(
            'species'
        ).annotate(total=Count('id')).order_by('-total')
        
        labels = [d['species'] for d in data]
        values = [d['total'] for d in data]
        return json.dumps({'labels': labels, 'values': values})

    @staticmethod
    def get_monthly_admissions():
        from apps.animales.models import Animal
        today = timezone.now().date()
        meses_es = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        labels, values = [], []

        for i in range(5, -1, -1):
            m = today.month - i
            y = today.year
            while m <= 0:
                m += 12
                y -= 1
            primer_dia = date(y, m, 1)
            ultimo_dia = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)

            count = Animal.objects.filter(
                is_active=True,
                admission_date__gte=primer_dia,
                admission_date__lt=ultimo_dia
            ).count()

            labels.append(meses_es[m - 1])
            values.append(count)

        return json.dumps({'labels': labels, 'values': values})

    @staticmethod
    def get_health_status():
        from apps.animales.models import Animal
        data = Animal.objects.filter(is_active=True).values(
            'status'
        ).annotate(total=Count('id')).order_by('-total')
        
        labels = [d['status'] for d in data]
        values = [d['total'] for d in data]
        return json.dumps({'labels': labels, 'values': values})

    # ─────────────────────────────────────────────────────
    # ❤️ VISTA ADOPCIONES: estadísticas
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_adopciones_stats():
        from apps.adopciones.models import Adopcion
        
        today = timezone.now().date()
        primer_dia_mes = today.replace(day=1)
        
        total = Adopcion.objects.filter(is_active=True).count()
        este_mes = Adopcion.objects.filter(
            is_active=True,
            adoption_date__gte=primer_dia_mes
        ).count()
        tasa_exito = 87  # placeholder

        return {
            'total_adopciones': total,
            'adopciones_mes': este_mes,
            'tasa_exito': tasa_exito,
            'pendientes': 18,  # placeholder
        }

    @staticmethod
    def get_adoptions_by_month():
        from apps.adopciones.models import Adopcion
        today = timezone.now().date()
        meses_es = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        labels, values = [], []

        for i in range(5, -1, -1):
            m = today.month - i
            y = today.year
            while m <= 0:
                m += 12
                y -= 1
            primer_dia = date(y, m, 1)
            ultimo_dia = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)

            count = Adopcion.objects.filter(
                is_active=True,
                adoption_date__gte=primer_dia,
                adoption_date__lt=ultimo_dia
            ).count()

            labels.append(meses_es[m - 1])
            values.append(count)

        return json.dumps({'labels': labels, 'values': values})

    @staticmethod
    def get_adoptions_by_species():
        from apps.adopciones.models import Adopcion
        data = Adopcion.objects.filter(is_active=True).select_related(
            'animal'
        ).values('animal__species').annotate(total=Count('id')).order_by('-total')
        
        labels = [d['animal__species'] for d in data]
        values = [d['total'] for d in data]
        return json.dumps({'labels': labels, 'values': values})

    @staticmethod
    def get_adoption_status_breakdown():
        from apps.adopciones.models import Adopcion
        data = Adopcion.objects.filter(is_active=True).values(
            'status'
        ).annotate(total=Count('id')).order_by('-total')
        
        labels = [d['status'] for d in data]
        values = [d['total'] for d in data]
        return json.dumps({'labels': labels, 'values': values})

    # ─────────────────────────────────────────────────────
    # 👥 VISTA PROPIETARIOS: estadísticas (antes Voluntarios)
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_voluntarios_stats():
        from apps.owners.models import Owner
        
        total_propietarios = Owner.objects.filter(is_active=True).count()
        voluntarios = Owner.objects.filter(is_volunteer=True, is_active=True).count()
        no_voluntarios = total_propietarios - voluntarios

        return {
            'voluntarios_activos': voluntarios,
            'total_propietarios': total_propietarios,
            'no_voluntarios': no_voluntarios,
            'tareas_completadas': voluntarios + no_voluntarios,
        }

    @staticmethod
    def get_volunteers_by_role():
        from apps.owners.models import Owner
        data = Owner.objects.filter(is_active=True).values(
            'is_volunteer'
        ).annotate(total=Count('id'))
        
        labels = ['Voluntarios', 'Propietarios']
        values = [
            next((d['total'] for d in data if d['is_volunteer']), 0),
            next((d['total'] for d in data if not d['is_volunteer']), 0)
        ]
        return json.dumps({'labels': labels, 'values': values})

    # ─────────────────────────────────────────────────────
    # 📦 VISTA INVENTARIO: estadísticas
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_inventario_stats():
        from apps.inventario.models import Product
        
        total = Product.objects.filter(is_active=True).count()
        stock_bajo = Product.objects.filter(is_active=True, quantity__lte=5).count()
        total_valor = Product.objects.filter(
            is_active=True
        ).aggregate(total=Sum('quantity'))['total'] or 0

        return {
            'total_productos': total,
            'stock_bajo': stock_bajo,
            'total_items': total_valor,
        }

    @staticmethod
    def get_inventory_categories():
        from apps.inventario.models import Product
        data = Product.objects.filter(is_active=True).values(
            'unit'
        ).annotate(total=Count('id')).order_by('-total')
        
        labels = [d['unit'] or 'Sin unidad' for d in data]
        values = [d['total'] for d in data]
        return json.dumps({'labels': labels, 'values': values})

    # ─────────────────────────────────────────────────────
    # 💰 VISTA DONACIONES: estadísticas
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_donaciones_stats():
        from apps.donaciones.models import Donacion
        
        today = timezone.now().date()
        primer_dia_mes = today.replace(day=1)
        
        total = Donacion.objects.filter(
            is_active=True,
            donation_type='Monetaria',
            status__in=['Recibida', 'Procesada']
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        este_mes = Donacion.objects.filter(
            is_active=True,
            donation_type='Monetaria',
            status__in=['Recibida', 'Procesada'],
            date__gte=primer_dia_mes
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        donors_qs = Donacion.objects.filter(
            is_active=True,
            donation_type='Monetaria',
            status__in=['Recibida', 'Procesada']
        )
        unique_donors = donors_qs.exclude(
            donante_email=''
        ).values('donante_email').distinct().count()
        
        count_donaciones = donors_qs.count()
        
        donors_mensuales = Donacion.objects.filter(
            is_active=True,
            donation_type='Monetaria',
            status__in=['Recibida', 'Procesada'],
            date__gte=primer_dia_mes
        ).values('donante_email').distinct().count()

        return {
            'total_donaciones': float(total),
            'donaciones_mes': float(este_mes),
            'promedio_donacion': round(float(total) / count_donaciones, 2) if count_donaciones > 0 else 0,
            'donantes_activos': unique_donors,
            'donantes_recurrentes': donors_mensuales,
        }

    @staticmethod
    def get_donations_by_type():
        from apps.donaciones.models import Donacion
        data = Donacion.objects.filter(is_active=True).values(
            'donation_type'
        ).annotate(total=Sum('amount')).order_by('-total')
        
        labels = [d['donation_type'] for d in data]
        values = [float(d['total'] or 0) for d in data]
        return json.dumps({'labels': labels, 'values': values})

    @staticmethod
    def get_donations_by_payment():
        from apps.donaciones.models import Donacion
        data = Donacion.objects.filter(is_active=True).values(
            'payment_method'
        ).annotate(total=Sum('amount')).order_by('-total')
        
        labels = [d['payment_method'] for d in data]
        values = [float(d['total'] or 0) for d in data]
        return json.dumps({'labels': labels, 'values': values})

    @staticmethod
    def get_top_donors(limit=5):
        from apps.donaciones.models import Donacion
        data = Donacion.objects.filter(
            is_active=True,
            donation_type='Monetaria',
            status__in=['Recibida', 'Procesada']
        ).values(
            'donante'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')[:limit]
        return data

    @staticmethod
    def get_recent_donations_full(limit=5):
        from apps.donaciones.models import Donacion
        return Donacion.objects.filter(
            is_active=True,
            status__in=['Recibida', 'Procesada']
        ).order_by('-date')[:limit]

    # ─────────────────────────────────────────────────────
    # 🏥 VISTA HISTORIAL MÉDICO: estadísticas
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_salud_stats():
        from apps.health.models import MedicalEvent
        
        total = MedicalEvent.objects.filter(is_active=True).count()
        abiertos = MedicalEvent.objects.filter(is_active=True, status='Abierto').count()
        en_proceso = MedicalEvent.objects.filter(is_active=True, status='En Proceso').count()
        resueltos = MedicalEvent.objects.filter(is_active=True, status='Resolved').count()
        
        prioridad_alta = MedicalEvent.objects.filter(
            is_active=True, severity='Alta', status__in=['Abierto', 'En Proceso']
        ).count()

        return {
            'total_eventos': total,
            'incidencias_abiertas': abiertos + en_proceso,
            'prioridad_alta': prioridad_alta,
            'tiempo_promedio': 3.2,
            'resueltos_mes': resueltos,
            'en_proceso': en_proceso,
        }

    @staticmethod
    def get_health_by_type():
        from apps.health.models import MedicalEvent
        data = MedicalEvent.objects.filter(is_active=True).values(
            'event_type'
        ).annotate(total=Count('id')).order_by('-total')
        
        labels = [d['event_type'] for d in data]
        values = [d['total'] for d in data]
        return json.dumps({'labels': labels, 'values': values})

    @staticmethod
    def get_health_by_severity():
        from apps.health.models import MedicalEvent
        data = MedicalEvent.objects.filter(is_active=True).values(
            'severity'
        ).annotate(total=Count('id')).order_by('-total')
        
        labels = [d['severity'] for d in data]
        values = [d['total'] for d in data]
        return json.dumps({'labels': labels, 'values': values})

    # ─────────────────────────────────────────────────────
    # 📊 REPORTES: datos reales para gráficos
    # ─────────────────────────────────────────────────────
    @staticmethod
    def get_reportes_resumen():
        from apps.animales.models import Animal
        from apps.adopciones.models import Adopcion
        from apps.donaciones.models import Donacion
        from apps.health.models import MedicalEvent
        
        return {
            'total_animales': Animal.objects.filter(is_active=True).count(),
            'total_adopciones': Adopcion.objects.filter(is_active=True).count(),
            'total_donaciones': Donacion.objects.filter(
                is_active=True,
                donation_type='Monetaria',
                status__in=['Recibida', 'Procesada']
            ).aggregate(total=Sum('amount'))['total'] or 0,
            'total_eventos_medicos': MedicalEvent.objects.filter(is_active=True).count(),
        }

    @staticmethod
    def get_reportes_tendencias():
        from apps.animales.models import Animal
        from apps.adopciones.models import Adopcion
        from apps.donaciones.models import Donacion
        
        today = timezone.now().date()
        meses_es = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        animales_data = []
        adopciones_data = []
        donaciones_data = []
        labels = []
        
        for i in range(5, -1, -1):
            m = today.month - i
            y = today.year
            while m <= 0:
                m += 12
                y -= 1
            primer_dia = date(y, m, 1)
            ultimo_dia = date(y + 1, 1, 1) if m == 12 else date(y, m + 1, 1)
            
            anim_count = Animal.objects.filter(
                is_active=True, admission_date__gte=primer_dia, admission_date__lt=ultimo_dia
            ).count()
            adop_count = Adopcion.objects.filter(
                is_active=True, adoption_date__gte=primer_dia, adoption_date__lt=ultimo_dia
            ).count()
            don_total = Donacion.objects.filter(
                is_active=True, date__gte=primer_dia, date__lt=ultimo_dia
            ).aggregate(t=Sum('amount'))['t'] or 0
            
            labels.append(meses_es[m - 1])
            animales_data.append(anim_count)
            adopciones_data.append(adop_count)
            donaciones_data.append(float(don_total))
        
        return json.dumps({
            'labels': labels,
            'animales': animales_data,
            'adopciones': adopciones_data,
            'donaciones': donaciones_data,
        })
