import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.componets.dialog_attendance_results import show_attendance_result


@st.dialog('Voice Attendance')
def voice_attendance_dialog(selected_subject_id):

    st.write(
        'Record classroom audio. Students should clearly say: "I am present"'
    )

    audio_data = st.audio_input("Record classroom audio")

    if st.button('Analyze Audio', width='stretch', type='primary'):

        if not audio_data:
            st.warning('Please record audio first!')
            return

        with st.spinner('Processing audio...'):

            enrolled_res = (
                supabase
                .table('subject_students')
                .select("*, students(*)")
                .eq('subject_id', selected_subject_id)
                .execute()
            )

            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning('No students enrolled!')
                return

            candidates_dict = {}

            for s in enrolled_students:
                student = s['students']
                if student.get('voice_embedding'):
                    candidates_dict[student['student_id']] = student['voice_embedding']

            if not candidates_dict:
                st.error('No enrolled students have voice embeddings!')
                return

            audio_bytes = audio_data.read()

            detected_score = process_bulk_audio(
                audio_bytes, candidates_dict, threshold=0.60
            )

            if detected_score is None:
                st.error('Voice processing failed!')
                return

            results = []
            attendance_to_log = []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node['students']
                student_id = student['student_id']
                score = detected_score.get(student_id)
                is_present = (score is not None and score >= 0.60)

                results.append({
                    "Name": student['name'],
                    "ID": student_id,
                    "Score": round(score, 3) if score else 0.0,
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })

                attendance_to_log.append({
                    'student_id': student_id,
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': is_present
                })

            st.session_state.voice_attendance_results = (
                pd.DataFrame(results), attendance_to_log
            )

        if st.session_state.get('voice_attendance_results'):
            st.divider()
            df_results, logs = st.session_state.voice_attendance_results
            show_attendance_result(df_results, logs)