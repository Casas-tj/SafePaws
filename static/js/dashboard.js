// ========================================
// SAFEPAWS DASHBOARD - JAVASCRIPT
// ========================================

document.addEventListener('DOMContentLoaded', function () {
    // Verificar autenticación
    checkAuth();

    // Inicializar navegación SPA
    initNavigation();

    // Inicializar gráficos
    initCharts();

    // Animar métricas
    animateMetrics();

    // Inicializar interacciones
    initInteractions();

    // Inicializar tabs
    initTabs();
});

// ========================================
// VERIFICACIÓN DE AUTENTICACIÓN
// ========================================
function checkAuth() {
    const isAuthenticated = localStorage.getItem('safepaws_authenticated');
    if (isAuthenticated !== 'true') {
        // Comentar la siguiente línea para desarrollo
        // window.location.href = 'index.html';
    }
}

// ========================================
// NAVEGACIÓN SPA
// ========================================
function initNavigation() {
    // Manejar clicks en sidebar
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const viewName = this.getAttribute('data-view');
            navigateTo(viewName);
        });
    });

    // Cargar vista inicial desde URL hash o mostrar panel
    const hash = window.location.hash.substring(1);
    if (hash) {
        navigateTo(hash);
    } else {
        navigateTo('panel');
    }

    // Manejar navegación del navegador (botones atrás/adelante)
    window.addEventListener('hashchange', function () {
        const hash = window.location.hash.substring(1);
        if (hash) {
            navigateTo(hash, false);
        }
    });
}

function navigateTo(viewName, updateHash = true) {
    // Ocultar todas las vistas
    const views = document.querySelectorAll('.dashboard-view');
    views.forEach(view => view.classList.remove('active'));

    // Mostrar la vista seleccionada
    const targetView = document.getElementById('view-' + viewName);
    if (targetView) {
        targetView.classList.add('active');
    }

    // Actualizar sidebar
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-view') === viewName) {
            link.classList.add('active');
        }
    });

    // Actualizar título de la página
    updatePageTitle(viewName);

    // Actualizar URL hash
    if (updateHash) {
        window.location.hash = viewName;
    }

    // Scroll al inicio
    window.scrollTo(0, 0);

    // Reinicializar gráficos si es necesario
    if (viewName === 'panel') {
        setTimeout(() => {
            initCharts();
        }, 100);
    }

    if (viewName === 'animales') {
        setTimeout(() => {
            initAnimalesCharts();
        }, 100);
    }

    if (viewName === 'adopciones') {
        setTimeout(() => {
            initAdopcionesCharts();
        }, 100);
    }

    if (viewName === 'voluntarios') {
        setTimeout(() => {
            initVoluntariosCharts();
        }, 100);
    }

    if (viewName === 'donaciones') {
        setTimeout(() => {
            initDonacionesCharts();
        }, 100);
    }

    if (viewName === 'incidencias') {
        setTimeout(() => {
            initIncidenciasCharts();
        }, 100);
    }

    if (viewName === 'reportes') {
        setTimeout(() => {
            initReportesCharts();
        }, 100);
    }
}

function updatePageTitle(viewName) {
    const titles = {
        'panel': 'Panel de Control',
        'animales': 'Gestión de Animales',
        'adopciones': 'Gestión de Adopciones',
        'voluntarios': 'Gestión de Voluntarios',
        'donaciones': 'Gestión de Donaciones',
        'incidencias': 'Gestión de Incidencias',
        'horario': 'Gestión de Horarios',
        'reportes': 'Centro de Reportes',
        'configuracion': 'Configuración del Sistema'
    };

    const subtitles = {
        'panel': 'Sistema de Gestión de Refugio Animal',
        'animales': 'Administra el registro completo de animales',
        'adopciones': 'Seguimiento de procesos de adopción',
        'voluntarios': 'Coordina y gestiona el equipo de voluntarios',
        'donaciones': 'Administra las contribuciones y donantes',
        'incidencias': 'Seguimiento de alertas y problemas',
        'horario': 'Planificación y asignación de turnos',
        'reportes': 'Genera y consulta informes del sistema',
        'configuracion': 'Ajustes generales y preferencias'
    };

    const pageTitle = document.getElementById('page-title');
    const pageSubtitle = document.getElementById('page-subtitle');

    if (pageTitle) {
        pageTitle.textContent = titles[viewName] || 'SafePaws';
    }

    if (pageSubtitle) {
        pageSubtitle.textContent = subtitles[viewName] || '';
    }
}

