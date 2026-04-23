from django.shortcuts import render


def home(request):
    return render(request, 'dashboard/home.html', {
        "headertitle": "SafePaws",
        "headersubtitle": "Sistema de gestión interna de la protectora de animales SafePaws",
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })


def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {
        # "headertitle": "SafePaws",
        # "headersubtitle": "Donde cada \nhuella cuenta",
        "btn_back": "Volver a home",
        "back_url": "home",
        # "headtitlebtn": "Nuevo Gasto",
        # "headlink": 'gastos-add'
    })


