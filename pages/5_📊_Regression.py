import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="Regression - Sales Prediction", page_icon="", layout="wide")

st.markdown("#  Regression - ทำนายยอดขายรวม")
st.markdown("### ทำนายยอดขาย (Sales Amount) ด้วย Random Forest Regressor")
st.markdown("---")

# โหลดโมเดลและรายการ Features
@st.cache_resource
def load_model():
    model_path = "models/regression_pipeline.pkl"
    features_path = "models/regression_features.pkl"
    
    if not os.path.exists(model_path):
        return None, None
    
    model = joblib.load(model_path)
    features = joblib.load(features_path)
    return model, features

model, original_features = load_model()

if model is None:
    st.error("❌ ไม่พบไฟล์โมเดล! โปรดตรวจสอบโฟลเดอร์ models/")
    st.stop()

# Sidebar - ฟอร์มกรอกข้อมูล
st.sidebar.header(" กรอกข้อมูลการขาย")
st.sidebar.markdown("---")

with st.sidebar.form("input_form"):
    st.subheader("🏪 ข้อมูลสาขาและหมวดหมู่")
    branch = st.selectbox("สาขา (Branch)", ["A", "B", "C", "D", "E"])
    category = st.selectbox("หมวดหมู่สินค้า (Category)", ["Fashion", "Electronics", "Food & Beverage", "Beauty", "Home & Living", "Sports"])
    campaign = st.selectbox("แคมเปญ (Campaign)", ["None", "Weekend Boost", "Member Day", "Payday Promo", "Clearance Sale", "Mega Sale"])
    
    st.subheader("👥 ข้อมูลบุคลากรและลูกค้า")
    customers_count = st.number_input("จำนวนลูกค้า (Customers Count)", min_value=10, max_value=500, value=100, step=10)
    employee_count = st.number_input("จำนวนพนักงาน (Employee Count)", min_value=5, max_value=50, value=20, step=1)
    
    st.subheader("📦 ข้อมูลสินค้าและการเงิน")
    units_sold = st.number_input("จำนวนหน่วยที่ขายได้ (Units Sold)", min_value=10, max_value=500, value=100, step=10)
    avg_price_per_unit = st.number_input("ราคาเฉลี่ยต่อหน่วย (Avg Price)", min_value=10.0, max_value=5000.0, value=500.0, step=10.0)
    discount_rate = st.slider("อัตราส่วนลด (Discount Rate)", 0.0, 30.0, 5.0, 0.1, help="เช่น 5.0 หมายถึง 5%")
    cost_amount = st.number_input("ต้นทุนรวม (Cost Amount)", min_value=1000.0, max_value=200000.0, value=30000.0, step=1000.0)
    gross_profit = st.number_input("กำไรขั้นต้น (Gross Profit)", min_value=1000.0, max_value=200000.0, value=20000.0, step=1000.0)
    
    st.subheader("📅 เงื่อนไขพิเศษ")
    is_weekend = st.selectbox("เป็นวันหยุดสุดสัปดาห์หรือไม่?", ["FALSE", "TRUE"])
    returned = st.selectbox("มีการคืนสินค้าหรือไม่?", ["FALSE", "TRUE"])
    payment_method = st.selectbox("วิธีการชำระเงิน (Payment Method)", ["Credit Card", "E-Wallet", "QR Payment", "Mobile Banking", "Cash"])
    day_of_week = st.selectbox("วันในสัปดาห์ (Day of Week)", ["วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์", "วันเสาร์", "วันอาทิตย์"])
    satisfaction_score = st.slider("คะแนนความพึงพอใจ (Satisfaction Score)", 1.0, 5.0, 4.0, 0.1)
    
    submitted = st.form_submit_button("🔮 ทำนายยอดขาย", use_container_width=True, type="primary")

