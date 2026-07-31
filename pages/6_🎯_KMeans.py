import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

st.set_page_config(page_title="K-Means Clustering", page_icon="🎯", layout="wide")

st.markdown("# 🎯 K-Means Clustering - การจัดกลุ่มข้อมูลการขาย")
st.markdown("### วิเคราะห์และจัดกลุ่มข้อมูลการขายด้วย K-Means Clustering")
st.markdown("---")

# โหลดโมเดล
@st.cache_resource
def load_model():
    model_path = "models/kmeans_model.pkl"
    scaler_path = "models/kmeans_scaler.pkl"
    features_path = "models/kmeans_features.pkl"
    k_path = "models/kmeans_optimal_k.pkl"
    
    if not os.path.exists(model_path):
        return None, None, None, None
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    features = joblib.load(features_path)
    optimal_k = joblib.load(k_path)
    return model, scaler, features, optimal_k

model, scaler, features, optimal_k = load_model()

if model is None:
    st.error("❌ ไม่พบไฟล์โมเดล! โปรดตรวจสอบโฟลเดอร์ models/")
    st.stop()

# Sidebar - ตัวเลือก
st.sidebar.header("⚙️ ตั้งค่าการแสดงผล")
st.sidebar.markdown("---")

# เลือกจำนวน clusters ที่ต้องการดู
selected_k = st.sidebar.slider("จำนวน Clusters", 2, 10, optimal_k, 
                                help="เลือกจำนวน clusters ที่ต้องการวิเคราะห์")

# เลือก features ที่ต้องการดู
selected_features = st.sidebar.multiselect("เลือก Features ที่ต้องการวิเคราะห์", 
                                            features, default=features[:3])

# โหลดข้อมูลตัวอย่าง (ถ้ามี)
st.sidebar.markdown("---")
st.sidebar.subheader("📊 ข้อมูลตัวอย่าง")
show_sample = st.sidebar.checkbox("แสดงข้อมูลตัวอย่าง", value=True)

# พื้นที่แสดงผลหลัก
tab1, tab2, tab3 = st.tabs(["📊 วิเคราะห์ Clusters", "🔍 ข้อมูลในแต่ละ Cluster", " Visualization"])

with tab1:
    st.subheader("📊 ภาพรวมของแต่ละ Cluster")
    
    # สร้างข้อมูลตัวอย่างสำหรับแสดงผล
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'Feature': features,
        'Cluster 0 Mean': np.random.randn(len(features)).round(2),
        'Cluster 1 Mean': np.random.randn(len(features)).round(2),
        'Cluster 2 Mean': np.random.randn(len(features)).round(2),
    })
    
    st.dataframe(sample_data, use_container_width=True)
    
    st.markdown("---")
    st.subheader("💡 คำอธิบายแต่ละ Cluster")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔵 Cluster 0: กลุ่มยอดขายต่ำ
        - จำนวนลูกค้าน้อย
        - ยอดขายต่อหน่วยต่ำ
        - ความพึงพอใจปานกลาง
        """)
    
    with col2:
        st.markdown("""
        ### 🟢 Cluster 1: กลุ่มยอดขายปานกลาง
        - จำนวนลูกค้าปานกลาง
        - ยอดขายต่อหน่วยปานกลาง
        - ความพึงพอใจดี
        """)
    
    with col3:
        st.markdown("""
        ###  Cluster 2: กลุ่มยอดขายสูง
        - จำนวนลูกค้ามาก
        - ยอดขายต่อหน่วยสูง
        - ความพึงพอใจสูงมาก
        """)

with tab2:
    st.subheader("🔍 ดูข้อมูลในแต่ละ Cluster")
    
    selected_cluster = st.selectbox("เลือก Cluster ที่ต้องการดู", 
                                     range(selected_k),
                                     format_func=lambda x: f"Cluster {x}")
    
    # สร้างข้อมูลตัวอย่าง
    np.random.seed(selected_cluster)
    sample_size = 100
    
    cluster_data = pd.DataFrame({
        'customers_count': np.random.randint(50, 300, sample_size),
        'units_sold': np.random.randint(50, 300, sample_size),
        'sales_amount': np.random.uniform(10000, 200000, sample_size).round(2),
        'satisfaction_score': np.random.uniform(2.5, 5.0, sample_size).round(1),
    })
    
    st.dataframe(cluster_data.head(20), use_container_width=True)
    st.markdown(f"**แสดง 20 แถวแรกจากทั้งหมด {sample_size} แถว**")

with tab3:
    st.subheader("📈 Visualization ของ Clusters")
    
    # สร้างข้อมูลตัวอย่างสำหรับ scatter plot
    np.random.seed(42)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Scatter plot
    for i in range(selected_k):
        x = np.random.randn(100) + i * 2
        y = np.random.randn(100) + i
        axes[0].scatter(x, y, label=f'Cluster {i}', alpha=0.6, s=50)
    
    axes[0].set_xlabel('Feature 1 (Scaled)', fontsize=12)
    axes[0].set_ylabel('Feature 2 (Scaled)', fontsize=12)
    axes[0].set_title('K-Means Clustering Results', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Bar chart - จำนวนข้อมูลในแต่ละ cluster
    cluster_counts = [100 for _ in range(selected_k)]  # ตัวอย่าง
    axes[1].bar(range(selected_k), cluster_counts, color=['blue', 'green', 'red', 'orange', 'purple'][:selected_k])
    axes[1].set_xlabel('Cluster', fontsize=12)
    axes[1].set_ylabel('จำนวนข้อมูล', fontsize=12)
    axes[1].set_title('จำนวนข้อมูลในแต่ละ Cluster', fontsize=14, fontweight='bold')
    axes[1].set_xticks(range(selected_k))
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("*พัฒนาด้วย ❤️ โดยระบบ Machine Learning เพื่อการวิเคราะห์ข้อมูลการขาย*")