// ========================================
// GESTIÓN DE TABS
// ========================================
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');

    tabButtons.forEach(button => {
        button.addEventListener('click', function () {
            const tabName = this.getAttribute('data-tab');
            const parentContainer = this.closest('.view-content') || this.closest('.control-panel');

            // Remover active de todos los botones del mismo grupo
            const siblingButtons = this.parentElement.querySelectorAll('.tab-btn');
            siblingButtons.forEach(btn => btn.classList.remove('active'));

            // Activar botón actual
            this.classList.add('active');

            // Ocultar todos los contenidos de tabs del mismo grupo
            const tabContents = parentContainer.querySelectorAll('.tab-content');
            tabContents.forEach(content => content.classList.remove('active'));

            // Mostrar contenido seleccionado
            const targetContent = parentContainer.querySelector('#tab-' + tabName);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

// ========================================
// INICIALIZACIÓN DE GRÁFICOS
// ========================================
let panelBarInstance = null;
let panelDoughnutInstance = null;

function initCharts() {
    createBarChart();
    createDoughnutChart();
}

// ========================================
// GRÁFICO DE BARRAS - Resumen Financiero
// ========================================
function createBarChart() {
    const ctx = document.getElementById('barChart');
    if (!ctx) return;

    if (panelBarInstance) {
        panelBarInstance.destroy();
        panelBarInstance = null;
    }

    const gradient1 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
    gradient1.addColorStop(0, '#10b981');
    gradient1.addColorStop(1, '#059669');

    const gradient2 = ctx.getContext('2d').createLinearGradient(0, 0, 0, 400);
    gradient2.addColorStop(0, '#3b82f6');
    gradient2.addColorStop(1, '#2563eb');

    panelBarInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            datasets: [
                {
                    label: 'Ingresos',
                    data: [12000, 15000, 18000, 14000, 20000, 17500, 19000, 21000, 18500, 22000, 25000, 30000],
                    backgroundColor: gradient1,
                    borderRadius: 8,
                    borderSkipped: false,
                    categoryPercentage: 0.9, // espacio entre grupos (meses)
                    barPercentage: 0.85      // espacio entre Ingresos / Gastos
                },
                {
                    label: 'Gastos',
                    data: [8000, 10000, 9500, 8500, 11000, 10500, 11500, 12000, 10800, 12500, 14000, 16000],
                    backgroundColor: gradient2,
                    borderRadius: 8,
                    borderSkipped: false,
                    categoryPercentage: 0.9,
                    barPercentage: 0.85
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#cbd5e1',
                        padding: 20,
                        font: {
                            size: 13,
                            weight: '600',
                            family: "'Inter', sans-serif"
                        },
                        usePointStyle: true,
                        pointStyle: 'circle',
                        boxWidth: 8,
                        boxHeight: 8
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#cbd5e1',
                    padding: 16,
                    cornerRadius: 12,
                    borderColor: 'rgba(59, 130, 246, 0.3)',
                    borderWidth: 1,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function (context) {
                            return context.dataset.label + ': $' + context.parsed.y.toLocaleString();
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(51, 65, 85, 0.3)',
                        drawBorder: false,
                        lineWidth: 1
                    },
                    border: {
                        display: false
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: {
                            size: 12,
                            weight: '500'
                        },
                        padding: 10,
                        callback: function (value) {
                            return '$' + (value / 1000) + 'k';
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    border: {
                        display: false
                    },
                    ticks: {
                        color: '#94a3b8',
                        font: {
                            size: 12,
                            weight: '500'
                        },
                        padding: 10
                    }
                }
            }
        }
    });
}

// ========================================
// GRÁFICO DE DONA - Distribución de Animales
// ========================================
function createDoughnutChart() {
    const ctx = document.getElementById('doughnutChart');
    if (!ctx) return;

    if (panelDoughnutInstance) {
        panelDoughnutInstance.destroy();
        panelDoughnutInstance = null;
    }

    panelDoughnutInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['En tratamiento', 'Adoptado', 'En acogida', 'En adopción'],
            datasets: [{
                data: [146, 38, 56, 34],
                backgroundColor: [
                    '#10b981',  // Verde
                    '#3b82f6',  // Azul
                    '#f59e0b',  // Amarillo/Naranja
                    '#8b5cf6'   // Púrpura
                ],
                borderWidth: 0,
                spacing: 3,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#cbd5e1',
                        font: {
                            size: 13,
                            weight: '600',
                            family: "'Inter', sans-serif"
                        },
                        padding: 20,
                        boxWidth: 16,
                        boxHeight: 16,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#ffffff',
                    bodyColor: '#cbd5e1',
                    borderColor: 'rgba(59, 130, 246, 0.3)',
                    borderWidth: 1,
                    padding: 16,
                    cornerRadius: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return label + ': ' + value + ' (' + percentage + '%)';
                        }
                    }
                }
            }
        }
    });
}

