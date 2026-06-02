from django.shortcuts import render


def sysmon(request):
    stats = {
        'cpu_percent': 68,
        'ram_percent': 42,
        'disk_percent': 77,
        'net_up': 12.5,
        'net_down': 48.3,
        'uptime': '14d 07h 33m',
        'processes': 284,
        'threads': 1024,
    }
    return render(request, 'sysmon/sysmon.html', {'stats': stats})
