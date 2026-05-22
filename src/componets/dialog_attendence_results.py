import streamlit as st
from src.database.db import create_attendence


def show_attendence_result(df, logs):

    st.write('Please Review Attendance Before Confirming...')
    st.dataframe(df, hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Discard', width='stretch'):
            st.session_state.voice_attendence_results = None
            st.session_state.attendence_images = []
            st.rerun()

    # FIX: col2 was indented inside col1, moved it outside
    with col2:
        if st.button('Confirm & Save', width='stretch', type='primary'):
            try:
                create_attendence(logs)
                st.toast('Attendance Saved!')
                st.session_state.attendence_images = []
                st.session_state.voice_attendence_results = None
                st.rerun()
            except Exception as e:
                st.error(f'Sync Failed! {e}')


@st.dialog("Attendance Reports..")
def attendence_result_dialog(df, logs):
    show_attendence_result(df, logs)