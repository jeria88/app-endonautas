"""
Genera el MD legible del snapshot semanal.
"""
from datetime import date


ESCENARIO_EMOJI = {'verde': '🟢', 'amarillo': '🟡', 'rojo': '🔴'}


def render(kpis: dict, escenario: str, alertas: list, decision: str, week_start: date, week_number: int) -> str:
    emoji = ESCENARIO_EMOJI.get(escenario, '⚪')
    lines = [
        f"# Reporte KPI — Semana {week_start.year}-W{week_number:02d}",
        f"**Período:** {week_start.strftime('%d %b')} – {(date.fromordinal(week_start.toordinal() + 6)).strftime('%d %b %Y')}",
        f"**Escenario:** {emoji} {escenario.upper()}",
        "",
        "## Usuarios y retención",
        f"- Registros nuevos esta semana: **{kpis.get('registros_nuevos', 0)}**",
        f"- Activación (test en 7d): **{kpis.get('activacion_pct', 0):.1f}%**",
        f"- Retención d7: **{kpis.get('retencion_d7_pct', 0):.1f}%**",
        f"- Retención d30: **{kpis.get('retencion_d30_pct', 0):.1f}%**",
        f"- Sesiones Espejo/usuario (últimos 30d): **{kpis.get('sesiones_espejo_avg', 0):.1f}**",
        "",
        "## Revenue",
        f"- Navegantes total: **{kpis.get('navegantes_total', 0)}** (+{kpis.get('navegantes_nuevos_semana', 0)} esta semana)",
        f"- MRR estimado: **${kpis.get('mrr_estimado_usd', 0):.2f} USD**",
        "",
        "## Email (Listmonk)",
        f"- Open rate: **{kpis.get('email_open_rate_pct', 0):.1f}%**",
        f"- CTR: **{kpis.get('email_ctr_pct', 0):.1f}%**",
        f"- Suscriptores totales: **{kpis.get('suscriptores_total', 0)}**",
        "",
        "## Tráfico (Umami)",
        f"- Visitas landing: **{kpis.get('visitas_landing', 0)}**",
        f"- Visitantes únicos: **{kpis.get('visitas_unicas', 0)}**",
    ]

    fuentes = kpis.get('fuentes_top', {})
    if fuentes:
        lines.append("- Top fuentes: " + ", ".join(f"{k} {v}%" for k, v in fuentes.items()))

    # SEO
    serp_top = kpis.get('serpbear_keywords_top3', {})
    lines += ["", "## SEO (SerpBear)"]
    if serp_top:
        lines.append(f"- Posición promedio: **{kpis.get('serpbear_posicion_avg', 0):.1f}** | Keywords subiendo: **{kpis.get('serpbear_subiendo', 0)}**")
        for kw, pos in serp_top.items():
            lines.append(f"- `{kw}`: posición **{pos}**")
    else:
        lines.append("- Sin datos (configura SERPBEAR_API_KEY o agrega keywords en SerpBear)")

    # RRSS
    lines += ["", "## RRSS"]
    lines += [
        f"- Tráfico desde Instagram: **{kpis.get('trafico_instagram', 0)}** visitas",
        f"- Tráfico desde TikTok: **{kpis.get('trafico_tiktok', 0)}** visitas",
        f"- Tráfico desde LinkedIn: **{kpis.get('trafico_linkedin', 0)}** visitas",
        f"- Posts publicados esta semana: **{kpis.get('posts_publicados_semana', 0)}**",
        f"- Seguidores Instagram: **{kpis.get('instagram_seguidores', 0)}**",
        f"- Seguidores TikTok: **{kpis.get('tiktok_seguidores', 0)}**",
        f"- Alcance Instagram: **{kpis.get('instagram_alcance', 0)}**",
    ]

    lines += [
        "",
        "## Alertas activas",
    ]
    if alertas:
        for a in alertas:
            lines.append(f"- `{a}`")
    else:
        lines.append("- Sin alertas")

    lines += [
        "",
        "## Decisión sugerida",
        decision,
    ]

    return "\n".join(lines)


def render_email_html(md_text: str, escenario: str) -> str:
    """Versión HTML mínima para el email TX de Listmonk."""
    color = {'verde': '#2d6a4f', 'amarillo': '#b5770d', 'rojo': '#9b2226'}.get(escenario, '#333')
    body = md_text.replace('\n', '<br>').replace('**', '<strong>').replace('**', '</strong>')
    return f"""<div style="font-family:sans-serif;max-width:600px;margin:auto;padding:24px;">
<div style="background:{color};color:white;padding:12px 20px;border-radius:8px;margin-bottom:20px;">
  <strong>Endonautas KPI — {escenario.upper()}</strong>
</div>
<pre style="white-space:pre-wrap;font-size:14px;line-height:1.6;">{md_text}</pre>
</div>"""
