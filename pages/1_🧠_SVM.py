import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="SVM Prediction", page_icon="🧠", layout="wide")

st.markdown("# 🧠 SVM - Sleep Quality Prediction")
st.markdown("### ทำนายคุณภาพการนอนหลับด้วย Support Vector Machine")
st.markdown("---")

# Load Model
@st.cache_resource
def load_model():
    model_path = "models/svm_model.pkl"
    scaler_path = "models/svm_scaler.pkl"
    features_path = "models/svm_features.pkl"
    
    if not os.path.exists(model_path):
        return None, None, None
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    features = joblib.load(features_path)
    return model, scaler, features

model, scaler, features = load_model()

if model is None:
    st.error("❌ ไม่พบไฟล์โมเดล! โปรดอัปโหลดไฟล์ `svm_model.pkl`, `svm_scaler.pkl`, `svm_features.pkl` ในโฟลเดอร์ `models/`")
    st.stop()

# Sidebar - Input Form
st.sidebar.header("📝 กรอกข้อมูลการนอนหลับ")

with st.sidebar.form("input_form"):
    st.subheader("👤 ข้อมูลส่วนตัว")
    age = st.number_input("อายุ (ปี)", min_value=5, max_value=100, value=35, step=1)
    gender = st.selectbox("เพศ", ["Male", "Female"])
    
    st.subheader("💤 ข้อมูลการนอน")
    sleep_duration = st.number_input("ระยะเวลาการนอน (ชั่วโมง)", min_value=3.0, max_value=12.0, value=7.5, step=0.5)
    rem_sleep = st.slider("REM Sleep (%)", 0, 50, 20)
    deep_sleep = st.slider("Deep Sleep (%)", 0, 100, 55)
    light_sleep = st.slider("Light Sleep (%)", 0, 100, 25)
    awakenings = st.number_input("จำนวนครั้งที่ตื่นกลางคืน", min_value=0, max_value=10, value=1)
    
    st.subheader("🕐 เวลา")
    bedtime_hour = st.slider("เวลาเข้านอน (ชั่วโมง)", 0, 23, 23)
    wakeup_hour = st.slider("เวลาตื่นนอน (ชั่วโมง)", 0, 23, 7)
    
    st.subheader("🧬 ไลฟ์สไตล์")
    caffeine = st.number_input("ปริมาณคาเฟอีน (mg)", min_value=0, max_value=500, value=0, step=25)
    alcohol = st.number_input("ปริมาณแอลกอฮอล์ (หน่วย)", min_value=0.0, max_value=10.0, value=0.0, step=0.5)
    smoking = st.selectbox("สูบบุหรี่", ["No", "Yes"])
    exercise = st.selectbox("ความถี่ในการออกกำลังกาย (ครั้ง/สัปดาห์)", 
                           [0, 1, 2, 3, 4, 5])
    
    submitted = st.form_submit_button("🔮 ทำนายผล", use_container_width=True)

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 ผลการทำนาย")
    
    if submitted:
        # Prepare input
        input_data = pd.DataFrame({
            'Age': [age],
            'Gender': [0 if gender == "Male" else 1],
            'Sleep duration': [sleep_duration],
            'REM sleep percentage': [rem_sleep],
            'Deep sleep percentage': [deep_sleep],
            'Light sleep percentage': [light_sleep],
            'Awakenings': [awakenings],
            'Caffeine consumption': [caffeine],
            'Alcohol consumption': [alcohol],
            'Smoking status': [0 if smoking == "No" else 1],
            'Exercise frequency': [exercise],
            'Bedtime_hour': [bedtime_hour],
            'Wakeup_hour': [wakeup_hour]
        })
        
        # Scale and predict
        input_scaled = scaler.transform(input_data[features])
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0]
        
        # Display result
        if prediction == 1:
            st.success("## ✅ คุณภาพการนอนหลับ: ดี (Good)")
            st.markdown(f"**ความมั่นใจ:** {probability[1]*100:.2f}%")
            st.balloons()
        else:
            st.warning("## ⚠️ คุณภาพการนอนหลับ: ต้องปรับปรุง (Poor)")
            st.markdown(f"**ความมั่นใจ:** {probability[0]*100:.2f}%")
        
        # Probability visualization
        st.subheader("📈 ความน่าจะเป็นของแต่ละคลาส")
        prob_df = pd.DataFrame({
            'Class': ['Poor (<0.80)', 'Good (>=0.80)'],
            'Probability': [probability[0]*100, probability[1]*100]
        })
        st.bar_chart(prob_df.set_index('Class'))
        
        # Recommendations
        st.subheader("💡 คำแนะนำ")
        if prediction == 0:
            st.markdown("""
            - 🛌 **นอนให้เป็นเวลา** - เข้านอนและตื่นเวลาเดิมทุกวัน
            - ☕ **ลดคาเฟอีน** - หลีกเลี่ยงกาแฟ/ชา หลังบ่าย 2 โมง
            - 📱 **ลดหน้าจอ** - หลีกเลี่ยงโทรศัพท์ก่อนนอน 1 ชั่วโมง
            - 🏃 **ออกกำลังกาย** - แต่อย่าออกกำลังกายหนักก่อนนอน
            - 🍷 **ลดแอลกอฮอล์** - แอลกอฮอล์รบกวนช่วง REM sleep
            """)
        else:
            st.markdown("""
            - 🎉 **ยอดเยี่ยม!** คุณมีคุณภาพการนอนหลับที่ดี
            - 📅 **รักษาไว้** - ทำตามกิจวัตรการนอนปัจจุบันต่อไป
            - 💪 **พัฒนาต่อ** - เพิ่มการออกกำลังกายเพื่อคุณภาพที่ดีขึ้น
            """)

with col2:
    st.subheader("📋 ข้อมูลที่กรอก")
    if submitted:
        st.dataframe(input_data.T.rename(columns={0: 'Value'}))
    
    st.subheader("ℹ️ เกี่ยวกับโมเดล")
    st.markdown("""
    **Algorithm:** Support Vector Machine (SVM)  
    **Kernel:** RBF (Radial Basis Function)  
    **Task:** Binary Classification  
    **Target:** Sleep Efficiency ≥ 0.80 = Good
    
    **Features:** 13 features  
    **Dataset:** Sleep Efficiency (452 records)
    """)

# Footer
st.markdown("---")
st.markdown("*พัฒนาด้วย ❤️ โดย Machine Learning Pipeline*")