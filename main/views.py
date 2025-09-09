from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'app_name': 'Sebelah Stadion',
        'name': 'Firos Aqiela Zufa',   # ganti dengan namamu
        'class': 'PBP F'        # ganti dengan kelasmu
    }
    return render(request, "main.html", context)