import streamlit as st
from src.componets.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.componets.footer import footer_home

def home_screen():
    
   

    header_home()
    style_background_home()
    style_base_layout()




    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm Teacher")
        st.image("https://cdn-icons-png.flaticon.com/128/3429/3429440.png", width=120 )
        if st.button("Teacher Portal ", type='primary',  icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type']="teacher"
            st.rerun()

    with col2:
        st.header("I'm Student")
        st.image("https://cdn-icons-png.flaticon.com/128/2995/2995657.png", width=120 )
        if st.button("Student Portal", type='primary', icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type']='student'

            st.rerun()
        
           

    footer_home()