// ========================================
// GRÁFICOS DE ANIMALES
// ========================================
let animalPieInstance = null;
let animalLineInstance = null;
let animalBarInstance = null;

function initAnimalesCharts() {
    createAnimalPieChart();
    createAnimalLineChart();
    createAnimalBarChart();
}

// --- Pie: Distribución por Especie ---
function createAnimalPieChart() {
    const ctx = document.getElementById('animalPieChart');
    if (!ctx) return;
    if (animalPieInstance) { animalPieInstance.destroy(); animalPieInstance = null; }

    animalPieInstance = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Perros 57%', 'Gatos 32%', 'Conejos 7%', 'Pájaros 4%'],
            datasets: [{
                data: [57, 32, 7, 4],
                backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'],
                borderWidth: 2,
                borderColor: '#0f172a'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8',
                        font: { size: 11 },
                        padding: 15,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    padding: 12,
                    borderColor: '#334155',
                    borderWidth: 1,
                    callbacks: {
                        label: function (context) {
                            return ' ' + context.label;
                        }
                    }
                }
            }
        }
    });
}

// --- Line: Ingresos Mensuales ---
function createAnimalLineChart() {
    const ctx = document.getElementById('animalLineChart');
    if (!ctx) return;
    if (animalLineInstance) { animalLineInstance.destroy(); animalLineInstance = null; }

    animalLineInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            datasets: [{
                label: 'Ingresos',
                data: [22, 28, 30, 35, 38, 42, 48, 45, 50, 55, 52, 58],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.08)',
                borderWidth: 2.5,
                tension: 0.35,
                fill: true,
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#0f172a',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#cbd5e1',
                    padding: 14,
                    cornerRadius: 10,
                    borderColor: 'rgba(59, 130, 246, 0.3)',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(51, 65, 85, 0.25)', drawBorder: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                },
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                }
            }
        }
    });
}

// --- Bar: Estado de Salud General ---
function createAnimalBarChart() {
    const ctx = document.getElementById('animalBarChart');
    if (!ctx) return;
    if (animalBarInstance) { animalBarInstance.destroy(); animalBarInstance = null; }

    animalBarInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Saludable', 'En Tratamiento', 'Crítico', 'Recuperación'],
            datasets: [{
                label: 'Animales',
                data: [189, 52, 7, 26],
                backgroundColor: ['#3b82f6', '#10b981', '#ef4444', '#14b8a6'],
                borderRadius: 6,
                borderSkipped: false,
                barThickness: 48
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#cbd5e1',
                    padding: 14,
                    cornerRadius: 10,
                    borderColor: 'rgba(59, 130, 246, 0.3)',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(51, 65, 85, 0.25)', drawBorder: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                },
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                }
            }
        }
    });
}

// ========================================
// ANIMACIÓN DE MÉTRICAS
// ========================================
function animateMetrics() {
    const metricValues = document.querySelectorAll('.metric-value');

    metricValues.forEach(element => {
        const finalValue = element.textContent.trim();
        animateValue(element, finalValue);
    });
}

function animateValue(element, finalValue) {
    // Extraer el número del texto
    const numericValue = parseInt(finalValue.replace(/[^0-9]/g, ''));

    if (isNaN(numericValue) || numericValue === 0) return;

    // Detectar prefijo ($) y sufijos
    const hasPrefix = finalValue.startsWith('$');
    const prefix = hasPrefix ? '$' : '';

    const duration = 2000; // 2 segundos
    const frameDuration = 1000 / 60; // 60 FPS
    const totalFrames = Math.round(duration / frameDuration);
    let frame = 0;

    const counter = setInterval(() => {
        frame++;
        const progress = easeOutQuart(frame / totalFrames);
        const currentValue = Math.round(numericValue * progress);

        element.textContent = prefix + currentValue.toLocaleString();

        if (frame === totalFrames) {
            clearInterval(counter);
            element.textContent = finalValue;
        }
    }, frameDuration);
}

