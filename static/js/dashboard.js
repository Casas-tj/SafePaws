/**
 * dashboard.js — SafePaws
 * Chart.js inicializado con datos reales pasados desde Django.
 * Las variables SPECIES_DATA, ADOPTIONS_DATA, DONATIONS_DATA
 * se definen en el bloque {% block js %} del template.
 */

// ══════════════════════════════════════════════════════
// NAVEGACIÓN entre vistas del dashboard
// ══════════════════════════════════════════════════════
function navigateTo(viewName) {
    document.querySelectorAll('.dashboard-view').forEach(v => v.classList.remove('active'));
    document.querySelectorAll('.sidebar-link').forEach(l => l.classList.remove('active'));

    const target = document.getElementById('view-' + viewName);
    if (target) target.classList.add('active');

    const link = document.querySelector(`[data-view="${viewName}"]`);
    if (link) link.classList.add('active');

    const titles = {
        panel:         ['Panel de Control', 'Sistema de Gestión de Refugio Animal'],
        animales:      ['Animales', 'Gestión y seguimiento de todos los animales'],
        adopciones:    ['Adopciones', 'Seguimiento de solicitudes y adopciones'],
        voluntarios:   ['Voluntarios', 'Gestión de voluntarios y turnos'],
        donaciones:    ['Donaciones', 'Seguimiento de donaciones y donantes'],
        incidencias:   ['Incidencias', 'Gestión y seguimiento de incidencias'],
        horario:       ['Horario', 'Horarios y turnos programados'],
        reportes:      ['Reportes', 'Reportes y análisis del sistema'],
        configuracion: ['Configuración', 'Ajustes del sistema'],
    };

    if (titles[viewName]) {
        const el = document.getElementById('page-title');
        const sub = document.getElementById('page-subtitle');
        if (el)  el.textContent  = titles[viewName][0];
        if (sub) sub.textContent = titles[viewName][1];
    }
}

// Iniciar en panel al cargar
document.addEventListener('DOMContentLoaded', () => {
    navigateTo('panel');

    // Navegación por sidebar
    document.querySelectorAll('.sidebar-link').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            navigateTo(link.dataset.view);
        });
    });

    // Configuración tabs
    document.querySelectorAll('[data-config-tab]').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('[data-config-tab]').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.config-tab-content').forEach(t => t.classList.remove('active'));
            btn.classList.add('active');
            const tab = document.getElementById('config-tab-' + btn.dataset.configTab);
            if (tab) tab.classList.add('active');
        });
    });

    initCharts();
});


// ══════════════════════════════════════════════════════
// PALETA DE COLORES
// ══════════════════════════════════════════════════════
const COLORS = {
    green:  '#10b981',
    blue:   '#3b82f6',
    yellow: '#f59e0b',
    red:    '#ef4444',
    purple: '#8b5cf6',
    cyan:   '#06b6d4',
    pink:   '#ec4899',
    slate:  '#64748b',
};

const SPECIES_COLORS = [
    COLORS.green, COLORS.blue, COLORS.yellow,
    COLORS.purple, COLORS.red, COLORS.cyan, COLORS.pink,
];

// Defaults seguros si Django no pasa datos
const _species   = (typeof SPECIES_DATA   !== 'undefined') ? SPECIES_DATA   : {labels:[], values:[]};
const _adoptions = (typeof ADOPTIONS_DATA !== 'undefined') ? ADOPTIONS_DATA : {labels:[], values:[]};
const _donations = (typeof DONATIONS_DATA !== 'undefined') ? DONATIONS_DATA : {labels:[], values:[]};

// Opciones comunes para todos los charts
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = 'Inter, system-ui, sans-serif';

const GRID_OPTS = {
    color: 'rgba(148,163,184,0.1)',
    drawBorder: false,
};

function tooltipStyle() {
    return {
        backgroundColor: '#1e293b',
        borderColor: '#334155',
        borderWidth: 1,
        padding: 10,
        titleColor: '#e2e8f0',
        bodyColor: '#94a3b8',
    };
}


