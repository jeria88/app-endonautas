from django import template

register = template.Library()


@register.filter
def dict_get(d, key):
    """Accede a d[key] con clave variable desde el template."""
    if hasattr(d, "get"):
        return d.get(key)
    return None


@register.filter
def pct(value):
    """Convierte una confianza 0..1 en porcentaje entero (0.69 → 69)."""
    try:
        return int(round(float(value) * 100))
    except (TypeError, ValueError):
        return 0


@register.filter
def is_selected(valor, cur):
    """True si `valor` es el signo elegido (radio) o está entre los elegidos (checkbox)."""
    if cur is None:
        return False
    if isinstance(cur, (list, tuple, set)):
        return valor in cur
    return valor == cur
