import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="K-Means Clustering", page_icon="🎯", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🎯 K-Means Clustering - จัดกลุ่มข้อมูลการขาย</p>', unsafe_allow_html=True)
st.markdown("### วิเคราะห์และจัดกลุ่มข้อมูลการขายด้วยอัลกอริทึม K-Means")
st.markdown("---")

# ============================================================
# โหลดและทำความสะอาดข้อมูล
# ============================================================
@st.cache_data
def load_and_clean_data():
    csv_path = "mall_sales_eda_3000_records.csv"
    if not os.path.exists(csv_path):
        return None
    
    df = pd.read_csv(csv_path)
    
    # ทำความสะอาดตัวเลขที่มี comma
    cols_to_clean = ['sales_amount', 'cost_amount', 'gross_profit', 'avg_price_per_unit']
    for col in cols_to_clean:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '', regex=False).astype(float)
    
    # ทำความสะอาด discount_rate
    if 'discount_rate' in df.columns:
        df['discount_rate'] = df['discount_rate'].astype(str).str.replace('%', '', regex=False).astype(float)
    
    # แปลง boolean
    bool_cols = ['is_weekend', 'returned']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].map({'TRUE': 1, 'FALSE': 0, True: 1, False: 0}).astype(int)
    
    return df

df = load_and_clean_data()

if df is None:
    st.error("❌ ไม่พบไฟล์ `mall_sales_eda_3000_records.csv` ในโฟลเดอร์โปรเจกต์!")
    st.stop()

# ============================================================
# Sidebar - ตั้งค่า
# ============================================================
st.sidebar.header("⚙️ ตั้งค่า K-Means")
st.sidebar.markdown("---")

# เลือกจำนวน clusters
n_clusters = st.sidebar.slider("จำนวนกลุ่ม (Clusters)", 2, 10, 4, 
                                help="เลือกจำนวนกลุ่มที่ต้องการจัด")

# เลือก features
st.sidebar.subheader("เลือกตัวแปร")
available_features = [
    'customers_count', 'employee_count', 'units_sold',
    'avg_price_per_unit', 'discount_rate', 'sales_amount',
    'cost_amount', 'gross_profit', 'satisfaction_score'
]

selected_features = st.sidebar.multiselect(
    "เลือกตัวแปร (อย่างน้อย 2 ตัว)",
    available_features,
    default=['customers_count', 'units_sold', 'sales_amount']
)

if len(selected_features) < 2:
    st.warning("⚠️ โปรดเลือกอย่างน้อย 2 ตัวแปร")
    st.stop()

# ============================================================
# ทำ K-Means แบบ Real-time
# ============================================================
X = df[selected_features].copy()
X = X.fillna(X.median())

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train K-Means
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)
df['Cluster'] = clusters

st.success(f"✅ จัดกลุ่มข้อมูลเสร็จสิ้น! พบ {n_clusters} กลุ่ม จากข้อมูล {len(df)} รายการ")

# ============================================================
# Tabs สำหรับแสดงผล
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 ภาพรวม", 
    "📈 กราฟ PCA", 
    " ข้อมูลแต่ละกลุ่ม",
    " ตารางข้อมูล"
])

