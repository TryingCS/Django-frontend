from django.shortcuts import render, redirect


def settings(request):
    saved = request.GET.get('saved', False)
    
    if request.method == 'POST':
        # In a real app, we'd save these to a model or session
        # For now, we just redirect with a success indicator
        return redirect('/settings/?saved=1')
    
    # Default settings (would come from DB/session in production)
    config = {
        'dark_mode': True,
        'notifications': True,
        'sound_effects': False,
        'auto_update': True,
        'high_contrast': False,
        'reduce_motion': False,
        'network_proxy': False,
        'debug_mode': False,
    }
    
    return render(request, 'settings_app/settings.html', {
        'config': config,
        'saved': saved,
    })
