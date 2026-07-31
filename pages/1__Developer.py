import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="ข้อมูลผู้พัฒนา", page_icon="👤", layout="wide")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Sarabun', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    
    .profile-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .profile-image {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        border: 5px solid white;
        object-fit: cover;
        margin-bottom: 1rem;
    }
    
    .info-box {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">👤 ข้อมูลผู้พัฒนา</p>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# ส่วนที่ 1: โหลดรูปภาพ
# ============================================================
# ตรวจสอบว่ามีไฟล์รูปภาพหรือไม่
image_paths = [
    "profile.jpg",
    "profile.png", 
    "developer.jpg",
    "developer.png",
    "assets/profile.jpg",
    "assets/profile.png"
]

profile_image = None
for path in image_paths:
    if os.path.exists(path):
        profile_image = Image.open(path)
        break

# ถ้าไม่มีรูป ใช้ avatar จาก UI Avatars API
if profile_image is None:
    avatar_url = "https://ui-avatars.com/api/?name=วชิรวิทย์+พรสวาท&size=200&background=667eea&color=fff&bold=true"
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <img src="{avatar_url}" style="width: 200px; height: 200px; border-radius: 50%; border: 5px solid #667eea;">
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
    """, unsafe_allow_html=True)
    st.image(profile_image, width=200)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# ส่วนที่ 2: ข้อมูลผู้พัฒนา
# ============================================================
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    <div class="info-box">
        <h3 style="color: #667eea; text-align: center;">📋 ข้อมูลส่วนตัว</h3>
        <hr style="border: 1px solid #667eea;">
        <p style="font-size: 1.1rem;"><strong>👤 ชื่อ-นามสกุล:</strong><br>วชิรวิทย์ พรสวาท</p>
        <p style="font-size: 1.1rem;"><strong> รหัสนักศึกษา:</strong><br>664245032</p>
        <p style="font-size: 1.1rem;"><strong>📧 อีเมล:</strong><br>wachirawit.p@student.example.com</p>
        <p style="font-size: 1.1rem;"><strong>🏫 สถาบัน:</strong><br>มหาวิทยาลัย...</p>
        <p style="font-size: 1.1rem;"><strong>📅 ปีการศึกษา:</strong><br>2566</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
        <h3 style="color: #667eea;">📝 เกี่ยวกับโปรเจกต์</h3>
        <hr style="border: 1px solid #667eea;">
        <p style="font-size: 1.1rem;">
            <strong>ชื่อโปรเจกต์:</strong> ระบบทำนายข้อมูลด้วย Machine Learning
        </p>
        <p style="font-size: 1.1rem;">
            <strong>คำอธิบาย:</strong> โปรเจกต์นี้พัฒนาขึ้นเพื่อศึกษาและประยุกต์ใช้ 
            อัลกอริทึม Machine Learning 6 ชนิด ในการทำนายและวิเคราะห์ข้อมูล 
            โดยมีการพัฒนาเป็นเว็บแอปพลิเคชันด้วย Streamlit
        </p>
    </div>
    
    <div class="info-box">
        <h3 style="color: #667eea;">🛠️ เทคโนโลยีที่ใช้</h3>
        <hr style="border: 1px solid #667eea;">
        <div style="text-align: center;">
            <span class="skill-tag">🐍 Python</span>
            <span class="skill-tag">🤖 Scikit-Learn</span>
            <span class="skill-tag">📊 Pandas</span>
            <span class="skill-tag">🔢 NumPy</span>
            <span class="skill-tag">📈 Matplotlib</span>
            <span class="skill-tag">🎨 Seaborn</span>
            <span class="skill-tag">🌐 Streamlit</span>
            <span class="skill-tag">📝 Jupyter Notebook</span>
            <span class="skill-tag"> Git & GitHub</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# ส่วนที่ 3: อัลกอริทึมที่ใช้
# ============================================================
st.markdown("---")
st.markdown("""
<div class="info-box">
    <h3 style="color: #667eea; text-align: center;"> อัลกอริทึม Machine Learning ที่ใช้</h3>
    <hr style="border: 1px solid #667eea;">
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-box" style="text-align: center;">
        <h4 style="color: #667eea;">🧠 SVM</h4>
        <p>Support Vector Machine<br>ใช้ทำนายคุณภาพการนอนหลับ</p>
        <p><strong>Dataset:</strong> Sleep Efficiency</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box" style="text-align: center;">
        <h4 style="color: #667eea;"> Regression</h4>
        <p>Linear Regression<br>ใช้ทำนายยอดขาย</p>
        <p><strong>Dataset:</strong> Mall Sales</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box" style="text-align: center;">
        <h4 style="color: #667eea;"> Decision Tree</h4>
        <p>Decision Tree Classifier<br>ใช้ทำนายโรคหัวใจ</p>
        <p><strong>Dataset:</strong> Heart Disease</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box" style="text-align: center;">
        <h4 style="color: #667eea;"> Random Forest</h4>
        <p>Random Forest Regressor<br>ใช้ทำนายยอดขาย</p>
        <p><strong>Dataset:</strong> Mall Sales</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-box" style="text-align: center;">
        <h4 style="color: #667eea;">👥 KNN</h4>
        <p>K-Nearest Neighbors<br>ใช้ทำนายราคาบ้าน</p>
        <p><strong>Dataset:</strong> California Housing</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box" style="text-align: center;">
        <h4 style="color: #667eea;">🎯 K-Means</h4>
        <p>K-Means Clustering<br>ใช้จัดกลุ่มข้อมูลการขาย</p>
        <p><strong>Dataset:</strong> Mall Sales</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# ส่วนที่ 4: Footer
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 15px; color: white; margin-top: 2rem;">
    <h3>✨ ขอบคุณที่เข้าชมโปรเจกต์นี้ ✨</h3>
    <p style="font-size: 1.1rem;">พัฒนาโดย วชิรวิทย์ พรสวาท | รหัสนักศึกษา 664245032</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">© 2026 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)