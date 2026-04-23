// 1. Configuración de usuarios y roles
const users = {
    "Administrador": { password: "ads123", role: "ADMIN_SISTEMA" },
    "Encargado": { password: "enc123", role: "ENCARGADO" },
    "Operativo": { password: "os123", role: "OPERATIVO_STOCK" },
    "Administrativo": { password: "adm123", role: "ADMINISTRATIVO" }
};

// 2. Verificación inmediata de sesión
function checkAuthentication() {
    const role = localStorage.getItem("role");
    const user = localStorage.getItem("user");
    const isAuthenticated = localStorage.getItem("safepaws_authenticated");
    const currentPage = window.location.pathname;

    if ((role && user) || isAuthenticated === "true") {
        if (currentPage.includes('login.html') || currentPage.endsWith('/')) {
            window.location.replace("home.html");
        }
    }
}

checkAuthentication();

// 3. 
document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const errorDisplay = document.getElementById('error');
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    // Referencias para "Recordarme"
    const usernameInput = document.getElementById('username');
    const rememberCheckbox = document.getElementById('remember');

    // Cargar usuario si fue recordado previamente
    const savedUser = localStorage.getItem('remembered_user');
    if (savedUser && usernameInput) {
        usernameInput.value = savedUser;
        if (rememberCheckbox) rememberCheckbox.checked = true;
    }

    // Funcionalidad de Mostrar/Ocultar contraseña
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function () {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.textContent = type === 'password' ? '👁️' : '🔒';
        });
    }

    if (!loginForm) return;

    // Bloqueo por intentos (Ya lo tenías)
    const savedAttempts = parseInt(localStorage.getItem("attempts")) || 0;
    if (savedAttempts >= 3) {
        disableLoginForm(loginForm, errorDisplay);
    }

    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        if (errorDisplay) errorDisplay.textContent = "";

        if (!username || !password) {
            if (errorDisplay) errorDisplay.textContent = "Por favor, complete todos los campos.";
            return;
        }

        const userData = users[username];

        if (userData && userData.password === password) {
            // 3. NUEVO: Lógica para guardar o borrar el nombre de usuario
            if (rememberCheckbox && rememberCheckbox.checked) {
                localStorage.setItem('remembered_user', username);
            } else {
                localStorage.removeItem('remembered_user');
            }

            // Datos de sesión (Ya lo tenías)
            localStorage.setItem('safepaws_authenticated', 'true');
            localStorage.setItem('safepaws_user', username);
            localStorage.setItem('user', username);
            localStorage.setItem('role', userData.role);
            localStorage.removeItem('attempts');
            window.location.replace('home.html');
        } else {
            handleFailedAttempt(passwordInput, errorDisplay, loginForm);
        }
    });
});

//Gestiona el contador de intentos fallidos
function handleFailedAttempt(passwordInput, errorDisplay, loginForm) {
    let attempts = parseInt(localStorage.getItem("attempts")) || 0;
    attempts++;
    localStorage.setItem("attempts", attempts);

    if (passwordInput) passwordInput.value = "";

    if (attempts >= 3) {
        disableLoginForm(loginForm, errorDisplay);
    } else {
        if (errorDisplay) errorDisplay.textContent = `Usuario o contraseña incorrectos. Intento ${attempts} de 3.`;
    }
}

//Deshabilita el botón de ingreso tras exceder intentos
function disableLoginForm(loginForm, errorDisplay) {
    const submitBtn = document.getElementById("loginBtn");
    if (submitBtn) submitBtn.disabled = true;
    if (submitBtn) submitBtn.style.backgroundColor = "#ccc";
    if (errorDisplay) errorDisplay.textContent = "Demasiados intentos fallidos. Inténtelo más tarde.";
}