import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="Regression Prediction", page_icon="📊", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #2196F3 0%, #21CBF3 100%);
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
        background: linear-gradient(135deg, #2196F3 0%, #21CBF3 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📊 Linear Regression - ทำนายยอดขาย</p>', unsafe_allow_html=True)
st.markdown("### ทำนายยอดขายรวมด้วยอัลกอริทึม Linear Regression")
st.markdown("---")

# โหลดโมเดล
@st.cache_resource
def load_model():
    model_path = "models/regression_pipeline.pkl"
    
    if not os.path.exists(model_path):
        return None
    
    model = joblib.load(model_path)
    return model

model = load_model()

if model is None:
    st.error("❌ ไม่พบไฟล์โมเดล! โปรดตรวจสอบโฟลเดอร์ models/")
    st.stop()

# Sidebar - ฟอร์มกรอกข้อมูล
st.sidebar.header("📝 กรอกข้อมูลการขาย")
st.sidebar.markdown("---")

with st.sidebar.form("input_form"):
    st.subheader(" ข้อมูลสาขาและหมวดหมู่")
    branch = st.selectbox("สาขา (Branch)", ["A", "B", "C", "D", "E"])
    category = st.selectbox("หมวดหมู่สินค้า (Category)", 
                            ["Fashion", "Electronics", "Food & Beverage", "Beauty", "Home & Living", "Sports"])
    campaign = st.selectbox("แคมเปญส่งเสริมการขาย (Campaign)", 
                            ["None", "Weekend Boost", "Member Day", "Payday Promo", "Clearance Sale", "Mega Sale"])
    
    st.subheader("👥 ข้อมูลบุคลากรและลูกค้า")
    customers_count = st.number_input("จำนวนลูกค้า (Customers Count)", min_value=10, max_value=300, value=100, step=10)
    employee_count = st.number_input("จำนวนพนักงาน (Employee Count)", min_value=5, max_value=40, value=20, step=1)
    
    st.subheader("📦 ข้อมูลสินค้าและการเงิน")
    units_sold = st.number_input("จำนวนหน่วยที่ขายได้ (Units Sold)", min_value=10, max_value=300, value=100, step=10)
    avg_price_per_unit = st.number_input("ราคาเฉลี่ยต่อหน่วย (Avg Price)", min_value=10.0, max_value=5000.0, value=500.0, step=10.0)
    discount_rate = st.slider("อัตราส่วนลด (%)", 0.0, 30.0, 5.0, 0.1)
    cost_amount = st.number_input("ต้นทุนรวม (Cost Amount)", min_value=1000.0, max_value=200000.0, value=30000.0, step=1000.0)
    gross_profit = st.number_input("กำไรขั้นต้น (Gross Profit)", min_value=1000.0, max_value=200000.0, value=20000.0, step=1000.0)
    
    st.subheader("💳 การชำระเงินและความพึงพอใจ")
    payment_method = st.selectbox("วิธีการชำระเงิน (Payment Method)", 
                                  ["Credit Card", "E-Wallet", "QR Payment", "Mobile Banking", "Cash"])
    returned = st.selectbox("มีการคืนสินค้าหรือไม่ (Returned)", ["FALSE", "TRUE"])
    satisfaction_score = st.slider("คะแนนความพึงพอใจ (1-5)", 1.0, 5.0, 4.0, 0.1)
    
    st.subheader(" วันและเวลา")
    day_of_week = st.selectbox("วันในสัปดาห์ (Day of Week)", 
                               ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"])
    is_weekend = st.selectbox("เป็นวันหยุดสุดสัปดาห์หรือไม่ (Is Weekend)", ["FALSE", "TRUE"])
    
    submitted = st.form_submit_button("🔮 ทำนายยอดขาย", use_container_width=True, type="primary")

# พื้นที่แสดงผลหลัก
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💰 ผลการทำนายยอดขาย")
    
    if submitted:
        try:
            # สร้าง DataFrame
            input_data = pd.DataFrame({
                'branch': [branch],
                'category': [category],
                'campaign': [campaign],
                'customers_count': [customers_count],
                'employee_count': [employee_count],
                'units_sold': [units_sold],
                'avg_price_per_unit': [avg_price_per_unit],
                'discount_rate': [discount_rate],
                'cost_amount': [cost_amount],
                'gross_profit': [gross_profit],
                'payment_method': [payment_method],
                'is_weekend': [1 if is_weekend == "TRUE" else 0],
                'returned': [1 if returned == "TRUE" else 0],
                'satisfaction_score': [satisfaction_score],
                'day_of_week': [day_of_week]
            })
            
            # ทำนายผล (Pipeline จะจัดการ preprocessing ให้อัตโนมัติ)
            prediction = model.predict(input_data)[0]
            
            # จัดรูปแบบตัวเลข
            formatted_prediction = f"฿ {prediction:,.2f}"
            
            st.markdown(f"""
            <div class="result-box">
                <h2>💰 ยอดขายที่คาดการณ์</h2>
                <h1 style="font-size: 3rem; margin: 0;">{formatted_prediction}</h1>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            
            # คำแนะนำเพิ่มเติม
            st.subheader("💡 ข้อสังเกตและคำแนะนำ")
            profit_estimate = prediction - cost_amount
            
            if profit_estimate > 0:
                st.success(f"✅ **กำไรโดยประมาณ:** ฿ {profit_estimate:,.2f} (ยอดขายหักต้นทุน)")
            else:
                st.warning(f"⚠️ **ขาดทุนโดยประมาณ:** ฿ {profit_estimate:,.2f} (ควรปรับลดต้นทุนหรือเพิ่มยอดขาย)")
                
            st.info("📊 **Linear Regression** เป็นโมเดลเชิงเส้นที่ตีความได้ง่าย เหมาะสำหรับการวิเคราะห์ความสัมพันธ์ระหว่างตัวแปร")
            
        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาด: {str(e)}")

with col2:
    st.subheader(" ข้อมูลที่คุณกรอก")
    if submitted:
        summary_df = pd.DataFrame({
            'รายการ': [
                'สาขา', 'หมวดหมู่', 'แคมเปญ', 
                'จำนวนลูกค้า', 'จำนวนพนักงาน', 'จำนวนหน่วยที่ขาย',
                'ราคาเฉลี่ย/หน่วย', 'อัตราส่วนลด (%)', 'ต้นทุนรวม',
                'กำไรขั้นต้น', 'วิธีการชำระเงิน', 'มีการคืนสินค้า', 
                'คะแนนความพึงพอใจ', 'วันในสัปดาห์', 'วันหยุดสุดสัปดาห์'
            ],
            'ค่า': [
                branch, category, campaign,
                customers_count, employee_count, units_sold,
                f"฿ {avg_price_per_unit:,.2f}", f"{discount_rate}%", f"฿ {cost_amount:,.2f}",
                f"฿ {gross_profit:,.2f}", payment_method, returned,
                satisfaction_score, day_of_week, is_weekend
            ]
        })
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("ℹ️ เกี่ยวกับโมเดล")
    st.markdown("""
    **อัลกอริทึม:** Linear Regression  
    **งาน:** Regression (ทำนายค่าต่อเนื่อง)  
    **เป้าหมาย:** Sales Amount (ยอดขายรวม)  
    **จำนวนฟีเจอร์:** 15 ตัวแปร  
    
    **ข้อดีของ Linear Regression:**
    - ตีความได้ง่าย (เห็นความสัมพันธ์เชิงเส้น)
    - รวดเร็วในการเทรนและทำนาย
    - ใช้ Pipeline จัดการ preprocessing อัตโนมัติ
    """)

# Footer
st.markdown("---")
st.markdown("*พัฒนาด้วย ❤️ โดยระบบ Machine Learning เพื่อการพยากรณ์ยอดขาย*")