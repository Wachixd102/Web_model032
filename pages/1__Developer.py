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
    avatar_url = "https://scontent.fbkk22-2.fna.fbcdn.net/v/t39.30808-6/711709473_2394837197667750_2574019075777161019_n.jpg?stp=dst-jpg_tt6&cstp=mx960x960&ctp=s960x960&_nc_cat=103&_nc_map=urlgen_bucketless&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeHyrJ0ZpMEU7qsxr6K6HwgCqJDikdAp1_mokOKR0CnX-aLJqAOrj1A_c9LKyLR2Qpn_DCnjIDeuwD2XaCr6DHGN&_nc_ohc=ilRFXDdib5YQ7kNvwGVlfEp&_nc_oc=AdrnT0qd7idL1Xb4Ijc0ZgweHZ_-czNs3RCGwB0phBJzXdky4WqxFyhAKmp3cTzlw5o&_nc_zt=23&_nc_ht=scontent.fbkk22-2.fna&_nc_gid=nvM4W5q9JoJepDyLMeJdLQ&_nc_ss=7b2a8&oh=00_AQFt_wlc73DVvyCcKdIMAlCnLCBkou-sfmGKWKQxpkc2YA&oe=6A725D96"
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
    <h3 style="color: #000000; text-align: center;"> ข้อมูลส่วนตัว</h3>
    <hr style="border: 2px solid #000000;">
    <p style="font-size: 1.3rem; text-align: center;">
        <strong>👤 ชื่อ-นามสกุล:</strong><br>
        <span style="font-size: 1.5rem; color: #000000;">วชิรวิทย์ พรสวาท</span>
    </p>
    <p style="font-size: 1.3rem; text-align: center;">
        <strong>🎓 รหัสนักศึกษา:</strong><br>
        <span style="font-size: 1.5rem; color: #000000;">664245032</span>
    </p>
    <p style="font-size: 1.2rem; text-align: center;">
        <strong>📧 อีเมล:</strong><br>
        <span style="font-size: 1.5rem; color: #000000;">alonenightcore02@gmail.com/span>
    </p>
    <p style="font-size: 1.2rem; text-align: center;">
        <strong>🏫 สถาบัน:</strong><br>
        <span style="font-size: 1.5rem; color: #000000;">มหาวิทยาลัยราชภัฏนครปฐม</span>
    </p>
    <p style="font-size: 1.2rem; text-align: center;">
        <span style="font-size: 1.5rem; color: #000000;">ปีการศึกษา:</strong><br>
        2566</span>
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