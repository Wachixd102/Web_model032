import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="การทำนายด้วย SVM", page_icon="🧠", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
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
    .good-result {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    .poor-result {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🧠 การทำนายคุณภาพการนอนหลับด้วย SVM</p>', unsafe_allow_html=True)
st.markdown("###  Support Vector Machine (เครื่องเวกเตอร์ค้ำยัน)")
st.markdown("---")

# โหลดโมเดล
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
    st.error("❌ ไม่พบไฟล์โมเดล! โปรดตรวจสอบโฟลเดอร์ models/")
    st.stop()

# Sidebar - ฟอร์มกรอกข้อมูล
st.sidebar.header("📝 กรอกข้อมูลการนอนหลับ")
st.sidebar.markdown("---")

with st.sidebar.form("input_form"):
    st.subheader("👤 ข้อมูลส่วนตัว")
    age = st.number_input("อายุ (ปี)", min_value=5, max_value=100, value=35, step=1, 
                          help="กรอกอายุของคุณเป็นปี")
    gender = st.selectbox("เพศ", ["ชาย (Male)", "หญิง (Female)"])
    
    st.subheader("💤 ข้อมูลการนอน")
    sleep_duration = st.number_input("ระยะเวลาการนอน (ชั่วโมง)", 
                                      min_value=3.0, max_value=12.0, value=7.5, step=0.5)
    rem_sleep = st.slider("สัดส่วนการนอนช่วง REM (%)", 0, 50, 20, 
                          help="ปกติควรอยู่ที่ 20-25%")
    deep_sleep = st.slider("สัดส่วนการนอนหลับลึก (%)", 0, 100, 55,
                           help="ปกติควรอยู่ที่ 13-23%")
    light_sleep = st.slider("สัดส่วนการนอนหลับตื้น (%)", 0, 100, 25,
                            help="ปกติควรอยู่ที่ 40-50%")
    awakenings = st.number_input("จำนวนครั้งที่ตื่นกลางดึก", 
                                  min_value=0, max_value=10, value=1, step=1)
    
    st.subheader(" เวลาเข้านอนและตื่นนอน")
    bedtime_hour = st.slider("เวลาเข้านอน (ชั่วโมง)", 0, 23, 23,
                             help="เช่น 23 = 4 ทุ่ม, 0 = เที่ยงคืน")
    wakeup_hour = st.slider("เวลาตื่นนอน (ชั่วโมง)", 0, 23, 7,
                            help="เช่น 7 = 7 โมงเช้า")
    
    st.subheader("🧬 ไลฟ์สไตล์")
    caffeine = st.number_input("ปริมาณคาเฟอีนต่อวัน (มก.)", 
                                min_value=0, max_value=500, value=0, step=25,
                                help="กาแฟ 1 แก้ว ≈ 95 มก.")
    alcohol = st.number_input("ปริมาณแอลกอฮอล์ (หน่วย)", 
                               min_value=0.0, max_value=10.0, value=0.0, step=0.5)
    smoking = st.selectbox("สูบบุหรี่หรือไม่", ["ไม่สูบ", "สูบ"])
    exercise = st.selectbox("ความถี่ในการออกกำลังกาย (ครั้ง/สัปดาห์)", 
                            [0, 1, 2, 3, 4, 5, 6, 7])
    
    submitted = st.form_submit_button("🔮 ทำนายผล", use_container_width=True, type="primary")

# พื้นที่แสดงผลหลัก
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 ผลการทำนาย")
    
    if submitted:
        # แปลงข้อมูลให้ตรงกับโมเดล
        gender_val = 0 if gender == "ชาย (Male)" else 1
        smoking_val = 0 if smoking == "ไม่สูบ" else 1
        
        input_data = pd.DataFrame({
            'Age': [age],
            'Gender': [gender_val],
            'Sleep duration': [sleep_duration],
            'REM sleep percentage': [rem_sleep],
            'Deep sleep percentage': [deep_sleep],
            'Light sleep percentage': [light_sleep],
            'Awakenings': [awakenings],
            'Caffeine consumption': [caffeine],
            'Alcohol consumption': [alcohol],
            'Smoking status': [smoking_val],
            'Exercise frequency': [exercise],
            'Bedtime_hour': [bedtime_hour],
            'Wakeup_hour': [wakeup_hour]
        })
        
        # ทำนายผล
        input_scaled = scaler.transform(input_data[features])
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0]
        
        # แสดงผลลัพธ์
        if prediction == 1:
            st.markdown("""
            <div class="result-box good-result">
                <h2>✅ คุณภาพการนอนหลับ: ดี (Good)</h2>
                <p>Sleep Efficiency ≥ 0.80</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown("""
            <div class="result-box poor-result">
                <h2>⚠️ คุณภาพการนอนหลับ: ต้องปรับปรุง (Poor)</h2>
                <p>Sleep Efficiency < 0.80</p>
            </div>
            """, unsafe_allow_html=True)
        
        # แสดงความน่าจะเป็น
        st.subheader("📈 ความน่าจะเป็นของแต่ละประเภท")
        col_poor, col_good = st.columns(2)
        with col_poor:
            st.metric("😴 ต้องปรับปรุง (Poor)", f"{probability[0]*100:.2f}%")
        with col_good:
            st.metric("😊 ดี (Good)", f"{probability[1]*100:.2f}%")
        
        # กราฟแท่งความน่าจะเป็น
        prob_df = pd.DataFrame({
            'ประเภท': ['ต้องปรับปรุง', 'ดี'],
            'ความน่าจะเป็น (%)': [probability[0]*100, probability[1]*100]
        })
        st.bar_chart(prob_df.set_index('ประเภท'))
        
        # คำแนะนำ
        st.subheader(" คำแนะนำเพื่อสุขภาพการนอนที่ดีขึ้น")
        if prediction == 0:
            st.warning("**ผลการวิเคราะห์:** คุณภาพการนอนของคุณยังต้องปรับปรุง")
            st.markdown("""
            ### 🎯 แนวทางแก้ไข:
            
            1. 🛌 **ปรับเวลาเข้านอนให้เป็นเวลาเดิม** 
               - ควรเข้านอนและตื่นเวลาเดิมทุกวัน (รวมถึงวันหยุด)
            
            2. ☕ **ลดคาเฟอีน** 
               - หลีกเลี่ยงกาแฟ ชา น้ำอัดลม หลังบ่าย 2 โมง
            
            3. 📱 **ลดแสงสีฟ้าก่อนนอน** 
               - งดใช้โทรศัพท์/คอมพิวเตอร์ 1 ชั่วโมงก่อนนอน
            
            4. 🏃 **ออกกำลังกายสม่ำเสมอ** 
               - แต่ไม่ควรออกกำลังกายหนักภายใน 3 ชั่วโมงก่อนนอน
            
            5. 🍷 **ลดแอลกอฮอล์และบุหรี่** 
               - แอลกอฮอล์รบกวนช่วง REM sleep
               - บุหรี่มีนิโคตินซึ่งเป็นสารกระตุ้น
            
            6. 🌡️ **ปรับสภาพแวดล้อมการนอน** 
               - ห้องมืด เย็น และเงียบ
            """)
        else:
            st.success("**ผลการวิเคราะห์:** คุณมีคุณภาพการนอนหลับที่ดีมาก!")
            st.markdown("""
            ### 🎉 รักษามาตรฐานไว้:
            
            - 📅 **รักษากิจวัตร** - ทำตามตารางนอนปัจจุบันต่อไป
            - 💪 **พัฒนาต่อ** - เพิ่มการออกกำลังกายเพื่อคุณภาพที่ดีขึ้น
            -  **จัดการความเครียด** - โยคะหรือสมาธิก่อนนอนช่วยได้
            - 📊 **ติดตามผล** - บันทึกการนอนอย่างสม่ำเสมอ
            """)

with col2:
    st.subheader("📋 ข้อมูลที่คุณกรอก")
    if submitted:
        summary_df = pd.DataFrame({
            'รายการ': [
                'อายุ', 'เพศ', 'ระยะเวลานอน (ชม.)', 
                'REM Sleep (%)', 'หลับลึก (%)', 'หลับตื้น (%)',
                'จำนวนครั้งที่ตื่น', 'คาเฟอีน (มก.)', 'แอลกอฮอล์ (หน่วย)',
                'สูบบุหรี่', 'ออกกำลังกาย (ครั้ง/สัปดาห์)',
                'เวลาเข้านอน', 'เวลาตื่นนอน'
            ],
            'ค่า': [
                age, gender, sleep_duration,
                rem_sleep, deep_sleep, light_sleep,
                awakenings, caffeine, alcohol,
                smoking, exercise,
                f"{bedtime_hour}:00", f"{wakeup_hour}:00"
            ]
        })
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("️ เกี่ยวกับโมเดลนี้")
    st.info("""
    **อัลกอริทึม:** Support Vector Machine (SVM)  
    **เคอร์เนล:** RBF (Radial Basis Function)  
    **งาน:** การจำแนกประเภท 2 กลุ่ม (Binary Classification)  
    **เป้าหมาย:** Sleep Efficiency ≥ 0.80 = ดี
    
    **จำนวนฟีเจอร์:** 13 ตัวแปร  
    **ชุดข้อมูล:** Sleep Efficiency (452 ระเบียน)
    """)
    
    st.subheader(" เกณฑ์การประเมิน")
    st.markdown("""
    | ระดับ | Sleep Efficiency |
    |-------|-----------------|
    | 😊 ดี | ≥ 0.80 (80%) |
    | 😴 ต้องปรับปรุง | < 0.80 (80%) |
    """)

# Footer
st.markdown("---")
st.markdown("*พัฒนาด้วย ❤️ โดยระบบ Machine Learning เพื่อสุขภาพการนอนที่ดี*")