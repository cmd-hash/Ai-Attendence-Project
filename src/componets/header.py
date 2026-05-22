import streamlit as st
import requests

def header_home():

    logo_url="https://cdn-icons-gif.flaticon.com/19035/19035057.gif"
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px;">
        <img src='{logo_url}'style='height:100px;' />
        <h1 style='text-align:center; color:#E0E3FF'> QUICK SNAP </h1>
        </div>


        """, unsafe_allow_html=True)
    








def header_dashboard():

    logo_url="https://cdn-icons-gif.flaticon.com/19035/19035057.gif"
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; gap:10px; margin-top:30px">
        <img src='{logo_url}'style='height:85px;' />
        <h2 style='text-align:center; color:#5865F2'> QUICK SNAP </h2>
        </div>


        """, unsafe_allow_html=True)