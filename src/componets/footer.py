import streamlit as st
import requests

def footer_home():

    logo_url = "https://cdn-icons-png.flaticon.com/128/5611/5611037.png"

    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content: center; items-align: center">
        <p style="font-weight:bold; color:white;"> Powered By  </p>
        <img src='{logo_url}' style=max-height:25px  width:25px object-fit:contain; />
        </div>

        
        """, unsafe_allow_html=True)
    

def footer_dashboard():

    logo_url = "https://cdn-icons-png.flaticon.com/128/5611/5611037.png"

    st.markdown(f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content: center; items-align: center">
        <p style="font-weight:bold; color:black;"> Powered By  </p>
        <img src='{logo_url}' style=max-height:25px  width:25px object-fit:contain; />
        </div>

        
        """, unsafe_allow_html=True)