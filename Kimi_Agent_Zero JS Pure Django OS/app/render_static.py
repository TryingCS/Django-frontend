#!/usr/bin/env python
"""Pre-render Django templates to static HTML for deployment."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'synthex.settings')
django.setup()

from django.template.loader import render_to_string

# Output directory for static site
OUTPUT_DIR = '/mnt/agents/output/static_site'
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, 'static', 'css'), exist_ok=True)

# Copy CSS file
with open('/mnt/agents/output/app/static/css/synthex.css', 'r') as f:
    css_content = f.read()

with open(os.path.join(OUTPUT_DIR, 'static', 'css', 'synthex.css'), 'w') as f:
    f.write(css_content)

print("CSS copied.")

# Render each page
pages = {
    'index.html': ('desktop/desktop.html', {'show_boot': True}),
    'terminal/index.html': ('terminal/terminal.html', {
        'lines': [
            "> INITIALIZING SYNTHEX KERNEL...",
            "> MOUNTING VIRTUAL DRIVES... [OK]",
            "> LOADING USER PROFILE... DONE",
            "> CONNECTING TO NEURAL INTERFACE...",
            "> UPLINK ESTABLISHED. WELCOME, OPERATOR.",
        ]
    }),
    'sysmon/index.html': ('sysmon/sysmon.html', {
        'stats': {
            'cpu_percent': 68,
            'ram_percent': 42,
            'disk_percent': 77,
            'net_up': 12.5,
            'net_down': 48.3,
            'uptime': '14d 07h 33m',
            'processes': 284,
            'threads': 1024,
        }
    }),
    'media/index.html': ('media_app/media.html', {
        'track': {
            'title': 'Neon Horizon',
            'artist': 'CyberVoid Ensemble',
            'album': 'Midnight Synthesis',
            'duration': '3:42',
            'current': '1:15',
        },
        'playlist': [
            {'title': 'Neon Horizon', 'artist': 'CyberVoid Ensemble', 'duration': '3:42', 'active': True},
            {'title': 'Digital Rain', 'artist': 'Glitch Protocol', 'duration': '4:15', 'active': False},
            {'title': 'Synthetic Dreams', 'artist': 'Neural Mesh', 'duration': '5:01', 'active': False},
            {'title': 'Binary Sunset', 'artist': 'Null Pointer', 'duration': '3:28', 'active': False},
            {'title': 'Quantum Echo', 'artist': 'Phase Drift', 'duration': '4:44', 'active': False},
        ]
    }),
    'settings/index.html': ('settings_app/settings.html', {
        'config': {
            'dark_mode': True,
            'notifications': True,
            'sound_effects': False,
            'auto_update': True,
            'high_contrast': False,
            'reduce_motion': False,
            'network_proxy': False,
            'debug_mode': False,
        },
        'saved': False,
    }),
}

from django.http import HttpRequest
from django.template.context_processors import request as request_processor

for filepath, (template_name, context) in pages.items():
    fullpath = os.path.join(OUTPUT_DIR, filepath)
    os.makedirs(os.path.dirname(fullpath), exist_ok=True)

    # Build a mock request for the template context
    mock_request = HttpRequest()
    mock_request.method = 'GET'
    mock_request.path = '/' + filepath.replace('index.html', '').rstrip('/')
    if not mock_request.path or mock_request.path == '/':
        mock_request.path = '/'

    context['request'] = mock_request
    context['csrf_token'] = 'static-csrf-token-placeholder'

    # Render template
    html = render_to_string(template_name, context)

    # Fix static URLs and links for static deployment
    html = html.replace('href="/static/', 'href="../static/')
    html = html.replace('href="/"', 'href="../index.html"')
    html = html.replace('href="/terminal/"', 'href="../terminal/index.html"')
    html = html.replace('href="/sysmon/"', 'href="../sysmon/index.html"')
    html = html.replace('href="/media/"', 'href="../media/index.html"')
    html = html.replace('href="/settings/"', 'href="../settings/index.html"')

    # For index.html, fix the relative paths (one less ../)
    if filepath == 'index.html':
        html = html.replace('href="../static/', 'href="static/')
        html = html.replace('href="../index.html"', 'href="index.html"')
        html = html.replace('href="../terminal/index.html"', 'href="terminal/index.html"')
        html = html.replace('href="../sysmon/index.html"', 'href="sysmon/index.html"')
        html = html.replace('href="../media/index.html"', 'href="media/index.html"')
        html = html.replace('href="../settings/index.html"', 'href="settings/index.html"')

    # Also fix the request.path-based active states manually
    # Replace the template conditional with static classes
    path_map = {
        '/terminal/': 'terminal',
        '/sysmon/': 'sysmon',
        '/media/': 'media',
        '/settings/': 'settings',
    }

    with open(fullpath, 'w') as f:
        f.write(html)

    print(f"Rendered: {filepath}")

# Create a settings-saved variant
saved_context = pages['settings/index.html'][1].copy()
saved_context['saved'] = True
saved_context['request'] = mock_request
saved_context['csrf_token'] = 'static-csrf-token-placeholder'
saved_html = render_to_string('settings_app/settings.html', saved_context)
saved_html = saved_html.replace('href="/static/', 'href="../static/')
saved_html = saved_html.replace('href="/"', 'href="../index.html"')
saved_html = saved_html.replace('href="/terminal/"', 'href="../terminal/index.html"')
saved_html = saved_html.replace('href="/sysmon/"', 'href="../sysmon/index.html"')
saved_html = saved_html.replace('href="/media/"', 'href="../media/index.html"')
saved_html = saved_html.replace('href="/settings/"', 'href="../settings/index.html"')

with open(os.path.join(OUTPUT_DIR, 'settings', 'saved.html'), 'w') as f:
    f.write(saved_html)

print("Rendered: settings/saved.html")
print("\nStatic site generated successfully!")
