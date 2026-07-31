import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="Decision Tree - Heart Disease", page_icon="🌳", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #27ae60 0%, #2ecc71 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .result-box {
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    .safe-result {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
    }
    .risk-result {
        background: linear-gradient(135deg, #c0392b 0%, #e74c3c 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🌳 Decision Tree - ทำนายโรคหัวใจ</p>', unsafe_allow_html=True)
st.markdown("### วิเคราะห์ความเสี่ยงโรคหัวใจด้วย Decision Tree Classifier")
st.markdown("---")

# โหลดโมเดล
@st.cache_resource
def load_model():
    model_path = "models/decision_tree_model.pkl"
    encoders_path = "models/label_encoders.pkl"
    features_path = "models/decision_tree_features.pkl"
    
    if not os.path.exists(model_path):
        return None, None, None
    
    model = joblib.load(model_path)
    label_encoders = joblib.load(encoders_path)
    features = joblib.load(features_path)
    return model, label_encoders, features

model, label_encoders, features = load_model()

if model is None:
    st.error("❌ ไม่พบไฟล์โมเดล! โปรดตรวจสอบโฟลเดอร์ models/")
    st.stop()

# Sidebar - ฟอร์มกรอกข้อมูล
st.sidebar.header("📝 กรอกข้อมูลสุขภาพ")
st.sidebar.markdown("---")

with st.sidebar.form("input_form"):
    st.subheader(" ข้อมูลส่วนตัว")
    age = st.number_input("อายุ (ปี)", min_value=20, max_value=100, value=55, step=1)
    sex = st.selectbox("เพศ", ["ชาย (Male)", "หญิง (Female)"])
    
    st.subheader(" อาการเจ็บหน้าอก")
    chest_pain_type = st.selectbox("ประเภทอาการเจ็บหน้าอก", 
                                    ["Typical Angina", "Atypical Angina", 
                                     "Non-Anginal Pain", "Asymptomatic"])
    
    st.subheader("🩺 ค่าสุขภาพ")
    resting_bp = st.number_input("ความดันโลหิตขณะพัก (mm Hg)", 
                                  min_value=80, max_value=250, value=130, step=5)
    cholesterol = st.number_input("ระดับคอเลสเตอรอล (mg/dl)", 
                                   min_value=100, max_value=600, value=250, step=10)
    fasting_bs = st.selectbox("น้ำตาลในเลือดขณะอดอาหาร > 120 mg/dl", 
                               ["ไม่ใช่ (No)", "ใช่ (Yes)"])
    max_hr = st.number_input("อัตราการเต้นหัวใจสูงสุด", 
                              min_value=60, max_value=220, value=150, step=5)
    oldpeak = st.number_input("ST Depression (Oldpeak)", 
                               min_value=0.0, max_value=7.0, value=1.0, step=0.1)
    
    st.subheader("📊 ผลตรวจ ECG")
    resting_ecg = st.selectbox("ผล ECG ขณะพัก", 
                                ["Normal", "ST-T Wave Abnormality", 
                                 "Left Ventricular Hypertrophy"])
    st_slope = st.selectbox("ความชันของ ST Segment", 
                             ["Upsloping", "Flat", "Downsloping"])
    
    st.subheader("🏃 การออกกำลังกาย")
    exercise_angina = st.selectbox("เจ็บหน้าอกเมื่อออกกำลังกาย", 
                                    ["ไม่ใช่ (No)", "ใช่ (Yes)"])
    
    submitted = st.form_submit_button("🔮 วิเคราะห์ความเสี่ยง", 
                                       use_container_width=True, type="primary")

# พื้นที่แสดงผลหลัก
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 ผลการวิเคราะห์")
    
    if submitted:
        # แปลงข้อมูลให้ตรงกับโมเดล
        sex_val = 1 if sex == "ชาย (Male)" else 0
        fasting_bs_val = 1 if fasting_bs == "ใช่ (Yes)" else 0
        exercise_angina_val = 1 if exercise_angina == "ใช่ (Yes)" else 0
        
        # Encode categorical variables
        chest_pain_encoded = label_encoders['ChestPainType'].transform([chest_pain_type])[0]
        resting_ecg_encoded = label_encoders['RestingECG'].transform([resting_ecg])[0]
        st_slope_encoded = label_encoders['ST_Slope'].transform([st_slope])[0]
        
        input_data = pd.DataFrame({
            'Age': [age],
            'Sex': [sex_val],
            'ChestPainType': [chest_pain_encoded],
            'RestingBP': [resting_bp],
            'Cholesterol': [cholesterol],
            'FastingBS': [fasting_bs_val],
            'RestingECG': [resting_ecg_encoded],
            'MaxHR': [max_hr],
            'ExerciseAngina': [exercise_angina_val],
            'Oldpeak': [oldpeak],
            'ST_Slope': [st_slope_encoded]
        })
        
        # ทำนายผล
        prediction = model.predict(input_data[features])[0]
        probability = model.predict_proba(input_data[features])[0]
        
        # แสดงผลลัพธ์
        if prediction == 0:
            st.markdown("""
            <div class="result-box safe-result">
                <h2>✅ ไม่พบความเสี่ยงโรคหัวใจ</h2>
                <p>ผลลัพธ์: No Heart Disease</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown("""
            <div class="result-box risk-result">
                <h2>⚠️ พบความเสี่ยงโรคหัวใจ</h2>
                <p>ผลลัพธ์: Has Heart Disease</p>
            </div>
            """, unsafe_allow_html=True)
        
        # แสดงความน่าจะเป็น
        st.subheader("📈 ความน่าจะเป็น")
        col_safe, col_risk = st.columns(2)
        with col_safe:
            st.metric("✅ ไม่เป็นโรค", f"{probability[0]*100:.2f}%")
        with col_risk:
            st.metric("⚠️ เป็นโรค", f"{probability[1]*100:.2f}%")
        
        # คำแนะนำ
        st.subheader("💡 คำแนะนำด้านสุขภาพ")
        if prediction == 1:
            st.warning("**ผลการวิเคราะห์:** คุณมีความเสี่ยงต่อโรคหัวใจ")
            st.markdown("""
            ###  แนวทางลดความเสี่ยง:
            
            1. 🏃 **ออกกำลังกายสม่ำเสมอ** 
               - อย่างน้อย 150 นาที/สัปดาห์ (เดินเร็ว, วิ่ง, ว่ายน้ำ)
            
            2. 🥗 **ควบคุมอาหาร**
               - ลดไขมันอิ่มตัว, โซเดียม, น้ำตาล
               - เพิ่มผัก, ผลไม้, ธัญพืชไม่ขัดสี
            
            3.  **เลิกสูบบุหรี่**
               - บุหรี่เพิ่มความเสี่ยงโรคหัวใจ 2-4 เท่า
            
            4. 🍷 **จำกัดแอลกอฮอล์**
               - ไม่เกิน 1-2 แก้ว/วัน
            
            5.  **จัดการความเครียด**
               - โยคะ, สมาธิ, นอนหลับให้เพียงพอ
            
            6. 🩺 **พบแพทย์เป็นประจำ**
               - ตรวจสุขภาพประจำปี, ติดตามความดันและคอเลสเตอรอล
            """)
        else:
            st.success("**ผลการวิเคราะห์:** คุณไม่มีความเสี่ยงโรคหัวใจในขณะนี้")
            st.markdown("""
            ### 🎉 รักษามาตรฐานสุขภาพ:
            
            - 📅 **ตรวจสุขภาพประจำปี** - เพื่อติดตามค่าสุขภาพ
            -  **ออกกำลังกายต่อเนื่อง** - รักษานิสัยที่ดี
            - 🥗 **อาหารสมดุล** - รักษาโภชนาการที่ดี
            - 😊 **สุขภาพจิตดี** - จัดการความเครียดอย่างเหมาะสม
            """)

with col2:
    st.subheader(" ข้อมูลที่คุณกรอก")
    if submitted:
        summary_df = pd.DataFrame({
            'รายการ': [
                'อายุ', 'เพศ', 'ประเภทเจ็บหน้าอก', 
                'ความดันโลหิต', 'คอเลสเตอรอล', 'น้ำตาล>120',
                'ECG', 'หัวใจสูงสุด', 'เจ็บอกเมื่อออกกำลังกาย',
                'ST Depression', 'ST Slope'
            ],
            'ค่า': [
                age, sex, chest_pain_type,
                f"{resting_bp} mmHg", f"{cholesterol} mg/dl", fasting_bs,
                resting_ecg, max_hr, exercise_angina,
                oldpeak, st_slope
            ]
        })
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("ℹ️ เกี่ยวกับโมเดล")
    st.markdown("""
    **อัลกอริทึม:** Decision Tree Classifier  
    **งาน:** Binary Classification  
    **เป้าหมาย:** Heart Disease Prediction  
    **จำนวนฟีเจอร์:** 11 ตัวแปร  
    **ชุดข้อมูล:** Heart Disease (918 ระเบียน)
    
    **ข้อดีของ Decision Tree:**
    - ตีความผลได้ง่าย
    - แสดงเป็นกฎ (rules) ที่เข้าใจได้
    - ไม่ต้อง scale ข้อมูล
    """)
    
    st.subheader("📊 เกณฑ์การประเมิน")
    st.markdown("""
    | ค่า | ความหมาย |
    |-----|---------|
    | 0 | ไม่เป็นโรคหัวใจ |
    | 1 | เป็นโรคหัวใจ |
    """)

# Footer
st.markdown("---")
st.markdown("*พัฒนาด้วย ❤️ โดยระบบ Machine Learning เพื่อสุขภาพหัวใจที่ดี*")