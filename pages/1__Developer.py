import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="ข้อมูลผู้พัฒนา", page_icon="👤", layout="wide")

# Custom CSS - แก้ไขแล้ว (ไม่กระทบตัวอักษรส่วนอื่น)
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
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .profile-card h1,
    .profile-card h2,
    .profile-card h3,
    .profile-card p {
        color: white !important;
    }
    
    .info-box {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .footer-box {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-top: 2rem;
    }
    
    .footer-box h3,
    .footer-box p {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">👤 ข้อมูลผู้พัฒนา</p>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# ส่วนที่ 1: โหลดรูปภาพ
# ============================================================
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
st.markdown("""
<div class="info-box" style="max-width: 600px; margin: 0 auto;">
    <h3 style="color: #667eea; text-align: center;"> ข้อมูลส่วนตัว</h3>
    <hr style="border: 2px solid #667eea;">
    <p style="font-size: 1.3rem; text-align: center;">
        <strong>👤 ชื่อ-นามสกุล:</strong><br>
        <span style="font-size: 1.5rem; color: #764ba2;">วชิรวิทย์ พรสวาท</span>
    </p>
    <p style="font-size: 1.3rem; text-align: center;">
        <strong>🎓 รหัสนักศึกษา:</strong><br>
        <span style="font-size: 1.5rem; color: #764ba2;">664245032</span>
    </p>
    <p style="font-size: 1.2rem; text-align: center;">
        <strong>📧 อีเมล:</strong><br>
        wachirawit.p@student.example.com
    </p>
    <p style="font-size: 1.2rem; text-align: center;">
        <strong>🏫 สถาบัน:</strong><br>
        มหาวิทยาลัย...
    </p>
    <p style="font-size: 1.2rem; text-align: center;">
        <strong>📅 ปีการศึกษา:</strong><br>
        2566
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# ส่วนที่ 3: Footer
# ============================================================
st.markdown("""
<div class="footer-box">
    <h3>✨ ขอบคุณที่เข้าชม ✨</h3>
    <p style="font-size: 1.1rem;">พัฒนาโดย วชิรวิทย์ พรสวาท | รหัสนักศึกษา 664245032</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">© 2026 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)