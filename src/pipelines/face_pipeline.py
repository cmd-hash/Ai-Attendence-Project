import dlib
import cv2
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students



# LOAD DLIB MODELS


@st.cache_resource
def load_dlib_models():

    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec



# GENERATE FACE EMBEDDINGS


def get_face_embeddings(image_np):

    detector, sp, facerec = load_dlib_models()

    #  IMAGE FORMAT FIX 
    image_np = np.array(image_np)

    # RGBA -> RGB
    if len(image_np.shape) == 3 and image_np.shape[2] == 4:
        image_np = image_np[:, :, :3]

    # Ensure proper datatype
    image_np = image_np.astype(np.uint8)

    #RESIZE LARGE IMAGE 
    height, width = image_np.shape[:2]

    max_width = 640

    if width > max_width:

        scale = max_width / width

        new_width = int(width * scale)
        new_height = int(height * scale)

        image_np = cv2.resize(
            image_np,
            (new_width, new_height)
        )

    print("IMAGE SHAPE:", image_np.shape)
    print("IMAGE DTYPE:", image_np.dtype)

    #  FACE DETECTION 
    print("Starting face detection...")

    faces = detector(image_np, 1)

    print("Face detection completed")
    print("FACES DETECTED:", len(faces))

    encodings = []

    for i, face in enumerate(faces):

        print(f"Processing face {i+1}")

        shape = sp(image_np, face)

        face_descriptor = facerec.compute_face_descriptor(
            image_np,
            shape,
            1
        )

        encodings.append(np.array(face_descriptor))

    print("Encoding generation completed")

    return encodings



# TRAIN MODEL


@st.cache_resource
def get_trained_model():

    X = []
    y = []

    student_db = get_all_students()

    print("DATABASE DATA:", student_db)

    if not student_db:
        return None

    for student in student_db:

        embedding = student.get('face_embedding')

        if embedding:

            X.append(np.array(embedding))

            y.append(student.get('student_id'))

    print("TOTAL TRAINING SAMPLES:", len(X))

    if len(X) == 0:
        return None

    #  UNIQUE STUDENTS 
    unique_students = list(set(y))

    print("UNIQUE STUDENTS:", unique_students)

    #  SINGLE STUDENT 
    if len(unique_students) < 2:

        print("Only one student found. Skipping SVM training.")

        return {
            'clf': None,
            'X': X,
            'y': y
        }

    #  MULTIPLE STUDENTS 
    clf = SVC(
        kernel='linear',
        probability=True,
        class_weight='balanced'
    )

    try:

        print("Training classifier...")

        clf.fit(X, y)

        print("Training completed")

    except ValueError as e:

        st.error(f"Training Error: {e}")

        return None

    return {
        'clf': clf,
        'X': X,
        'y': y
    }



# RETRAIN MODEL


def train_classifier():

    st.cache_resource.clear()

    model_data = get_trained_model()

    return bool(model_data)



# PREDICT ATTENDANCE


def predict_attendance(class_image_np):

    print("Starting attendance prediction...")

    encodings = get_face_embeddings(class_image_np)

    detected_student = {}

    model_data = get_trained_model()

    if not model_data:

        print("No trained model found")

        return detected_student, [], len(encodings)

    clf = model_data.get('clf')

    X_train = model_data['X']

    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    print("ALL STUDENTS:", all_students)

    for encoding in encodings:

        #  MULTIPLE STUDENTS 
        if len(all_students) >= 2 and clf is not None:

            predicted_id = int(
                clf.predict([encoding])[0]
            )

        #  SINGLE STUDENT 
        else:

            predicted_id = int(all_students[0])

        print("PREDICTED ID:", predicted_id)

        student_embedding = X_train[
            y_train.index(predicted_id)
        ]

        #  DISTANCE SCORE 
        best_match_score = np.linalg.norm(
            student_embedding - encoding
        )

        print("MATCH SCORE:", best_match_score)

        resemblance_threshold = 0.85

        if best_match_score <= resemblance_threshold:

            detected_student[predicted_id] = True

            print("MATCH FOUND")

        else:

            print("NO MATCH")

    print("Attendance prediction completed")

    return detected_student, all_students, len(encodings)