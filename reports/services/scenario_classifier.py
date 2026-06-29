"""
Clasifica el escenario semanal en verde/amarillo/rojo según umbrales del plan H2 2026.
Los umbrales están aquí, no en el management command, para poder testearse y ajustarse.
"""

# MRR proyectado por mes (USD) — escenario amarillo del plan H2 2026
# Índice = mes calendario (7=julio, 8=agosto, ..., 12=diciembre)
MRR_PROYECTADO = {
    7: 50,
    8: 100,
    9: 180,
    10: 250,
    11: 340,
    12: 430,
}

THRESHOLDS = {
    'retencion_d30_verde': 40.0,
    'retencion_d30_amarillo': 25.0,
    'mrr_factor_verde': 1.0,
    'mrr_factor_amarillo': 0.5,
    'activacion_min': 20.0,
    'open_rate_min': 20.0,
}


def classify(kpis: dict, month: int) -> tuple:
    """
    Devuelve (escenario, alertas, decision_sugerida).
    kpis: dict con todos los campos del KPISnapshot.
    month: mes calendario para saber MRR proyectado.
    """
    mrr_base = MRR_PROYECTADO.get(month, MRR_PROYECTADO[12])
    ret_d30 = kpis.get('retencion_d30_pct', 0)
    mrr = kpis.get('mrr_estimado_usd', 0)
    alertas = []

    # Alertas individuales
    if ret_d30 < THRESHOLDS['retencion_d30_amarillo']:
        alertas.append('retencion_d30_critica')
    elif ret_d30 < THRESHOLDS['retencion_d30_verde']:
        alertas.append('retencion_d30_baja')

    if mrr < mrr_base * THRESHOLDS['mrr_factor_amarillo']:
        alertas.append('mrr_critico')
    elif mrr < mrr_base * THRESHOLDS['mrr_factor_verde']:
        alertas.append('mrr_bajo')

    if kpis.get('activacion_pct', 0) < THRESHOLDS['activacion_min']:
        alertas.append('activacion_baja')

    if kpis.get('email_open_rate_pct', 0) < THRESHOLDS['open_rate_min']:
        alertas.append('open_rate_bajo')

    if kpis.get('registros_nuevos', 0) == 0:
        alertas.append('sin_registros_semana')

    # Clasificación
    if ret_d30 < THRESHOLDS['retencion_d30_amarillo'] or mrr < mrr_base * THRESHOLDS['mrr_factor_amarillo']:
        escenario = 'rojo'
    elif ret_d30 < THRESHOLDS['retencion_d30_verde'] or mrr < mrr_base * THRESHOLDS['mrr_factor_verde']:
        escenario = 'amarillo'
    else:
        escenario = 'verde'

    decision = _decision(escenario, alertas, mrr_base)
    return escenario, alertas, decision


def _decision(escenario, alertas, mrr_base):
    if escenario == 'verde':
        return 'Continuar plan. Revisar si activar Función B (verificar retención d30 ≥30% sostenida 4 semanas).'
    if escenario == 'amarillo':
        partes = ['Mantener foco distribución. No agregar features.']
        if 'activacion_baja' in alertas:
            partes.append('Priorizar mejora onboarding (primer test en 24h).')
        if 'open_rate_bajo' in alertas:
            partes.append('Revisar asunto emails y horario de envío.')
        return ' '.join(partes)
    # rojo
    partes = ['ATENCIÓN: escenario crítico.']
    if 'retencion_d30_critica' in alertas:
        partes.append('Retención d30 <25%: problema de producto. Revisar primera sesión Espejo.')
    if 'mrr_critico' in alertas:
        partes.append(f'MRR <50% del target (${mrr_base * 0.5:.0f}): revisar oferta y funnel de conversión.')
    partes.append('Evaluar si pivotar a modelo sesiones 1a1 para generar ingreso inmediato.')
    return ' '.join(partes)
