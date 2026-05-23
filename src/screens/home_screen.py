import streamlit as st
from src.componets.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.componets.footer import footer_home


def home_screen():

    header_home()
    style_background_home()
    style_base_layout()

    st.markdown("""
    <style>
    /* Make columns bigger and more attractive */
    .stApp div[data-testid="stColumn"] {
        background: linear-gradient(145deg, rgba(88,101,242,0.25), rgba(255,255,255,0.07)) !important;
        padding: 2.5rem 2rem !important;
        border-radius: 2rem !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
        backdrop-filter: blur(10px) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
        min-height: 380px !important;
    }

    .stApp div[data-testid="stColumn"]:hover {
        transform: translateY(-6px) !important;
        box-shadow: 0 16px 48px rgba(88,101,242,0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Spacer
    st.markdown("<div style='margin-top: 20px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("<h2 style='font-size:2rem; margin-bottom:1rem;'>I'm Teacher</h2>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/128/3429/3429440.png", width=150)
        st.markdown("<p style='color:rgba(255,255,255,0.6); margin-bottom:1.5rem;'>Manage subjects, take AI attendance & view reports</p>", unsafe_allow_html=True)
        if st.button("Teacher Portal →", type='primary', width='stretch', key='teacher_btn'):
            st.session_state['login_type'] = "teacher"
            st.rerun()

    with col2:
        st.markdown("<h2 style='font-size:2rem; margin-bottom:1rem;'>I'm Student</h2>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/128/2995/2995657.png", width=150)
        st.markdown("<p style='color:rgba(255,255,255,0.6); margin-bottom:1.5rem;'>Enroll in subjects & track your attendance records</p>", unsafe_allow_html=True)
        if st.button("Student Portal →", type='primary', width='stretch', key='student_btn'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    footer_home()
