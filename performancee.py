import streamlit as st
import pandas as pd
import pickle
import sklearn.compose._column_transformer  # 👈 this is the exact module pickle is complaining about

# 🔧 Compatibility patch for old scikit-learn pickled models
if not hasattr(sklearn.compose._column_transformer, "_RemainderColsList"):
    class _RemainderColsList(list):
        """Placeholder for backward compatibility with old sklearn models."""
        pass
    sklearn.compose._column_transformer._RemainderColsList = _RemainderColsList

# ✅ Now load your model safely
with open("performance.pkl", "rb") as f:
    model = pickle.load(f)




# Set page configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="centered"
)

# Custom CSS for dark mode
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #0c0c0c;
        color: #ffffff;
    }
    .main-card {
        background: #1e1e1e;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0,255,255,0.05);
        margin-top: 2rem;
    }
    .title {
        font-size: 38px;
        font-weight: bold;
        color: #00ffff;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub {
        font-size: 17px;
        color: #c2c2c2;
        text-align: center;
        margin-bottom: 2rem;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        margin-top: 3rem;
        color: #888;
    }
    .stSlider > div[data-baseweb="slider"] > div {
        background: #00ffff33 !important;
    }
    .stSelectbox > div[data-baseweb="select"] {
        background: #2a2a2a;
        color: white;
    }
    .stButton>button {
        background-color: #00ffff;
        color: #000000;
        font-weight: bold;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #00cccc;
    }
    </style>
""", unsafe_allow_html=True)

# Logo and Titles
st.image("https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=80)
st.markdown('<div class="title">Student Performance Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Analyze lifestyle and habits to predict academic performance</div>', unsafe_allow_html=True)

# Form container with card style
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    with st.form("prediction_form"):
        st.markdown("### 📋 Student Information Form")

        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input('Age', 10, 60, 20)
            study_hours_per_day = st.slider('Study Hours per Day', 0.0, 18.0, 5.0)
            social_media_hours = st.slider('Social Media Hours', 0.0, 12.0, 1.0)
            netflix_hours = st.slider('Netflix Hours', 0.0, 12.0, 1.0)
            attendance_percentage = st.slider('Attendance Rate (%)', 0.0, 100.0, 60.0)
            sleep_hours = st.slider('Sleep Hours per Day', 1.0, 24.0, 8.0)

        with col2:
            exercise_frequency = st.slider('Exercise Days/Week', 1, 7, 2)
            mental_health_rating = st.slider('Mental Health Rating (1-10)', 1, 10, 5)
            gender = st.selectbox('Gender', ['Male', 'Female'])
            part_time_job = st.selectbox('Part-time Job?', ['Yes', 'No'])
            diet_quality = st.selectbox('Diet Quality', ['Fair', 'Good', 'Poor'])
            internet_quality = st.selectbox('Internet Quality', ['Average', 'Poor', 'Good'])
            extracurricular_participation = st.selectbox('Extracurricular Activities?', ['Yes', 'No'])
            parental_education_level = st.selectbox('Parent Education Level', ['Master', 'Bachelor', 'High School', 'None'])

        submitted = st.form_submit_button("🎯 Predict Performance")

    st.markdown('</div>', unsafe_allow_html=True)

# Prediction handling
if submitted:
    input_data = {
        'age': [age],
        'study_hours_per_day': [study_hours_per_day],
        'social_media_hours': [social_media_hours],
        'netflix_hours': [netflix_hours],
        'attendance_percentage': [attendance_percentage],
        'sleep_hours': [sleep_hours],
        'exercise_frequency': [exercise_frequency],
        'mental_health_rating': [mental_health_rating],
        'gender': [gender],
        'part_time_job': [part_time_job],
        'diet_quality': [diet_quality],
        'internet_quality': [internet_quality],
        'extracurricular_participation': [extracurricular_participation],
        'parental_education_level': [parental_education_level]
    }

    df = pd.DataFrame(input_data)
    prediction = model.predict(df)[0]

    st.success(f"🎓 Predicted Academic Performance: **{prediction}**")

# Footer
st.markdown('<div class="footer">© 2025 Student Insight Tool | Designed by Tobi Seun Animasahun</div>', unsafe_allow_html=True)