# ============================================================
# TAB 1: ภาพรวม
# ============================================================
with tab1:
    st.subheader(" ภาพรวมของแต่ละกลุ่ม")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### จำนวนข้อมูลในแต่ละกลุ่ม")
        cluster_counts = df['Cluster'].value_counts().sort_index()
        st.bar_chart(cluster_counts)
    
    with col2:
        st.markdown("### สัดส่วนของแต่ละกลุ่ม")
        fig, ax = plt.subplots(figsize=(6, 6))
        colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))
        ax.pie(cluster_counts, labels=[f'กลุ่ม {i}' for i in cluster_counts.index], 
               autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')
        st.pyplot(fig)
    
    st.markdown("---")
    st.subheader("📊 ค่าเฉลี่ยของแต่ละตัวแปรในแต่ละกลุ่ม")
    
    # แปลงค่าทั้งหมดเป็น string เพื่อป้องกัน PyArrow Error
    cluster_means = df.groupby('Cluster')[selected_features].mean().round(2)
    cluster_means_str = cluster_means.astype(str)
    
    st.dataframe(cluster_means_str, width="stretch")

# ============================================================
# TAB 2: กราฟ PCA
# ============================================================
with tab2:
    st.subheader("📈 การแสดงผลแบบ PCA (2 มิติ)")
    
    # ใช้ PCA ลดมิติเหลือ 2 มิติ
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    
    df_pca = pd.DataFrame({
        'PC1': X_pca[:, 0],
        'PC2': X_pca[:, 1],
        'Cluster': clusters
    })
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))
    
    for i in range(n_clusters):
        cluster_data = df_pca[df_pca['Cluster'] == i]
        ax.scatter(cluster_data['PC1'], cluster_data['PC2'], 
                  c=[colors[i]], label=f'กลุ่ม {i}', 
                  alpha=0.6, s=80, edgecolors='k', linewidth=0.5)
    
    # แสดง centroids
    centroids_pca = pca.transform(kmeans.cluster_centers_)
    ax.scatter(centroids_pca[:, 0], centroids_pca[:, 1], 
              c='red', marker='X', s=300, label='จุดศูนย์กลาง', 
              edgecolors='black', linewidth=2, zorder=5)
    
    ax.set_xlabel(f'Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', fontsize=12)
    ax.set_ylabel(f'Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', fontsize=12)
    ax.set_title(f'K-Means Clustering Results (k={n_clusters})', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    
    st.info(f"💡 PCA อธิบายความแปรปรวนได้ {sum(pca.explained_variance_ratio_)*100:.1f}% ของข้อมูลทั้งหมด")

# ============================================================
# TAB 3: ข้อมูลแต่ละกลุ่ม
# ============================================================
with tab3:
    st.subheader("🔍 วิเคราะห์แต่ละกลุ่ม")
    
    selected_cluster = st.selectbox("เลือกกลุ่มที่ต้องการดู", range(n_clusters))
    
    cluster_data = df[df['Cluster'] == selected_cluster]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("จำนวนข้อมูล", f"{len(cluster_data)} รายการ")
        st.metric("สัดส่วน", f"{len(cluster_data)/len(df)*100:.1f}%")
    
    with col2:
        st.metric("ค่าเฉลี่ยยอดขาย", f"฿ {cluster_data['sales_amount'].mean():,.2f}")
        st.metric("ค่าเฉลี่ยความพึงพอใจ", f"{cluster_data['satisfaction_score'].mean():.2f}")
    
    st.markdown("---")
    st.markdown(f"###  ค่าสถิติของกลุ่มที่ {selected_cluster}")
    
    # แปลงเป็น string เพื่อป้องกัน PyArrow Error
    cluster_stats = cluster_data[selected_features].describe().round(2).astype(str)
    st.dataframe(cluster_stats, width="stretch")
    
    st.markdown("---")
    st.markdown(f"###  ข้อมูลตัวอย่าง (10 รายการแรก)")
    
    sample_data = cluster_data.head(10).copy()
    # แปลงคอลัมน์ตัวเลขเป็น string
    for col in sample_data.select_dtypes(include=[np.number]).columns:
        sample_data[col] = sample_data[col].astype(str)
    
    st.dataframe(sample_data, width="stretch")

# ============================================================
# TAB 4: ตารางข้อมูลทั้งหมด
# ============================================================
with tab4:
    st.subheader("📋 ตารางข้อมูลทั้งหมด")
    
    # เลือกคอลัมน์ที่จะแสดง
    display_cols = st.multiselect(
        "เลือกคอลัมน์ที่ต้องการแสดง",
        df.columns.tolist(),
        default=['Cluster'] + selected_features
    )
    
    if display_cols:
        display_df = df[display_cols].copy()
        # แปลงคอลัมน์ตัวเลขเป็น string
        for col in display_df.select_dtypes(include=[np.number]).columns:
            display_df[col] = display_df[col].astype(str)
        
        st.dataframe(display_df, width="stretch")
        
        # ปุ่มดาวน์โหลด
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 ดาวน์โหลดข้อมูลทั้งหมด (CSV)",
            data=csv,
            file_name='mall_sales_with_clusters.csv',
            mime='text/csv'
        )

# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.markdown("*พัฒนาด้วย ❤️ โดยระบบ Machine Learning เพื่อการวิเคราะห์ข้อมูลการขาย*")