// Función de easing para animación suave
function easeOutQuart(x) {
    return 1 - Math.pow(1 - x, 4);
}

// ========================================
// INTERACCIONES
// ========================================
function initInteractions() {
    // Efecto hover en cards
    const cards = document.querySelectorAll('.metric-card, .chart-card, .activity-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        });
    });

    // Sidebar toggle para móvil
    const sidebar = document.querySelector('.dashboard-sidebar');
    const menuButton = document.querySelector('.menu-toggle');

    if (menuButton) {
        menuButton.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // Click fuera del sidebar para cerrar en móvil
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 1024) {
            if (sidebar && !sidebar.contains(e.target) && !e.target.classList.contains('menu-toggle')) {
                sidebar.classList.remove('open');
            }
        }
    });

    // Animación de scroll suave
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || href === '#panel' || href.startsWith('#')) {
                // No hacer scroll para navegación SPA
                return;
            }
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Actualizar hora en tiempo real (si hay un elemento de hora)
    updateTime();
    setInterval(updateTime, 1000);
}

function updateTime() {
    const timeElement = document.querySelector('.current-time');
    if (timeElement) {
        const now = new Date();
        const options = {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        };
        timeElement.textContent = now.toLocaleTimeString('es-ES', options);
    }
}

// ========================================
// UTILIDADES
// ========================================

// Formatear números
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Formatear moneda
function formatCurrency(amount) {
    return '$' + formatNumber(amount);
}

// Obtener saludo según hora del día
function getGreeting() {
    const hour = new Date().getHours();
    if (hour < 12) return 'Buenos días';
    if (hour < 19) return 'Buenas tardes';
    return 'Buenas noches';
}

// ========================================
// MANEJO DE ERRORES
// ========================================
window.addEventListener('error', function (e) {
    console.error('Error en el dashboard:', e.error);
});

// ========================================
// GRÁFICOS DE ADOPCIONES
// ========================================
let adopcionesLineInstance = null;
let adopcionesDoughnutInstance = null;
let adopcionesBarInstance = null;

// Gráfico de Línea: Adopciones por Mes
function createAdopcionesLineChart() {
    const ctx = document.getElementById('adopcionesLineChart');
    if (!ctx) return;
    if (adopcionesLineInstance) { adopcionesLineInstance.destroy(); adopcionesLineInstance = null; }

    adopcionesLineInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            datasets: [{
                label: 'Adopciones',
                data: [14, 16, 18, 22, 24, 20, 24, 18, 20, 22, 26, 24],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 2.5,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#0f172a',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#cbd5e1',
                    padding: 12,
                    cornerRadius: 8,
                    borderColor: 'rgba(16, 185, 129, 0.3)',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 28,
                    grid: { color: 'rgba(51, 65, 85, 0.25)', drawBorder: false },
                    border: { display: false },
                    ticks: {
                        color: '#94a3b8',
                        font: { size: 11 },
                        padding: 8,
                        stepSize: 7
                    }
                },
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                }
            }
        }
    });
}

// Gráfico de Donut: Adopciones por Especie
function createAdopcionesDoughnutChart() {
    const ctx = document.getElementById('adopcionesDoughnutChart');
    if (!ctx) return;
    if (adopcionesDoughnutInstance) { adopcionesDoughnutInstance.destroy(); adopcionesDoughnutInstance = null; }

    adopcionesDoughnutInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Perros', 'Gatos', 'Conejos', 'Otros'],
            datasets: [{
                data: [51, 18, 7, 5],
                backgroundColor: [
                    '#10b981',
                    '#3b82f6',
                    '#f59e0b',
                    '#8b5cf6'
                ],
                borderColor: '#0f172a',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#cbd5e1',
                        padding: 15,
                        font: { size: 11 },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#cbd5e1',
                    padding: 12,
                    cornerRadius: 8,
                    borderColor: 'rgba(59, 130, 246, 0.3)',
                    borderWidth: 1,
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(0);
                            return `${label}: ${percentage}%`;
                        }
                    }
                }
            }
        }
    });
}

