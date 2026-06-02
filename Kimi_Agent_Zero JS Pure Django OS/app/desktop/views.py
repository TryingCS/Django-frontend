from django.shortcuts import render


def desktop(request):
    booted = request.session.get('booted', False)
    if not booted:
        request.session['booted'] = True
    return render(request, 'desktop/desktop.html', {'show_boot': not booted})
