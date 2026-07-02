from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def static_fallback(name):
    resources = getattr(settings, 'STATIC_CDN_RESOURCES')
    res = resources.get(name)

    if not res:
        return ''
    
    cdn_url = res.get('url')
    integrity_hash = res.get('integrity')
    local_path = res.get('local')

    if name.endswith('_css'):
        html_str = f'<link rel="stylesheet" href="{cdn_url}" ' \
            f'integrity="{integrity_hash}" crossorigin="anonymous" ' \
            f'onerror="var link=document.createElement(\'link\'); link.rel=\'stylesheet\'; link.href=\'{local_path}\'; document.head.appendChild(link);"/>'
        
        return mark_safe(html_str)
    
    elif name.endswith('_js'):
        html_str = f'<script src="{cdn_url}" ' \
            f'integrity="{integrity_hash}" crossorigin="anonymous" ' \
            f'onerror="var s=document.createElement(\'script\'); s.src=\'{local_path}\'; document.body.appendChild(s);"></script>'

        return mark_safe(html_str)
    else:
        return ''
    