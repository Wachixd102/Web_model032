import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="KNN Price Prediction", page_icon="👥", layout="wide")

st.markdown("# 👥 KNN - ทำนายราคาบ้าน (California Housing)")
st.markdown("### ทำนายราคาบ้านโดยประมาณด้วยอัลกอริทึม K-Nearest Neighbors (Regression)")
st.markdown("---")

# โหลดโมเดล
@st.cache_resource
def load_model():
    model_path = "models/knn_model.pkl"
    scaler_path = "models/knn_scaler.pkl"
    features_path = "models/knn_features.pkl"
    
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
st.sidebar.header("📝 กรอกข้อมูลอสังหาริมทรัพย์")
st.sidebar.markdown("---")

with st.sidebar.form("input_form"):
    st.subheader("📍 ทำเลที่ตั้ง")
    longitude = st.number_input("ลองจิจูด (Longitude)", min_value=-125.0, max_value=-114.0, value=-122.0, step=0.1)
    latitude = st.number_input("ละติจูด (Latitude)", min_value=32.0, max_value=42.0, value=37.0, step=0.1)
    
    st.subheader("🏠 ลักษณะบ้าน")
    housing_median_age = st.number_input("อายุบ้านโดยเฉลี่ย (ปี)", min_value=1, max_value=100, value=30, step=1)
    total_rooms = st.number_input("จำนวนห้องทั้งหมด", min_value=1, max_value=50000, value=2000, step=10)
    total_bedrooms = st.number_input("จำนวนห้องนอนทั้งหมด", min_value=1, max_value=10000, value=500, step=10)
    households = st.number_input("จำนวนครัวเรือน", min_value=1, max_value=10000, value=500, step=10)
    
    st.subheader("👥 ประชากรและรายได้")
    population = st.number_input("จำนวนประชากร", min_value=1, max_value=50000, value=1000, step=10)
    median_income = st.number_input("รายได้มัธยฐาน (หน่วย: $1,000)", min_value=0.1, max_value=15.0, value=3.0, step=0.1, 
                                    help="ตัวอย่าง: 3.0 หมายถึง $3,000")
    
    submitted = st.form_submit_button("🔮 ทำนายราคาบ้าน", use_container_width=True, type="primary")

# พื้นที่แสดงผลหลัก
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💰 ผลการทำนายราคาบ้าน")
    
    if submitted:
        input_data = pd.DataFrame({
            'longitude': [longitude],
            'latitude': [latitude],
            'housing_median_age': [housing_median_age],
            'total_rooms': [total_rooms],
            'total_bedrooms': [total_bedrooms],
            'population': [population],
            'households': [households],
            'median_income': [median_income]
        })
        
        # Scale และทำนาย
        input_scaled = scaler.transform(input_data[features])
        prediction = model.predict(input_scaled)[0]
        
        # จัดรูปแบบราคา
        formatted_price = f"${prediction:,.2f}"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center; color: white; margin: 1rem 0;">
            <h2>🏡 ราคาบ้านโดยประมาณ</h2>
            <h1 style="font-size: 3rem; margin: 0;">{formatted_price}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        
        # คำแนะนำเพิ่มเติม
        st.subheader("💡 ข้อสังเกต")
        if prediction > 300000:
            st.info("📈 **พื้นที่ราคาสูง:** ทำเลนี้น่าจะมีสิ่งอำนวยความสะดวกครบครัน หรืออยู่ในย่านธุรกิจ/ชายทะเล")
        elif prediction > 150000:
            st.info("📊 **พื้นที่ราคาปานกลาง:** เป็นทำเลที่อยู่อาศัยทั่วไป มีความสมดุลระหว่างราคาและสิ่งอำนวยความสะดวก")
        else:
            st.info("📉 **พื้นที่ราคาประหยัด:** อาจอยู่ห่างจากใจกลางเมือง หรือเป็นพื้นที่ที่กำลังพัฒนา")

with col2:
    st.subheader("📋 ข้อมูลที่คุณกรอก")
    if submitted:
        summary_df = pd.DataFrame({
            'รายการ': [
                'ลองจิจูด', 'ละติจูด', 'อายุบ้าน (ปี)', 
                'จำนวนห้องทั้งหมด', 'จำนวนห้องนอน', 'จำนวนครัวเรือน',
                'จำนวนประชากร', 'รายได้มัธยฐาน ($1,000)'
            ],
            'ค่า': [
                longitude, latitude, housing_median_age,
                total_rooms, total_bedrooms, households,
                population, f"{median_income:.1f}"
            ]
        })
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("ℹ️ เกี่ยวกับโมเดล")
    st.markdown("""
    **อัลกอริทึม:** K-Nearest Neighbors (KNN) Regressor  
    **งาน:** Regression (ทำนายค่าต่อเนื่อง)  
    **เป้าหมาย:** Median House Value  
    **จำนวนฟีเจอร์:** 8 ตัวแปร  
    
    *หมายเหตุ: KNN ทำงานโดยหาราคาเฉลี่ยจาก 'บ้านที่คล้ายกันที่สุด' (Neighbors) ในข้อมูลฝึกสอน*
    """)

# Footer
st.markdown("---")
st.markdown("*พัฒนาด้วย ❤️ โดยระบบ Machine Learning เพื่อการประเมินราคาอสังหาริมทรัพย์*")