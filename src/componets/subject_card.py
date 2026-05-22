import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div style="background:#1e1b4b; border-left: 8px solid #EB459E; padding:25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom:20px;">
        <h3 style="margin:0; font-size: 1.5rem; color:white;">{name}</h3>
        <p style="margin:10px 0; color:rgba(255,255,255,0.7);">Code : <span style="background:#5865F2; color:white; padding:2px 8px; border-radius:5px;">{code}</span> &nbsp;| Section : <span style="color:rgba(255,255,255,0.7);">{section}</span></p>
        """

    if stats:
        html += '<div style="display:flex; gap:8px; flex-wrap:wrap;">'
        for icon, label, value in stats:
            html += (
                f'<div style="background:rgba(235,69,158,0.15); padding:5px 12px; border-radius:12px;'
                f' font-size:0.9rem; color:white;">'
                f'{icon} <b>{value}</b> {label}</div>'
            )
        html += "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()