// Gráfico de Barras: Estado del Proceso
function createAdopcionesBarChart() {
    const ctx = document.getElementById('adopcionesBarChart');
    if (!ctx) return;
    if (adopcionesBarInstance) { adopcionesBarInstance.destroy(); adopcionesBarInstance = null; }

    adopcionesBarInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['En Proceso', 'Aprobadas', 'En Seguimiento', 'Completadas'],
            datasets: [{
                label: 'Estado',
                data: [18, 24, 12, 32],
                backgroundColor: '#3b82f6',
                borderColor: '#2563eb',
                borderWidth: 0,
                borderRadius: 8,
                barThickness: 60
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#cbd5e1',
                    padding: 12,
                    cornerRadius: 8,
                    borderColor: 'rgba(59, 130, 246, 0.3)',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 32,
                    grid: { color: 'rgba(51, 65, 85, 0.25)', drawBorder: false },
                    border: { display: false },
                    ticks: {
                        color: '#94a3b8',
                        font: { size: 11 },
                        padding: 8,
                        stepSize: 8
                    }
                },
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                }
            }
        }
    });
}

// Inicializar gráficos de adopciones cuando se cambia a esa vista
function initAdopcionesCharts() {
    setTimeout(() => {
        createAdopcionesLineChart();
        createAdopcionesDoughnutChart();
        createAdopcionesBarChart();
    }, 100);
}

// ========================================
// GRÁFICOS DE VOLUNTARIOS
// ========================================
let volLineInstance = null;
let volPieInstance = null;
let volBarInstance = null;

function initVoluntariosCharts() {
    createVolLineChart();
    createVolPieChart();
    createVolBarChart();
}

// --- Line: Horas de Voluntariado (Mensual) ---
function createVolLineChart() {
    const ctx = document.getElementById('volLineChart');
    if (!ctx) return;
    if (volLineInstance) { volLineInstance.destroy(); volLineInstance = null; }

    volLineInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            datasets: [{
                label: 'Horas',
                data: [165, 185, 210, 240, 265, 280, 310, 335, 350, 365, 380, 398],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.08)',
                borderWidth: 2.5,
                tension: 0.35,
                fill: true,
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#0f172a',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#cbd5e1',
                    padding: 14,
                    cornerRadius: 10,
                    borderColor: 'rgba(59, 130, 246, 0.3)',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 450,
                    grid: { color: 'rgba(51, 65, 85, 0.25)', drawBorder: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8, stepSize: 100 }
                },
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                }
            }
        }
    });
}

// --- Pie: Distribución por Tarea (with external labels) ---
function createVolPieChart() {
    const ctx = document.getElementById('volPieChart');
    if (!ctx) return;
    if (volPieInstance) { volPieInstance.destroy(); volPieInstance = null; }

    volPieInstance = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Cuidado Animal 51%', 'Administrativo 24%', 'Eventos 15%', 'Transporte 10%'],
            datasets: [{
                data: [51, 24, 15, 10],
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6'],
                borderWidth: 2,
                borderColor: '#0f172a'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8',
                        font: { size: 11 },
                        padding: 15,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    padding: 12,
                    borderColor: '#334155',
                    borderWidth: 1,
                    callbacks: {
                        label: function (context) {
                            return ' ' + context.label;
                        }
                    }
                }
            }
        }
    });
}

// --- Bar: Voluntarios por Turno ---
function createVolBarChart() {
    const ctx = document.getElementById('volBarChart');
    if (!ctx) return;
    if (volBarInstance) { volBarInstance.destroy(); volBarInstance = null; }

    volBarInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Mañana', 'Tarde', 'Noche'],
            datasets: [{
                label: 'Voluntarios',
                data: [32, 38, 19],
                backgroundColor: '#3b82f6',
                borderRadius: 6,
                borderSkipped: false,
                barThickness: 72
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#cbd5e1',
                    padding: 14,
                    cornerRadius: 10,
                    borderColor: 'rgba(59, 130, 246, 0.3)',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 45,
                    grid: { color: 'rgba(51, 65, 85, 0.25)', drawBorder: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8, stepSize: 10 }
                },
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                }
            }
        }
    });
}

