import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

st.set_page_config(page_title="K-Means Clustering", page_icon="🎯", layout="wide")

st.markdown("# 🎯 K-Means Clustering - การจัดกลุ่มข้อมูลการขาย")
st.markdown("### วิเคราะห์และจัดกลุ่มข้อมูลการขายด้วย K-Means Clustering")
st.markdown("---")

# โหลดข้อมูล
@st.cache_data
def load_data():
    # ลองโหลดจากไฟล์ CSV
    csv_path = "mall_sales_eda_3000_records(Sales_Data).csv"
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None

df = load_data()

if df is None:
    st.error("❌ ไม่พบไฟล์ข้อมูล! โปรดวางไฟล์ `mall_sales_eda_3000_records(Sales_Data).csv` ในโฟลเดอร์โปรเจกต์")
    st.stop()

# ทำความสะอาดข้อมูล
st.sidebar.header("⚙️ ตั้งค่า")

# เลือกจำนวน clusters
n_clusters = st.sidebar.slider("จำนวนกลุ่ม (Clusters)", 2, 10, 4)

# เลือก features
st.sidebar.subheader("เลือกตัวแปร")
available_features = ['customers_count', 'employee_count', 'units_sold', 
                      'avg_price_per_unit', 'sales_amount', 'cost_amount', 
                      'gross_profit', 'satisfaction_score']

selected_features = st.sidebar.multiselect(
    "เลือกตัวแปรที่ต้องการใช้",
    available_features,
    default=['customers_count', 'units_sold', 'sales_amount']
)

if len(selected_features) < 2:
    st.warning("⚠️ โปรดเลือกอย่างน้อย 2 ตัวแปร")
    st.stop()

# ทำความสะอาดข้อมูล
df_clean = df[selected_features].copy()
df_clean = df_clean.fillna(df_clean.median())

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clean)

# รัน K-Means
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)
df_clean['Cluster'] = clusters

# แสดงผล
st.success(f"✅ จัดกลุ่มข้อมูลเสร็จสิ้น! พบ {n_clusters} กลุ่ม")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 ภาพรวม", " กราฟ", "📋 ข้อมูลในแต่ละกลุ่ม"])

with tab1:
    st.subheader("📊 ภาพรวมของแต่ละกลุ่ม")
    
    # แสดงจำนวนข้อมูลในแต่ละ cluster
    cluster_counts = df_clean['Cluster'].value_counts().sort_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### จำนวนข้อมูลในแต่ละกลุ่ม")
        st.bar_chart(cluster_counts)
    
    with col2:
        st.markdown("### สัดส่วนของแต่ละกลุ่ม")
        fig, ax = plt.subplots()
        ax.pie(cluster_counts, labels=[f'กลุ่ม {i}' for i in cluster_counts.index], 
               autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    
    # แสดงค่าเฉลี่ยของแต่ละ cluster
    st.markdown("### ค่าเฉลี่ยของแต่ละตัวแปรในแต่ละกลุ่ม")
    cluster_means = df_clean.groupby('Cluster')[selected_features].mean()
    st.dataframe(cluster_means.round(2))

with tab2:
    st.subheader("📈 กราฟแสดงการจัดกลุ่ม")
    
    # ใช้ PCA เพื่อลดมิติเหลือ 2 มิติ
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    df_pca = pd.DataFrame({
        'PC1': X_pca[:, 0],
        'PC2': X_pca[:, 1],
        'Cluster': clusters
    })
    
    # Scatter plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    
    for i in range(n_clusters):
        cluster_data = df_pca[df_pca['Cluster'] == i]
        ax.scatter(cluster_data['PC1'], cluster_data['PC2'], 
                  c=colors[i % len(colors)], label=f'กลุ่ม {i}', 
                  alpha=0.6, s=50)
    
    # แสดง centroids
    centroids_pca = pca.transform(kmeans.cluster_centers_)
    ax.scatter(centroids_pca[:, 0], centroids_pca[:, 1], 
              c='black', marker='X', s=200, label='จุดศูนย์กลาง', 
              edgecolors='white', linewidth=2)
    
    ax.set_xlabel('Principal Component 1', fontsize=12)
    ax.set_ylabel('Principal Component 2', fontsize=12)
    ax.set_title('K-Means Clustering Results', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    
    st.info(f"💡 PCA อธิบายความแปรปรวนได้ {sum(pca.explained_variance_ratio_)*100:.1f}%")

with tab3:
    st.subheader("📋 ข้อมูลในแต่ละกลุ่ม")
    
    selected_cluster = st.selectbox("เลือกกลุ่มที่ต้องการดู", range(n_clusters))
    
    cluster_data = df[df_clean['Cluster'] == selected_cluster]
    
    st.markdown(f"### กลุ่มที่ {selected_cluster}")
    st.markdown(f"**จำนวนข้อมูล:** {len(cluster_data)} รายการ")
    
    # แสดงค่าเฉลี่ย
    st.markdown("### ค่าเฉลี่ยของกลุ่มนี้")
    cluster_stats = cluster_data[selected_features].describe()
    st.dataframe(cluster_stats.round(2))
    
    # แสดงข้อมูลตัวอย่าง
    st.markdown("### ข้อมูลตัวอย่าง (10 รายการแรก)")
    st.dataframe(cluster_data.head(10))
    
    # ดาวน์โหลดข้อมูลของกลุ่มนี้
    csv = cluster_data.to_csv(index=False)
    st.download_button(
        label="📥 ดาวน์โหลดข้อมูลของกลุ่มนี้",
        data=csv,
        file_name=f'cluster_{selected_cluster}.csv',
        mime='text/csv'
    )

# Footer
st.markdown("---")
st.markdown("*พัฒนาด้วย ❤️ โดยระบบ Machine Learning เพื่อการวิเคราะห์ข้อมูลการขาย*")