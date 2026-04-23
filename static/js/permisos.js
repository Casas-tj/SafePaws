/* ROLES DEL SISTEMA */
const ROLES = {
    ENCARGADO: 'ENCARGADO',
    OPERATIVO_STOCK: 'OPERATIVO_STOCK',
    ADMINISTRATIVO: 'ADMINISTRATIVO',
    ADMIN_SISTEMA: 'ADMIN_SISTEMA'
};

/* PERMISOS POR ROL */
const PERMISSIONS = {
    ENCARGADO: {
        view: [
            'animales',
            'adopciones',
            'voluntarios',
            'usuarios',
            'incidencias',
            'donaciones',
            'inventario',
            'dashboard',
            'reportes',
        ],
        actions: [
            'cambiar_estado',
            'asignar_voluntario'
        ]
    },

    OPERATIVO_STOCK: {
        view: [
            'inventario',
            'donaciones',
            'productos',
            'movimientos_stock'
        ],
        actions: [
            'crear_producto',
            'actualizar_stock',
            'registrar_donacion',
            'registrar_salida'
        ]
    },

    ADMINISTRATIVO: {
        view: [
            'animales',
            'usuarios',
            'voluntarios',
            'adopciones',
            'incidencias'
        ],
        actions: [
            'crear_animal',
            'editar_animal',
            'crear_usuario',
            'editar_usuario',
            'registrar_incidencia',
            'crear_adopcion',
            'actualizar_adopcion'
        ]
    },

    ADMIN_SISTEMA: {
        view: ['*'],
        actions: ['*']
    }
};

/* OBTENER ROL ACTUAL */
function getCurrentRole() {
    // Intentamos leerlo de ambas formas para estar seguros
    const role = localStorage.getItem('role');
    if (role) return role;

    const user = JSON.parse(localStorage.getItem('user'));
    return user?.role || null;
}

/* VALIDAR ACCESO A VISTA */
function canView(view) {
    const role = getCurrentRole();
    if (!role || !PERMISSIONS[role]) return false;

    const views = PERMISSIONS[role].view;
    return views.includes('*') || views.includes(view);
}

/* VALIDAR ACCIÓN */
function canDo(action) {
    const role = getCurrentRole();
    if (!role || !PERMISSIONS[role]) return false;

    const actions = PERMISSIONS[role].actions;
    return actions.includes('*') || actions.includes(action);
}

/* OCULTAR ELEMENTOS SEGÚN ROL */
function applyRoleVisibility() {

    /* CARDS (home.html) */
    document.querySelectorAll('.card').forEach(card => {
        const section = card.getAttribute('data-section');
        if (!section || !canView(section)) {
            card.style.display = 'none';
        }
    });

    /* BOTONES / ACCIONES */
    document.querySelectorAll('[data-action]').forEach(el => {
        const action = el.dataset.action;
        if (!canDo(action)) {
            el.style.display = 'none';
        }
    });
}

/* PROTEGER ACCESO DIRECTO A PÁGINA */
function protectPage(requiredView) {
    if (!canView(requiredView)) {
        alert('No tienes permisos para acceder a esta sección');
        window.location.replace('/home.html');
    }
}

/* INICIALIZAR */
document.addEventListener('DOMContentLoaded', applyRoleVisibility);

