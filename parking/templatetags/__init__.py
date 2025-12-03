from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def time_since_now(value):
    """Calcula el tiempo transcurrido desde value hasta ahora"""
    if not value:
        return ""
    
    now = timezone.now()
    delta = now - value
    
    total_minutes = int(delta.total_seconds() / 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

@register.filter
def duration_between(start, end):
    """Calcula la duración entre dos fechas"""
    if not start or not end:
        return ""
    
    delta = end - start
    total_minutes = int(delta.total_seconds() / 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"
