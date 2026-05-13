from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services.dashboard_services import DashboardService


@login_required
def home(request):
    return render(request, 'dashboard/home.html', {
        "headertitle": "SafePaws",
        "headersubtitle": "Sistema de gestión interna de la protectora de animales SafePaws",
    })


@login_required
def dashboard(request):
    # ── Panel Principal ─────────────────────────────
    stats             = DashboardService.get_panel_stats()
    recent_adoptions  = DashboardService.get_recent_adoptions(limit=3)
    recent_donations  = DashboardService.get_recent_donations(limit=3)
    stock_alerts      = DashboardService.get_stock_alerts(limit=3)
    recent_medical    = DashboardService.get_recent_medical_events(limit=2)

    # ── Charts Panel Principal ───────────────────────
    species_data      = DashboardService.get_species_chart_data()
    adoptions_data    = DashboardService.get_monthly_adoptions_chart()
    donations_data    = DashboardService.get_monthly_donations_chart()

    # ── Vista Animales ───────────────────────────────
    animales_stats    = DashboardService.get_animales_stats()
    recent_animals    = DashboardService.get_recent_animals(limit=5)
    species_chart     = DashboardService.get_animals_by_species()
    monthly_admissions = DashboardService.get_monthly_admissions()
    health_status     = DashboardService.get_health_status()

    # ── Vista Adopciones ─────────────────────────────
    adopciones_stats  = DashboardService.get_adopciones_stats()
    adoptions_monthly = DashboardService.get_adoptions_by_month()
    adoptions_species = DashboardService.get_adoptions_by_species()
    adoption_status   = DashboardService.get_adoption_status_breakdown()

    # ── Vista Voluntarios ─────────────────────────────
    voluntarios_stats = DashboardService.get_voluntarios_stats()
    volunteers_role   = DashboardService.get_volunteers_by_role()
    volunteers_list  = DashboardService.get_volunteers_list(limit=5)
    owners_list       = DashboardService.get_all_owners(limit=5)

    # ── Vista Inventario ─────────────────────────────
    inventario_stats  = DashboardService.get_inventario_stats()
    inventory_cats   = DashboardService.get_inventory_categories()

    # ── Vista Donaciones ─────────────────────────────
    donaciones_stats = DashboardService.get_donaciones_stats()
    donations_type   = DashboardService.get_donations_by_type()
    donations_payment = DashboardService.get_donations_by_payment()
    top_donors       = DashboardService.get_top_donors(limit=5)
    recent_don_full  = DashboardService.get_recent_donations_full(limit=5)

    # ── Vista Salud/Incidencias ──────────────────────
    salud_stats       = DashboardService.get_salud_stats()
    health_types      = DashboardService.get_health_by_type()
    health_severity  = DashboardService.get_health_by_severity()
    medical_events   = DashboardService.get_recent_medical_full(limit=5)
    open_events      = DashboardService.get_open_medical_events(limit=5)
    resolved_events  = DashboardService.get_recent_resolved_events(limit=5)

    # ── Vista Reportes ───────────────────────────────
    reportes_resumen = DashboardService.get_reportes_resumen()
    reportes_tendencias = DashboardService.get_reportes_tendencias()

    return render(request, 'dashboard/dashboard.html', {
        # Navegación
        'btn_back': 'Volver',
        'back_url': 'home',

        # Panel Principal
        'stats': stats,
        'recent_adoptions': recent_adoptions,
        'recent_donations': recent_donations,
        'stock_alerts': stock_alerts,
        'recent_medical': recent_medical,
        'species_data': species_data,
        'adoptions_data': adoptions_data,
        'donations_data': donations_data,

        # Animales
        'animales_stats': animales_stats,
        'recent_animals': recent_animals,
        'species_chart': species_chart,
        'monthly_admissions': monthly_admissions,
        'health_status': health_status,

        # Adopciones
        'adopciones_stats': adopciones_stats,
        'adoptions_monthly': adoptions_monthly,
        'adoptions_species': adoptions_species,
        'adoption_status': adoption_status,

        # Voluntarios
        'voluntarios_stats': voluntarios_stats,
        'volunteers_role': volunteers_role,
        'volunteers_list': volunteers_list,
        'owners_list': owners_list,

        # Inventario
        'inventario_stats': inventario_stats,
        'inventory_cats': inventory_cats,

        # Donaciones
        'donaciones_stats': donaciones_stats,
        'donations_type': donations_type,
        'donations_payment': donations_payment,
        'top_donors': top_donors,
        'recent_don_full': recent_don_full,

        # Salud/Incidencias
        'salud_stats': salud_stats,
        'health_types': health_types,
        'health_severity': health_severity,
        'medical_events': medical_events,
        'open_events': open_events,
        'resolved_events': resolved_events,

        # Reportes
        'reportes_resumen': reportes_resumen,
        'reportes_tendencias': reportes_tendencias,
    })