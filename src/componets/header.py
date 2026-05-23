import streamlit as st


def header_home():

    logo_url = "https://cdn-icons-gif.flaticon.com/19035/19035057.gif"
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:10px; padding-top:20px;">
            <div style="
                width:110px; height:110px;
                border-radius:50%;
                background: linear-gradient(135deg, #5865F2, #EB459E);
                display:flex; align-items:center; justify-content:center;
                box-shadow: 0 8px 32px rgba(88,101,242,0.5);
                margin-bottom:16px;
                padding: 8px;
            ">
                <img src='{logo_url}' style='height:90px; width:90px; border-radius:50%; object-fit:cover;' />
            </div>
            <h1 style='text-align:center; color:#E0E3FF; letter-spacing:4px;'>QUICK SNAP</h1>
            <p style='color:rgba(255,255,255,0.5); font-size:1rem; margin-top:-10px; letter-spacing:2px;'>AI POWERED ATTENDANCE</p>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():

    logo_url = "https://cdn-icons-gif.flaticon.com/19035/19035057.gif"
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; gap:10px; margin-top:30px">
            <div style="
                width:70px; height:70px;
                border-radius:50%;
                background: linear-gradient(135deg, #5865F2, #EB459E);
                display:flex; align-items:center; justify-content:center;
                box-shadow: 0 4px 16px rgba(88,101,242,0.4);
                padding: 5px;
            ">
                <img src='{logo_url}' style='height:58px; width:58px; border-radius:50%; object-fit:cover;' />
            </div>
            <h2 style='text-align:center; color:#5865F2;'>QUICK SNAP</h2>
        </div>
    """, unsafe_allow_html=True)