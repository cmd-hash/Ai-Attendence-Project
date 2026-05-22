from src.database.config import supabase
import bcrypt


def hash_pass(pwd):
    return bcrypt.hashpw(
        pwd.encode(),
        bcrypt.gensalt()
    ).decode()


def check_pass(pwd, hashed):
    return bcrypt.checkpw(
        pwd.encode(),
        hashed.encode()
    )


def check_teacher_exist(username):

    response = (
        supabase
        .table("teachers")
        .select("username")
        .eq("username", username)
        .execute()
    )

    return len(response.data) > 0


def create_teacher(username, password, name):

    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name
    }

    response = (
        supabase
        .table("teachers")
        .insert(data)
        .execute()
    )

    return response.data


def teacher_login(username, password):

    response = (
        supabase
        .table("teachers")
        .select("*")
        .eq("username", username)
        .execute()
    )

    if response.data:

        teacher = response.data[0]

        if check_pass(password, teacher['password']):
            return teacher

    return None


def get_all_students():

    response = (
        supabase
        .table('students')
        .select("*")
        .execute()
    )

    return response.data


def create_student(
    new_name,
    face_embedding=None,
    voice_embedding=None
):

    data = {
        'name': new_name,
        'face_embedding': face_embedding,
        'voice_embedding': voice_embedding
    }

    response = (
        supabase
        .table('students')
        .insert(data)
        .execute()
    )

    print("SUPABASE RESPONSE:", response)

    return response.data


def create_subject(subject_code, name, section, teacher_id):

    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id
    }

    response = (
        supabase
        .table("subjects")
        .insert(data)
        .execute()
    )

    return response.data


def get_teacher_subjects(teacher_id):

    response = (
        supabase
        .table('subjects')
        .select("*, subject_students(student_id), attendance_logs(timestamp)")
        .eq("teacher_id", teacher_id)
        .execute()
    )

    subjects = response.data

    for sub in subjects:

        # Total students
        subject_students = sub.get("subject_students", [])
        sub['total_students'] = len(subject_students)

        # FIX: truncate timestamp to minute level (YYYY-MM-DDTHH:MM)
        # so logs from the same session are grouped correctly
        attendance_logs = sub.get('attendance_logs', [])
        unique_sessions = len(
            set(
                log['timestamp'][:16]
                for log in attendance_logs
            )
        )
        sub['total_classes'] = unique_sessions

        # Remove nested data
        sub.pop('subject_students', None)
        sub.pop('attendance_logs', None)

    return subjects


def enroll_student_to_subject(student_id, subject_id):

    data = {
        'student_id': student_id,
        'subject_id': subject_id
    }

    response = (
        supabase
        .table('subject_students')
        .insert(data)
        .execute()
    )

    return response.data


def unenroll_student_to_subject(student_id, subject_id):

    response = (
        supabase
        .table('subject_students')
        .delete()
        .eq('student_id', student_id)
        .eq('subject_id', subject_id)
        .execute()
    )

    return response.data


def get_student_subjects(student_id):

    response = (
        supabase
        .table('subject_students')
        .select('*, subjects(*)')
        .eq('student_id', student_id)
        .execute()
    )

    return response.data


def get_student_attendence(student_id):

    response = (
        supabase
        .table('attendance_logs')
        .select('*, subjects(*)')
        .eq('student_id', student_id)
        .execute()
    )

    return response.data


def create_attendence(logs):

    response = (
        supabase
        .table('attendance_logs')
        .insert(logs)
        .execute()
    )

    return response.data


def get_attendence_for_teacher(teacher_id):
    response = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data