# พื้นที่แสดงผลหลัก
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💰 ผลการทำนายยอดขาย")
    
    if submitted:
        # สร้าง DataFrame จากข้อมูลที่ผู้ใช้กรอก
        input_data = pd.DataFrame({
            'customers_count': [customers_count],
            'employee_count': [employee_count],
            'units_sold': [units_sold],
            'avg_price_per_unit': [avg_price_per_unit],
            'discount_rate': [discount_rate],
            'cost_amount': [cost_amount],
            'gross_profit': [gross_profit],
            'is_weekend': [1 if is_weekend == "TRUE" else 0],
            'returned': [1 if returned == "TRUE" else 0],
            'satisfaction_score': [satisfaction_score],
            'payment_method': [payment_method],
            'branch': [branch],
            'category': [category],
            'campaign': [campaign],
            'day_of_week': [day_of_week]
        })
        
        # ทำนายผล
        prediction = model.predict(input_data)[0]
        
        # จัดรูปแบบตัวเลข
        formatted_prediction = f"{prediction:,.2f}"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center; color: white; margin: 1rem 0;">
            <h2>💰 ยอดขายที่คาดการณ์</h2>
            <h1 style="font-size: 3rem; margin: 0;">฿ {formatted_prediction}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.balloons()
        
        # คำแนะนำเพิ่มเติม
        st.subheader("💡 ข้อสังเกตและคำแนะนำ")
        if prediction > 100000:
            st.success(f"✅ **ยอดขายสูงมาก!** คาดการณ์ยอดขายได้ ฿ {prediction:,.2f}")
            st.info("📊 **ปัจจัยที่ส่งผล:** จำนวนลูกค้าสูง, ยอดขายต่อหน่วยดี, หรือมีแคมเปญส่งเสริมการขายที่ดี")
        elif prediction > 50000:
            st.info(f"️ **ยอดขายปานกลาง** คาดการณ์ยอดขายได้ ฿ {prediction:,.2f}")
            st.info("📊 **คำแนะนำ:** เพิ่มจำนวนลูกค้าหรือปรับแคมเปญส่งเสริมการขาย")
        else:
            st.warning(f"⚠️ **ยอดขายต่ำ** คาดการณ์ยอดขายได้ ฿ {prediction:,.2f}")
            st.info("📊 **คำแนะนำ:** ควรปรับปรุงกลยุทธ์การขาย เพิ่มโปรโมชั่น หรือขยายฐานลูกค้า")

with col2:
    st.subheader("📋 ข้อมูลที่คุณกรอก")
    if submitted:
        summary_df = pd.DataFrame({
            'รายการ': [
                'สาขา', 'หมวดหมู่', 'แคมเปญ', 
                'จำนวนลูกค้า', 'จำนวนพนักงาน', 'จำนวนหน่วยที่ขาย',
                'ราคาเฉลี่ย/หน่วย', 'อัตราส่วนลด (%)', 'ต้นทุนรวม',
                'กำไรขั้นต้น', 'วันหยุดสุดสัปดาห์', 'มีการคืนสินค้า', 
                'วิธีการชำระเงิน', 'วันในสัปดาห์', 'คะแนนความพึงพอใจ'
            ],
            'ค่า': [
                branch, category, campaign,
                customers_count, employee_count, units_sold,
                f"฿ {avg_price_per_unit:,.2f}", f"{discount_rate}%", f"฿ {cost_amount:,.2f}",
                f"฿ {gross_profit:,.2f}", is_weekend, returned, 
                payment_method, day_of_week, satisfaction_score
            ]
        })
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("ℹ️ เกี่ยวกับโมเดล")
    st.markdown("""
    **อัลกอริทึม:** Random Forest Regressor  
    **งาน:** Regression (ทำนายค่าต่อเนื่อง)  
    **เป้าหมาย:** Sales Amount (ยอดขายรวม)  
    **จำนวนฟีเจอร์:** 15 ตัวแปร  
    
    *หมายเหตุ: โมเดลนี้ใช้ Ensemble Learning เพื่อลด Overfitting และจัดการกับความสัมพันธ์ที่ซับซ้อนระหว่างฟีเจอร์ได้ดี*
    """)

# Footer
st.markdown("---")
st.markdown("*พัฒนาด้วย ❤️ โดยระบบ Machine Learning เพื่อการพยากรณ์ยอดขาย*")