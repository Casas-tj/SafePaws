// Verifica si el usuario tiene una sesión activa antes de mostrar nada.

//Si no hay rol o marca de autenticación, lo expulsa al login.
function checkAuth() {
    const role = localStorage.getItem("role");
    const isAuthenticated = localStorage.getItem('safepaws_authenticated');

    if (!role || isAuthenticated !== 'true') {
        window.location.replace("login.html");
    }
}

// Inicialización del DOM
document.addEventListener("DOMContentLoaded", () => {
    // Ejecutar funciones principales de interfaz
    displayUserName();
    initNavigation();
    updateDashboardStats();

    // Iniciar temporizador de inactividad
    resetInactivityTimer();
});

// Recupera el nombre del usuario del almacenamiento local y lo muestra en el header.
function displayUserName() {
    const username = localStorage.getItem('safepaws_user') || localStorage.getItem('user');
    const userNameElement = document.getElementById('user-name') || document.querySelector('.user-name');

    if (userNameElement && username) {
        userNameElement.textContent = username;
    }
}

// Limpia todos los datos de sesión y redirige al login.
// Se usa tanto para el botón de salir como para la inactividad.
function logout() {
    if (arguments.length > 0 && !confirm("¿Deseas cerrar sesión?")) return;

    localStorage.clear();
    sessionStorage.clear();
    window.location.replace("login.html");
}

// Control de inactividad: Cierra la sesión tras 15 minutos sin movimiento.
let inactivityTimer;
function resetInactivityTimer() {
    clearTimeout(inactivityTimer);
    // 15 minutos
    inactivityTimer = setTimeout(logout, 15 * 60 * 1000);
}

// Escuchar movimientos para resetear el tiempo de vida de la sesión
['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(evt => {
    document.addEventListener(evt, resetInactivityTimer);
});

// Configura el evento click en las tarjetas del menú principal.
// Verifica permisos antes de permitir el acceso.
function initNavigation() {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('click', () => {
            const requiredView = card.dataset.view;

            // Verifica si la función canView (de permisos.js) existe y da permiso
            if (typeof canView === "function" && !canView(requiredView)) {
                alert('No tienes permisos suficientes para acceder a la sección: ' + requiredView);
                return;
            }

            // Si tiene permiso, el atributo onclick del HTML o la URL de la tarjeta hará el resto
            const targetUrl = card.getAttribute('onclick');
            if (!targetUrl) {
                const sectionId = card.dataset.section;
                console.log('Navegando internamente a:', sectionId);
                // Aquí podrías añadir lógica para mostrar/ocultar DIVs si no usas páginas separadas
            }
        });
    });
}

// 5. ESTADÍSTICAS DEL DASHBOARD

// Carga datos del localStorage y actualiza los contadores visuales si existen.
function updateDashboardStats() {
    // Carga de datos con fallback a array vacío si no existen
    const animals = JSON.parse(localStorage.getItem('animals')) || [];
    const adoptions = JSON.parse(localStorage.getItem('adoptions')) || [];
    const incidents = JSON.parse(localStorage.getItem('incidents')) || [];
    const volunteers = JSON.parse(localStorage.getItem('volunteers')) || [];
    const donations = JSON.parse(localStorage.getItem('donations')) || [];

    // Mapeo de elementos del DOM
    const stats = {
        'totalAnimals': `${animals.length} registrados`,
        'totalAdoptions': `${adoptions.length} realizadas`,
        'totalIncidents': `${incidents.length} abiertas`,
        'totalVolunteers': `${volunteers.length} activos`
    };

    // Actualizar textos de forma dinámica
    for (const [id, text] of Object.entries(stats)) {
        const el = document.getElementById(id);
        if (el) el.textContent = text;
    }

    // Cálculo especial para el total de donaciones en moneda
    const totalDonationsEl = document.getElementById('totalDonations');
    if (totalDonationsEl) {
        const totalMoney = donations.reduce((sum, d) => sum + Number(d.amount || 0), 0);
        totalDonationsEl.textContent = `${totalMoney.toLocaleString()} €`;
    }
}