// ========================================
// DONACIONES CHARTS
// ========================================
let donLineInstance = null;
let donPieInstance = null;
let donBarInstance = null;

function initDonacionesCharts() {
    createDonLineChart();
    createDonPieChart();
    createDonBarChart();
}

function createDonLineChart() {
    const ctx = document.getElementById('donLineChart');
    if (!ctx) return;

    // Destruir instancia anterior si existe
    if (donLineInstance) {
        donLineInstance.destroy();
        donLineInstance = null;
    }

    donLineInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            datasets: [{
                label: 'Donaciones ($)',
                data: [8000, 9500, 12000, 13500, 15000, 18000, 19500, 21000, 22500, 24000, 25500, 27000],
                borderColor: '#22d3ee',
                backgroundColor: 'rgba(34, 211, 238, 0.1)',
                fill: true,
                tension: 0.35,
                borderWidth: 2,
                pointRadius: 4,
                pointBackgroundColor: '#22d3ee'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    padding: 12,
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    borderColor: '#334155',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(148, 163, 184, 0.1)' },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                },
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                }
            }
        }
    });
}

function createDonPieChart() {
    const ctx = document.getElementById('donPieChart');
    if (!ctx) return;

    // Destruir instancia anterior si existe
    if (donPieInstance) {
        donPieInstance.destroy();
        donPieInstance = null;
    }

    donPieInstance = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Monetarias 45%', 'Alimento 26%', 'Dedicaciones 13%', 'Suministros 11%'],
            datasets: [{
                data: [45, 26, 13, 11],
                backgroundColor: ['#22d3ee', '#3b82f6', '#f97316', '#a855f7'],
                borderWidth: 2,
                borderColor: '#0f172a'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8',
                        font: { size: 11 },
                        padding: 15,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    padding: 12,
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    borderColor: '#334155',
                    borderWidth: 1,
                    callbacks: {
                        label: function (context) {
                            return ' ' + context.label + ': ' + context.parsed + '%';
                        }
                    }
                }
            }
        }
    });
}

function createDonBarChart() {
    const ctx = document.getElementById('donBarChart');
    if (!ctx) return;

    // Destruir instancia anterior si existe
    if (donBarInstance) {
        donBarInstance.destroy();
        donBarInstance = null;
    }

    donBarInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Transferencia', 'Tarjetas', 'Efectivo', 'PayPal'],
            datasets: [{
                label: 'Donaciones',
                data: [120, 95, 65, 42],
                backgroundColor: '#22d3ee',
                borderRadius: 6,
                barThickness: 48
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    padding: 12,
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    borderColor: '#334155',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(148, 163, 184, 0.1)' },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                },
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                }
            }
        }
    });
}

// ========================================
// INCIDENCIAS CHARTS
// ========================================
let incLineInstance = null;
let incPieInstance = null;
let incBarInstance = null;

function initIncidenciasCharts() {
    createIncLineChart();
    createIncPieChart();
    createIncBarChart();
}

function createIncLineChart() {
    const ctx = document.getElementById('incLineChart');
    if (!ctx) return;

    // Destruir instancia anterior si existe
    if (incLineInstance) {
        incLineInstance.destroy();
        incLineInstance = null;
    }

    incLineInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            datasets: [{
                label: 'Incidentes',
                data: [12, 15, 8, 18, 14, 9, 5, 11, 7, 13, 6, 4],
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                fill: true,
                tension: 0.35,
                borderWidth: 2,
                pointRadius: 5,
                pointBackgroundColor: '#ef4444',
                pointBorderColor: '#1e293b',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    padding: 12,
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    borderColor: '#334155',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(148, 163, 184, 0.1)' },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                },
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                }
            }
        }
    });
}

function createIncPieChart() {
    const ctx = document.getElementById('incPieChart');
    if (!ctx) return;

    // Destruir instancia anterior si existe
    if (incPieInstance) {
        incPieInstance.destroy();
        incPieInstance = null;
    }

    incPieInstance = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Salud Animal 41%', 'Instalaciones 25%', 'Clima 7%', 'Seguridad 16%', 'Personal 11%'],
            datasets: [{
                data: [41, 25, 7, 16, 11],
                backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#a855f7', '#22d3ee'],
                borderWidth: 2,
                borderColor: '#0f172a'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8',
                        font: { size: 11 },
                        padding: 15,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    padding: 12,
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    borderColor: '#334155',
                    borderWidth: 1,
                    callbacks: {
                        label: function (context) {
                            return ' ' + context.label;
                        }
                    }
                }
            }
        }
    });
}