// ══════════════════════════════════════════════════════
// INICIALIZACIÓN DE TODOS LOS CHARTS
// ══════════════════════════════════════════════════════
function initCharts() {

    // ── Panel: Donaciones mensuales (bar) ────────────
    const barCtx = document.getElementById('barChart');
    if (barCtx) {
        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: _donations.labels,
                datasets: [{
                    label: 'Donaciones (€)',
                    data: _donations.values,
                    backgroundColor: 'rgba(16,185,129,0.7)',
                    borderColor: COLORS.green,
                    borderWidth: 1,
                    borderRadius: 4,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: { callbacks: {
                    label: ctx => ` €${ctx.parsed.y.toLocaleString('es-ES')}`
                }, ...tooltipStyle() }},
                scales: {
                    x: { grid: GRID_OPTS },
                    y: { grid: GRID_OPTS, beginAtZero: true,
                         ticks: { callback: v => `€${v}` } },
                },
            },
        });
    }

    // ── Panel: Distribución por especie (doughnut) ───
    const doughnutCtx = document.getElementById('doughnutChart');
    if (doughnutCtx) {
        const hasData = _species.values && _species.values.length > 0;
        new Chart(doughnutCtx, {
            type: 'doughnut',
            data: {
                labels: hasData ? _species.labels : ['Sin datos'],
                datasets: [{
                    data:            hasData ? _species.values : [1],
                    backgroundColor: hasData ? SPECIES_COLORS.slice(0, _species.labels.length) : ['#334155'],
                    borderWidth: 2,
                    borderColor: '#0f172a',
                    hoverOffset: 8,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { padding: 16, boxWidth: 12 } },
                    tooltip: tooltipStyle(),
                },
                cutout: '65%',
            },
        });
    }

    // ── Animales: distribución por especie (pie) ─────
    const animalPieCtx = document.getElementById('animalPieChart');
    if (animalPieCtx) {
        new Chart(animalPieCtx, {
            type: 'pie',
            data: {
                labels: _species.labels.length ? _species.labels : ['Sin datos'],
                datasets: [{
                    data: _species.values.length ? _species.values : [1],
                    backgroundColor: SPECIES_COLORS,
                    borderWidth: 2,
                    borderColor: '#0f172a',
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { padding: 16, boxWidth: 12 } },
                    tooltip: tooltipStyle(),
                },
            },
        });
    }

    // ── Animales: ingresos mensuales (line) ──────────
    const animalLineCtx = document.getElementById('animalLineChart');
    if (animalLineCtx) {
        new Chart(animalLineCtx, {
            type: 'line',
            data: {
                labels: _adoptions.labels,
                datasets: [{
                    label: 'Adopciones',
                    data: _adoptions.values,
                    borderColor: COLORS.blue,
                    backgroundColor: 'rgba(59,130,246,0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: COLORS.blue,
                    pointRadius: 4,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: tooltipStyle() },
                scales: {
                    x: { grid: GRID_OPTS },
                    y: { grid: GRID_OPTS, beginAtZero: true,
                         ticks: { stepSize: 1 } },
                },
            },
        });
    }

    // ── Animales: estado de salud (bar agrupado - demo) ─
    const animalBarCtx = document.getElementById('animalBarChart');
    if (animalBarCtx) {
        new Chart(animalBarCtx, {
            type: 'bar',
            data: {
                labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                datasets: [
                    { label: 'Saludables', data: [40, 45, 42, 50, 48, 55],
                      backgroundColor: 'rgba(16,185,129,0.7)', borderRadius: 4 },
                    { label: 'En tratamiento', data: [8, 6, 9, 7, 10, 8],
                      backgroundColor: 'rgba(245,158,11,0.7)', borderRadius: 4 },
                    { label: 'Críticos', data: [2, 1, 3, 1, 2, 1],
                      backgroundColor: 'rgba(239,68,68,0.7)', borderRadius: 4 },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'top' }, tooltip: tooltipStyle() },
                scales: {
                    x: { grid: GRID_OPTS, stacked: false },
                    y: { grid: GRID_OPTS, beginAtZero: true },
                },
            },
        });
    }

    // ── Adopciones: por mes (line) ───────────────────
    const adopLinCtx = document.getElementById('adopcionesLineChart');
    if (adopLinCtx) {
        new Chart(adopLinCtx, {
            type: 'line',
            data: {
                labels: _adoptions.labels,
                datasets: [{
                    label: 'Adopciones completadas',
                    data: _adoptions.values,
                    borderColor: COLORS.green,
                    backgroundColor: 'rgba(16,185,129,0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: COLORS.green,
                    pointRadius: 4,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: tooltipStyle() },
                scales: { x: { grid: GRID_OPTS }, y: { grid: GRID_OPTS, beginAtZero: true, ticks: { stepSize: 1 } } },
            },
        });
    }

    // ── Adopciones: por especie (doughnut) ───────────
    const adopDoughCtx = document.getElementById('adopcionesDoughnutChart');
    if (adopDoughCtx) {
        new Chart(adopDoughCtx, {
            type: 'doughnut',
            data: {
                labels: _species.labels.length ? _species.labels : ['Sin datos'],
                datasets: [{
                    data: _species.values.length ? _species.values : [1],
                    backgroundColor: SPECIES_COLORS,
                    borderWidth: 2, borderColor: '#0f172a', hoverOffset: 8,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false, cutout: '65%',
                plugins: { legend: { position: 'bottom', labels: { padding: 16, boxWidth: 12 } }, tooltip: tooltipStyle() },
            },
        });
    }

    // ── Donaciones: tendencia mensual (line) ─────────
    const donLinCtx = document.getElementById('donLineChart');
    if (donLinCtx) {
        new Chart(donLinCtx, {
            type: 'line',
            data: {
                labels: _donations.labels,
                datasets: [{
                    label: 'Donaciones (€)',
                    data: _donations.values,
                    borderColor: COLORS.yellow,
                    backgroundColor: 'rgba(245,158,11,0.1)',
                    tension: 0.4, fill: true,
                    pointBackgroundColor: COLORS.yellow, pointRadius: 4,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: {
                    callbacks: { label: ctx => ` €${ctx.parsed.y.toLocaleString('es-ES')}` },
                    ...tooltipStyle(),
                }},
                scales: {
                    x: { grid: GRID_OPTS },
                    y: { grid: GRID_OPTS, beginAtZero: true, ticks: { callback: v => `€${v}` } },
                },
            },
        });
    }

    // ── Donaciones: por tipo (pie - demo) ────────────
    const donPieCtx = document.getElementById('donPieChart');
    if (donPieCtx) {
        new Chart(donPieCtx, {
            type: 'pie',
            data: {
                labels: ['Monetaria', 'Material', 'Otro'],
                datasets: [{
                    data: [70, 20, 10],
                    backgroundColor: [COLORS.green, COLORS.blue, COLORS.slate],
                    borderWidth: 2, borderColor: '#0f172a',
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { padding: 16, boxWidth: 12 } }, tooltip: tooltipStyle() },
            },
        });
    }

    // ── Donaciones: métodos de pago (bar - demo) ─────
    const donBarCtx = document.getElementById('donBarChart');
    if (donBarCtx) {
        new Chart(donBarCtx, {
            type: 'bar',
            data: {
                labels: ['Transferencia', 'Efectivo', 'Tarjeta', 'PayPal', 'Cheque', 'Otro'],
                datasets: [{
                    label: 'Donaciones',
                    data: [45, 25, 15, 10, 3, 2],
                    backgroundColor: [
                        COLORS.blue, COLORS.green, COLORS.yellow,
                        COLORS.cyan, COLORS.purple, COLORS.slate,
                    ],
                    borderRadius: 4,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: tooltipStyle() },
                scales: { x: { grid: GRID_OPTS }, y: { grid: GRID_OPTS, beginAtZero: true } },
            },
        });
    }

    // ── Voluntarios: horas por mes (line - demo) ─────
    const volLinCtx = document.getElementById('volLineChart');
    if (volLinCtx) {
        new Chart(volLinCtx, {
            type: 'line',
            data: {
                labels: _adoptions.labels,
                datasets: [{
                    label: 'Horas de voluntariado',
                    data: [280, 310, 295, 330, 380, 398],
                    borderColor: COLORS.purple,
                    backgroundColor: 'rgba(139,92,246,0.1)',
                    tension: 0.4, fill: true,
                    pointBackgroundColor: COLORS.purple, pointRadius: 4,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: tooltipStyle() },
                scales: { x: { grid: GRID_OPTS }, y: { grid: GRID_OPTS, beginAtZero: true } },
            },
        });
    }

    // ── Voluntarios: por tarea (pie - demo) ──────────
    const volPieCtx = document.getElementById('volPieChart');
    if (volPieCtx) {
        new Chart(volPieCtx, {
            type: 'pie',
            data: {
                labels: ['Cuidado Animal', 'Administración', 'Medicina', 'Vigilancia', 'Otros'],
                datasets: [{
                    data: [40, 20, 20, 10, 10],
                    backgroundColor: [COLORS.green, COLORS.blue, COLORS.yellow, COLORS.purple, COLORS.slate],
                    borderWidth: 2, borderColor: '#0f172a',
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { padding: 16, boxWidth: 12 } }, tooltip: tooltipStyle() },
            },
        });
    }

    // ── Voluntarios: por turno (bar - demo) ──────────
    const volBarCtx = document.getElementById('volBarChart');
    if (volBarCtx) {
        new Chart(volBarCtx, {
            type: 'bar',
            data: {
                labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                datasets: [
                    { label: 'Mañana',  data: [8, 7, 6, 9, 8, 5, 4], backgroundColor: 'rgba(16,185,129,0.7)', borderRadius: 4 },
                    { label: 'Tarde',   data: [6, 8, 7, 5, 7, 6, 5], backgroundColor: 'rgba(59,130,246,0.7)',  borderRadius: 4 },
                    { label: 'Noche',   data: [3, 2, 3, 2, 3, 4, 3], backgroundColor: 'rgba(139,92,246,0.7)', borderRadius: 4 },
                ],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'top' }, tooltip: tooltipStyle() },
                scales: { x: { grid: GRID_OPTS }, y: { grid: GRID_OPTS, beginAtZero: true, ticks: { stepSize: 1 } } },
            },
        });
    }

    // ── Reportes: ingresos y adopciones (line doble) ─
    const repLinCtx = document.getElementById('repLineChart');
    if (repLinCtx) {
        new Chart(repLinCtx, {
            type: 'line',
            data: {
                labels: _adoptions.labels,
                datasets: [
                    {
                        label: 'Adopciones', data: _adoptions.values,
                        borderColor: COLORS.blue, backgroundColor: 'rgba(59,130,246,0.1)',
                        tension: 0.4, fill: true, pointRadius: 4,
                    },
                    {
                        label: 'Donaciones (€/100)', data: _donations.values.map(v => v / 100),
                        borderColor: COLORS.green, backgroundColor: 'rgba(16,185,129,0.1)',
                        tension: 0.4, fill: true, pointRadius: 4,
                    },
                ],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'top' }, tooltip: tooltipStyle() },
                scales: { x: { grid: GRID_OPTS }, y: { grid: GRID_OPTS, beginAtZero: true } },
            },
        });
    }

    // ── Reportes: donaciones (bar) ───────────────────
    const repBarCtx = document.getElementById('repBarChart');
    if (repBarCtx) {
        new Chart(repBarCtx, {
            type: 'bar',
            data: {
                labels: _donations.labels,
                datasets: [{
                    label: 'Donaciones (€)',
                    data: _donations.values,
                    backgroundColor: 'rgba(245,158,11,0.7)',
                    borderColor: COLORS.yellow,
                    borderWidth: 1, borderRadius: 4,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: {
                    callbacks: { label: ctx => ` €${ctx.parsed.y.toLocaleString('es-ES')}` },
                    ...tooltipStyle(),
                }},
                scales: {
                    x: { grid: GRID_OPTS },
                    y: { grid: GRID_OPTS, beginAtZero: true, ticks: { callback: v => `€${v}` } },
                },
            },
        });
    }

    // ── Incidencias: por mes (line - demo) ───────────
    const incLinCtx = document.getElementById('incLineChart');
    if (incLinCtx) {
        new Chart(incLinCtx, {
            type: 'line',
            data: {
                labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                datasets: [{
                    label: 'Incidencias',
                    data: [12, 8, 15, 7, 10, 7],
                    borderColor: COLORS.red,
                    backgroundColor: 'rgba(239,68,68,0.1)',
                    tension: 0.4, fill: true, pointRadius: 4,
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: tooltipStyle() },
                scales: { x: { grid: GRID_OPTS }, y: { grid: GRID_OPTS, beginAtZero: true } },
            },
        });
    }

    // ── Incidencias: por tipo (pie - demo) ───────────
    const incPieCtx = document.getElementById('incPieChart');
    if (incPieCtx) {
        new Chart(incPieCtx, {
            type: 'pie',
            data: {
                labels: ['Salud Animal', 'Instalaciones', 'Seguridad', 'Personal', 'Clima'],
                datasets: [{
                    data: [35, 25, 15, 15, 10],
                    backgroundColor: [COLORS.red, COLORS.yellow, COLORS.blue, COLORS.purple, COLORS.cyan],
                    borderWidth: 2, borderColor: '#0f172a',
                }],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { padding: 16, boxWidth: 12 } }, tooltip: tooltipStyle() },
            },
        });
    }

    // ── Incidencias: por severidad (bar - demo) ──────
    const incBarCtx = document.getElementById('incBarChart');
    if (incBarCtx) {
        new Chart(incBarCtx, {
            type: 'bar',
            data: {
                labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                datasets: [
                    { label: 'Crítica', data: [2, 1, 3, 1, 2, 1], backgroundColor: 'rgba(239,68,68,0.8)', borderRadius: 4 },
                    { label: 'Alta',    data: [4, 3, 5, 3, 4, 3], backgroundColor: 'rgba(245,158,11,0.8)', borderRadius: 4 },
                    { label: 'Media',   data: [6, 4, 7, 3, 4, 3], backgroundColor: 'rgba(59,130,246,0.7)', borderRadius: 4 },
                ],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'top' }, tooltip: tooltipStyle() },
                scales: { x: { grid: GRID_OPTS }, y: { grid: GRID_OPTS, beginAtZero: true } },
            },
        });
    }

    // ── Adopciones: estado del proceso (bar - demo) ──
    const adopBarCtx = document.getElementById('adopcionesBarChart');
    if (adopBarCtx) {
        new Chart(adopBarCtx, {
            type: 'bar',
            data: {
                labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                datasets: [
                    { label: 'Completadas', data: _adoptions.values,
                      backgroundColor: 'rgba(16,185,129,0.7)', borderRadius: 4 },
                    { label: 'Pendientes',  data: [3, 2, 4, 2, 3, 2],
                      backgroundColor: 'rgba(59,130,246,0.7)', borderRadius: 4 },
                    { label: 'Canceladas',  data: [1, 0, 1, 0, 1, 0],
                      backgroundColor: 'rgba(239,68,68,0.7)', borderRadius: 4 },
                ],
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { position: 'top' }, tooltip: tooltipStyle() },
                scales: { x: { grid: GRID_OPTS }, y: { grid: GRID_OPTS, beginAtZero: true, ticks: { stepSize: 1 } } },
            },
        });
    }
}

// ══════════════════════════════════════════════════════
// 🔔 NOTIFICACIONES: toggle dropdown
// ══════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('btn-notif');
    const dropdown = document.getElementById('notif-dropdown');
    if (!btn || !dropdown) return;

    btn.addEventListener('click', function (e) {
        e.stopPropagation();
        dropdown.classList.toggle('open');
    });

    document.addEventListener('click', function () {
        dropdown.classList.remove('open');
    });

    dropdown.addEventListener('click', function (e) {
        e.stopPropagation();
    });
});
