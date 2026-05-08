import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.componets.header import header_dashboard

def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    header_dashboard()
    st.header("Teacher Screen")