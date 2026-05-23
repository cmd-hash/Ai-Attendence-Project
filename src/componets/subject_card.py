import streamlit as st


def subject_card(
    name,
    code,
    section,
    stats=None,
    footer_callback=None
):

    html = f"""
    <div style="

        background:
        linear-gradient(
            135deg,
            rgba(99,102,241,.18),
            rgba(139,92,246,.18)
        );

        backdrop-filter: blur(18px);

        border:1px solid rgba(255,255,255,.12);

        border-radius:24px;

        padding:24px;

        margin-bottom:20px;

        box-shadow:
        0 12px 30px rgba(0,0,0,.25);

    ">

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:15px;
        ">

            <h3 style="
                margin:0;
                color:white;
            ">
                📚 {name}
            </h3>

            <span style="
                background:#6366f1;
                color:white;
                padding:6px 12px;
                border-radius:999px;
                font-size:13px;
                font-weight:600;
            ">
                {code}
            </span>

        </div>

        <div style="
            color:#cbd5e1;
            margin-bottom:18px;
            font-size:15px;
        ">
            Section : <b>{section}</b>
        </div>
    """

    if stats:

        html += """
        <div style="
            display:flex;
            gap:10px;
            flex-wrap:wrap;
        ">
        """

        for icon, label, value in stats:

            html += f"""
            <div style="
                background:
                rgba(255,255,255,.08);

                padding:10px 16px;

                border-radius:14px;

                color:white;

                border:
                1px solid rgba(255,255,255,.08);

            ">
                {icon}
                <b>{value}</b>
                {label}
            </div>
            """

        html += "</div>"

    html += "</div>"

    st.markdown(
        html,
        unsafe_allow_html=True
    )

    if footer_callback:
        footer_callback()