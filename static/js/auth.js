/* LIMPIAR INTENTOS FALLIDOS AL INICIAR SESIÓN */
if (!localStorage.getItem("user")) {
    localStorage.removeItem("attempts");
}

// 1. CONFIGURACIÓN INICIAL
const USERS = {
    "Administrador": { password: "ads123", role: "ADMIN_SISTEMA" },
    "Encargado": { password: "enc123", role: "ENCARGADO" },
    "Operativo": { password: "os123", role: "OPERATIVO_STOCK" },
    "Administrativo": { password: "adm123", role: "ADMINISTRATIVO" }
};

// 2. FUNCIONES DE ESTADO DE SESIÓN
function isAuthenticated() {
    // Usamos 'user' como clave única para evitar conflictos con otros scripts
    return !!localStorage.getItem("user");
}

function requireAuth() {
    if (!isAuthenticated()) {
        console.warn("Acceso denegado: Usuario no autenticado.");
        window.location.replace("login.html");
    }
}

function redirectIfAuthenticated() {
    if (isAuthenticated()) {
        window.location.replace("home.html");
    }
}

// 3. ACCIONES DE LOGIN Y LOGOUT
function login(username, role) {
    const user = { 
        username: username, 
        role: role,
        loginTime: new Date().getTime()
    };
    localStorage.setItem("user", JSON.stringify(user));
    // Sincronizamos con claves que puedan usar otros scripts antiguos por compatibilidad
    localStorage.setItem("safepaws_authenticated", "true");
    
    window.location.replace("home.html");
}

function logout() {
    if (!confirm("¿Deseas cerrar sesión?")) return;
    
    // Limpieza total de almacenamiento
    localStorage.removeItem("user");
    localStorage.removeItem("safepaws_authenticated");
    localStorage.removeItem("attempts");
    sessionStorage.clear();
    
    window.location.replace("login.html");
}

// 4. INICIALIZACIÓN Y MANEJO DEL FORMULARIO
document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const userNameEl = document.getElementById("user-name");

    // Si estamos en una página interna, mostrar el nombre del usuario
    if (isAuthenticated() && userNameEl) {
        const user = JSON.parse(localStorage.getItem("user"));
        userNameEl.textContent = user.username;
    }

    // Lógica específica para la página de LOGIN
    if (loginForm) {
        redirectIfAuthenticated();
        const errorMsg = document.getElementById("error");

        loginForm.addEventListener("submit", (e) => {
            e.preventDefault();
            
            const userVal = document.getElementById("username").value.trim();
            const passVal = document.getElementById("password").value.trim();

            if (!userVal || !passVal) {
                if (errorMsg) errorMsg.textContent = "Por favor, complete todos los campos.";
                return;
            }

            // Validación contra el objeto USERS
            if (USERS[userVal] && USERS[userVal].password === passVal) {
                localStorage.removeItem("attempts");
                login(userVal, USERS[userVal].role);
            } else {
                // Manejo de intentos fallidos
                let attempts = parseInt(localStorage.getItem("attempts")) || 0;
                attempts++;
                localStorage.setItem("attempts", attempts);

                if (errorMsg) {
                    if (attempts >= 3) {
                        errorMsg.textContent = "Demasiados intentos fallidos. Inténtelo más tarde.";
                        loginForm.querySelector("button").disabled = true;
                    } else {
                        errorMsg.textContent = "Usuario o contraseña incorrectos.";
                    }
                }
            }
        });
    }
});