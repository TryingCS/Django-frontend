from django.shortcuts import render


def terminal(request):
    lines = [
        "> INITIALIZING SYNTHEX KERNEL...",
        "> MOUNTING VIRTUAL DRIVES... [OK]",
        "> LOADING USER PROFILE... DONE",
        "> CONNECTING TO NEURAL INTERFACE...",
        "> UPLINK ESTABLISHED. WELCOME, OPERATOR.",
    ]
    return render(request, 'terminal/terminal.html', {'lines': lines})
