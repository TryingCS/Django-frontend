from django.shortcuts import render


def media(request):
    track = {
        'title': 'Neon Horizon',
        'artist': 'CyberVoid Ensemble',
        'album': 'Midnight Synthesis',
        'duration': '3:42',
        'current': '1:15',
    }
    playlist = [
        {'title': 'Neon Horizon', 'artist': 'CyberVoid Ensemble', 'duration': '3:42', 'active': True},
        {'title': 'Digital Rain', 'artist': 'Glitch Protocol', 'duration': '4:15', 'active': False},
        {'title': 'Synthetic Dreams', 'artist': 'Neural Mesh', 'duration': '5:01', 'active': False},
        {'title': 'Binary Sunset', 'artist': 'Null Pointer', 'duration': '3:28', 'active': False},
        {'title': 'Quantum Echo', 'artist': 'Phase Drift', 'duration': '4:44', 'active': False},
    ]
    return render(request, 'media_app/media.html', {'track': track, 'playlist': playlist})