function createIncBarChart() {
    const ctx = document.getElementById('incBarChart');
    if (!ctx) return;

    // Destruir instancia anterior si existe
    if (incBarInstance) {
        incBarInstance.destroy();
        incBarInstance = null;
    }

    incBarInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Crítico', 'Alto', 'Medio', 'Bajo'],
            datasets: [{
                label: 'Incidentes',
                data: [8, 15, 30, 55],
                backgroundColor: '#22d3ee',
                borderRadius: 6,
                barThickness: 48
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    padding: 12,
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    borderColor: '#334155',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(148, 163, 184, 0.1)' },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                },
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                }
            }
        }
    });
}

// ========================================
// REPORTES CHARTS
// ========================================
let repLineInstance = null;
let repBarInstance = null;

function initReportesCharts() {
    createRepLineChart();
    createRepBarChart();
}

function createRepLineChart() {
    const ctx = document.getElementById('repLineChart');
    if (!ctx) return;

    // Destruir instancia anterior si existe
    if (repLineInstance) {
        repLineInstance.destroy();
        repLineInstance = null;
    }

    repLineInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            datasets: [
                {
                    label: 'Ingresos',
                    data: [14, 16, 18, 21, 19, 23, 25, 27, 26, 29, 31, 34],
                    borderColor: '#22d3ee',
                    backgroundColor: 'rgba(34, 211, 238, 0.1)',
                    fill: false,
                    tension: 0.35,
                    borderWidth: 2,
                    pointRadius: 4,
                    pointBackgroundColor: '#22d3ee'
                },
                {
                    label: 'Adopciones',
                    data: [4, 12, 15, 17, 14, 18, 16, 19, 21, 23, 25, 28],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: false,
                    tension: 0.35,
                    borderWidth: 2,
                    pointRadius: 4,
                    pointBackgroundColor: '#3b82f6'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8',
                        font: { size: 11 },
                        padding: 15,
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    padding: 12,
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    borderColor: '#334155',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(148, 163, 184, 0.1)' },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                },
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                }
            }
        }
    });
}

function createRepBarChart() {
    const ctx = document.getElementById('repBarChart');
    if (!ctx) return;

    // Destruir instancia anterior si existe
    if (repBarInstance) {
        repBarInstance.destroy();
        repBarInstance = null;
    }

    repBarInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            datasets: [{
                label: 'Donaciones',
                data: [8000, 12000, 9500, 13500, 12000, 18000, 21000, 19500, 17000, 22000, 26000, 30000],
                backgroundColor: '#f59e0b',
                borderRadius: 6,
                categoryPercentage: 0.8, // espacio entre columnas
                barPercentage: 0.9       // grosor de cada barra
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    padding: 12,
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    borderColor: '#334155',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(148, 163, 184, 0.1)' },
                    border: { display: false },
                    ticks: {
                        color: '#94a3b8',
                        font: { size: 11 },
                        padding: 8,
                        callback: function (value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                },
                x: {
                    grid: { display: false },
                    border: { display: false },
                    ticks: { color: '#94a3b8', font: { size: 11 }, padding: 8 }
                }
            }
        }
    });
}

// ========================================
// CONFIGURACIÓN - MANEJO DE PESTAÑAS
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    // Manejo de pestañas de configuración
    const configNavButtons = document.querySelectorAll('.config-nav-btn');
    
    configNavButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-config-tab');
            
            // Remover clase active de todos los botones
            configNavButtons.forEach(btn => btn.classList.remove('active'));
            
            // Agregar clase active al botón clickeado
            this.classList.add('active');
            
            // Ocultar todos los contenidos de pestañas
            const allTabContents = document.querySelectorAll('.config-tab-content');
            allTabContents.forEach(content => content.classList.remove('active'));
            
            // Mostrar el contenido de la pestaña seleccionada
            const targetContent = document.getElementById('config-tab-' + targetTab);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
});

// ========================================
// EXPORTAR FUNCIONES (si se necesita en otros archivos)
// ========================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatNumber,
        formatCurrency,
        getGreeting,
        navigateTo
    };
}