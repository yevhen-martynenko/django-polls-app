from django.shortcuts import render


def index(request):
    page = {
        'title': 'Polls'
    }
    return render(request, 'index.html', page)


def site_map(request):
    page = {
        'title': 'Site Map',
        'previous_page': request.headers.get('Referer'),
    }
    return render(request, 'site_map.html', page)

def csrf_attack(request):
    return render(request, 'csrf_attack.html')