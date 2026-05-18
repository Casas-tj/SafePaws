from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if request.POST.get("remember"):
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
                return redirect("home")
            else:
                return render(request, "accounts/login.html", {
                    "error": "Usuario inactivo"
                })

        return render(request, "accounts/login.html", {
            "error": "Credenciales incorrectas"
        })

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("accounts:login")
