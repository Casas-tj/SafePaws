from django.shortcuts import render, redirect


def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        # validación simple ejemplo
        if usuario == "Administrador" and password == "ads123":
            return redirect('home')  # ← AQUÍ CAMBIA DE PÁGINA
        elif usuario == "Encargado" and password == "enc123":
            return redirect('home')
        elif usuario == "Operativo" and password == "os123":
            return redirect('home')
        elif usuario == "Administrativo" and password == "admin123":
            return redirect('home')
    return render(request, 'login.html', {})
