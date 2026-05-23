import streamlit as st
import numpy as np
from PIL import Image
import time

from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.componets.header import header_dashboard
from src.componets.footer import footer_dashboard
from src.componets.dialog_enroll import enroll_dialog
from src.componets.subject_card import subject_card

from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier
)

from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject
)

from src.pipelines.voice_pipeline import get_voice_embedding


def student_dashboard():

    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2 = st.columns(
        2,
        vertical_alignment='center',
        gap='xxlarge'
    )

    with c1:
        header_dashboard()

    with c2:

        st.subheader(
            f"Welcome, {student_data['name']}"
        )

        if st.button(
            "Logout",
            type='primary',
            key='logoutBtn',
            shortcut="control+backspace"
        ):

            del st.session_state.student_data
            st.rerun()

    st.space()

    c1, c2 = st.columns(2)

    with c1:
        st.header('Your Enroll Subjects')

    with c2:
        if st.button(
            "Enroll in Subject",
            type='primary',
            width='stretch'
        ):
            enroll_dialog()

    st.divider()

    with st.spinner('Loading Your Enroll Subjects.....'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)

    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(sid, {"total": 0, "attended": 0})

        def unenroll_button(student_id=student_id, sid=sid):
            if st.button(
                "Unenroll From This Course..",
                key=f"unenroll_{sid}",
                type='tertiary',
                width='stretch',
                icon=':material/delete_forever:'):

                unenroll_student_to_subject(student_id, sid)
                st.toast(f"Unenrolled From This {sub['name']} Successfully!")
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )

    footer_dashboard()


def student_screen():

    style_background_dashboard()
    style_base_layout()

    # ---------- LOGIN CHECK ----------

    if "student_data" in st.session_state:
        student_dashboard()
        return

    # ---------- HEADER ----------

    c1, c2 = st.columns(
        2,
        vertical_alignment='center',
        gap='xxlarge'
    )

    with c1:
        header_dashboard()

    with c2:

        if st.button(
            "Go back to Home",
            type='secondary',
            key='loginbackbtn',
            shortcut="control+backspace"
        ):

            st.session_state['login_type'] = None
            st.rerun()

    # ---------- FACE LOGIN ----------

    st.header(
        'Login using FaceID',
        text_alignment='center'
    )

    st.space()
    st.space()

    show_registeration = False

    photo_source = st.camera_input(
        "Position your face in the center"
    )

    if photo_source:

        img = np.array(Image.open(photo_source))

        with st.spinner('AI is Scanning...'):

            detected, all_ids, num_faces = predict_attendance(img)

            # ---------- FACE CHECK ----------

            if num_faces == 0:

                st.warning('Face not Found!')

            elif num_faces > 1:

                st.warning('Multiple Faces Found!')

            else:

                # ---------- FACE RECOGNIZED ----------

                if detected:

                    student_id = list(detected.keys())[0]

                    all_students = get_all_students()

                    student = next(
                        (
                            s for s in all_students
                            if s['student_id'] == student_id
                        ),
                        None
                    )

                    if student:

                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student

                        st.toast(
                            f"Welcome Back! {student['name']}"
                        )

                        time.sleep(1)

                        st.rerun()

                # ---------- NEW STUDENT ----------

                else:

                    st.info(
                        "Face Not Recognized! "
                        "You Might Be A New Student!"
                    )

                    show_registeration = True

    # ---------- REGISTRATION ----------

    if show_registeration:

        with st.container(border=True):

            st.header('Register New Profile')

            new_name = st.text_input(
                'Enter Your Name',
                placeholder='E.g. Dewansh'
            )

            st.subheader('Optional : Voice Enrollment')

            st.info(
                "Enroll for voice-based attendance"
            )

            audio_data = None

            # ---------- AUDIO INPUT ----------

            try:

                audio_data = st.audio_input(
                    'Record a short phrase like: '
                    '"I am present, my name is Dewansh"'
                )

            except Exception:

                st.warning(
                    "Audio recording is not supported "
                    "on this device/browser"
                )

            # ---------- CREATE ACCOUNT ----------

            if st.button(
                'Create Account',
                type='primary'
            ):

                if new_name:

                    with st.spinner('Creating Profile...'):

                        img = np.array(
                            Image.open(photo_source)
                        )

                        encodings = get_face_embeddings(img)

                        if encodings:

                            face_emb = encodings[0].tolist()

                            voice_emb = None

                            if audio_data:

                                voice_emb = get_voice_embedding(
                                    audio_data.read()
                                )

                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb
                            )

                            if response_data:

                                train_classifier()

                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'

                                st.session_state.student_data = (
                                    response_data[0]
                                )

                                st.toast(
                                    f'Profile Created! '
                                    f'Hi {new_name}'
                                )

                                time.sleep(1)

                                st.rerun()

                            else:

                                st.error(
                                    'Could Not Capture '
                                    'Your Facial Features '
                                    'for Registration'
                                )

                        else:

                            st.error(
                                'No face encoding generated!'
                            )

                else:

                    st.warning(
                        'Please Enter Your Name!'
                    )

    # ---------- FOOTER ----------

    footer_dashboard()