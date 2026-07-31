import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Sleep Quality Prediction",
    page_icon="🛌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .model-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        transition: transform 0.3s;
    }
    .model-card:hover {
        transform: translateY(-5px);
    }
</style>
""", unsafe_allow_html=True)

# Main Title
st.markdown('<p class="main-title">🛌 Sleep Quality Prediction System</p>', unsafe_allow_html=True)
st.markdown("### ระบบทำนายคุณภาพการนอนหลับด้วย Machine Learning 6 โมเดล")
st.markdown("---")

# Introduction
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📊 Dataset", "Sleep Efficiency")
with col2:
    st.metric("🤖 Models", "6 Algorithms")
with col3:
    st.metric("🎯 Target", "Sleep Quality")

st.markdown("---")

# Model Cards
st.subheader("🎯 เลือกโมเดลที่ต้องการใช้งาน")

models = [
    {"name": "SVM (Support Vector Machine)", "icon": "🧠", "page": "1_🧠_SVM", 
     "desc": "โมเดลที่ใช้แยกประเภทด้วย Hyperplane เหมาะกับข้อมูลที่มีมิติสูง", "status": "✅ พร้อมใช้งาน"},
    {"name": "Decision Tree", "icon": "🌳", "page": "2_🌳_Decision_Tree",
     "desc": "โมเดลแบบต้นไม้ตัดสินใจ ตีความผลได้ง่าย", "status": "🔜 เร็วๆ นี้"},
    {"name": "KNN (K-Nearest Neighbors)", "icon": "👥", "page": "3_👥_KNN",
     "desc": "โมเดลที่ใช้ระยะทางหาเพื่อนบ้านที่ใกล้ที่สุด", "status": "🔜 เร็วๆ นี้"},
    {"name": "Random Forest", "icon": "🌲", "page": "4_🌲_Random_Forest",
     "desc": "โมเดลแบบ Ensemble ที่รวม Decision Tree หลายต้น", "status": "🔜 เร็วๆ นี้"},
    {"name": "Regression", "icon": "📊", "page": "5_📊_Regression",
     "desc": "โมเดลสำหรับทำนายค่าต่อเนื่อง (Sleep Efficiency)", "status": "🔜 เร็วๆ นี้"},
    {"name": "K-Means Clustering", "icon": "🎯", "page": "6_🎯_KMeans",
     "desc": "โมเดลแบบ Unsupervised สำหรับจัดกลุ่มข้อมูล", "status": "🔜 เร็วๆ นี้"},
]

cols = st.columns(2)
for idx, model in enumerate(models):
    with cols[idx % 2]:
        st.markdown(f"""
        <div class="model-card">
            <h2>{model['icon']} {model['name']}</h2>
            <p>{model['desc']}</p>
            <p><strong>{model['status']}</strong></p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
### 📖 เกี่ยวกับโปรเจกต์
โปรเจกต์นี้พัฒนาโดยการใช้ **Machine Learning 6 อัลกอริทึม** เพื่อทำนายคุณภาพการนอนหลับ 
จากปัจจัยต่างๆ เช่น อายุ, เพศ, ระยะเวลาการนอน, การบริโภคคาเฟอีน/แอลกอฮอล์, การสูบบุหรี่ ฯลฯ

**วิธีใช้งาน:** เลือกโมเดลจากเมนูด้านซ้ายมือ แล้วกรอกข้อมูลเพื่อทำนายผล
""")