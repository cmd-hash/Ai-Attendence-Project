import streamlit as st


def subject_card(
    name,
    code,
    section,
    stats=None,
    footer_callback=None
):
    stats_html = ""
    if stats:
        stats_html = '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;">'
        for icon, label, value in stats:
            stats_html += f'<div style="background:rgba(255,255,255,.08);padding:10px 16px;border-radius:14px;color:white;border:1px solid rgba(255,255,255,.1);font-size:14px;">{icon} <b>{value}</b> {label}</div>'
        stats_html += '</div>'

    html = f"""
    <div style="background:linear-gradient(135deg,rgba(99,102,241,.18),rgba(139,92,246,.18));backdrop-filter:blur(18px);border:1px solid rgba(255,255,255,.12);border-radius:24px;padding:24px;margin-bottom:8px;box-shadow:0 12px 30px rgba(0,0,0,.25);">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
            <h3 style="margin:0;color:white;font-size:18px;line-height:1.4;flex:1;padding-right:10px;">📚 {name}</h3>
            <span style="background:#6366f1;color:white;padding:6px 12px;border-radius:999px;font-size:13px;font-weight:600;white-space:nowrap;flex-shrink:0;">{code}</span>
        </div>
        <div style="color:#cbd5e1;margin-bottom:14px;font-size:15px;">Section : <b style="color:white;">{section}</b></div>
        {stats_html}
    </div>
    """

    st.html(html)

    if footer_callback:
        footer_callback()