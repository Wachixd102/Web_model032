import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="K-Means Clustering", page_icon="🎯", layout="wide")

st.markdown("# 🎯 K-Means Clustering")
st.markdown("### จัดกลุ่มข้อมูลด้วย K-Means Clustering")
st.markdown("---")

# ============================================================
# ส่วนที่ 1: อัปโหลดไฟล์
# ============================================================
st.subheader("📤 Step 1: Upload CSV File")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=['csv'],
    help="Upload CSV file for clustering analysis"
)

if uploaded_file is None:
    st.info("👆 Please upload a CSV file to start analysis")
    st.markdown("""
    ###  Supported Files:
    - `mall_sales_eda_3000_records.csv`
    - Any CSV file with numeric columns
    
    ### 💡 Tips:
    - File should have at least 2 numeric columns
    - System will auto-clean data (remove commas, %)
    """)
    st.stop()

# ============================================================
# ส่วนที่ 2: โหลดและทำความสะอาดข้อมูล
# ============================================================
@st.cache_data
def load_and_clean_data(file):
    df = pd.read_csv(file)
    
    # ทำความสะอาดตัวเลขที่มี comma
    cols_to_clean = ['sales_amount', 'cost_amount', 'gross_profit', 'avg_price_per_unit']
    for col in cols_to_clean:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(',', '', regex=False),
                errors='coerce'
            )
    
    # ทำความสะอาด discount_rate
    if 'discount_rate' in df.columns:
        df['discount_rate'] = pd.to_numeric(
            df['discount_rate'].astype(str).str.replace('%', '', regex=False),
            errors='coerce'
        )
    
    # แปลง boolean
    bool_cols = ['is_weekend', 'returned']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].map({'TRUE': 1, 'FALSE': 0, True: 1, False: 0})
    
    return df

df = load_and_clean_data(uploaded_file)

st.success(f"✅ File loaded successfully! Found {len(df)} rows, {len(df.columns)} columns")

# ============================================================
# ส่วนที่ 3: แสดงข้อมูลตัวอย่าง
# ============================================================
with st.expander("🔍 View Sample Data"):
    st.dataframe(df.head(10), use_container_width=True)
    st.markdown(f"**Total:** {len(df)} rows, {len(df.columns)} columns")

# ============================================================
# ส่วนที่ 4: เลือก Features
# ============================================================
st.subheader("⚙️ Step 2: Configure Analysis")

col1, col2 = st.columns(2)

with col1:
    n_clusters = st.slider("Number of Clusters (k)", 2, 10, 4, 
                            help="Select number of clusters")

with col2:
    # เลือกเฉพาะคอลัมน์ตัวเลข
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # กรองคอลัมน์ที่เหมาะสม
    exclude_cols = ['record_id', 'ID', 'id']
    available_features = [c for c in numeric_cols if c not in exclude_cols]
    
    selected_features = st.multiselect(
        "Select Features (min 2)",
        available_features,
        default=available_features[:3] if len(available_features) >= 3 else available_features[:2]
    )

if len(selected_features) < 2:
    st.warning("⚠️ Please select at least 2 features")
    st.stop()

# ============================================================
# ส่วนที่ 5: ทำ K-Means
# ============================================================
X = df[selected_features].copy()
X = X.fillna(X.median())

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train K-Means
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10, max_iter=300)
clusters = kmeans.fit_predict(X_scaled)
df['Cluster'] = clusters

st.success(f"✅ Clustering complete! Found {n_clusters} clusters from {len(df)} records")

# ============================================================
# ส่วนที่ 6: แสดงผล (Tabs)
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    " Overview", 
    "📈 PCA Visualization", 
    "🔍 Cluster Details",
    "📋 Data Table"
])

# ============================================================
# TAB 1: ภาพรวม
# ============================================================
with tab1:
    st.subheader("📊 Cluster Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Records per Cluster")
        cluster_counts = df['Cluster'].value_counts().sort_index()
        st.bar_chart(cluster_counts)
    
    with col2:
        st.markdown("### Cluster Distribution")
        fig, ax = plt.subplots(figsize=(6, 6))
        colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))
        ax.pie(cluster_counts, 
               labels=[f'Cluster {i}' for i in cluster_counts.index], 
               autopct='%1.1f%%', 
               startangle=90, 
               colors=colors)
        ax.axis('equal')
        st.pyplot(fig)
    
    st.markdown("---")
    st.subheader("📊 Mean Values per Cluster")
    
    cluster_means = df.groupby('Cluster')[selected_features].mean().round(2)
    
    # แก้ PyArrow Error: แปลงทุกคอลัมน์เป็น string
    cluster_means_display = cluster_means.copy()
    for col in cluster_means_display.columns:
        cluster_means_display[col] = cluster_means_display[col].astype(str)
    
    st.dataframe(cluster_means_display, use_container_width=True)

# ============================================================
# TAB 2: กราฟ PCA
# ============================================================
with tab2:
    st.subheader("📈 PCA 2D Visualization")
    
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
                  c=[colors[i]], 
                  label=f'Cluster {i}', 
                  alpha=0.6, s=80, edgecolors='black', linewidth=0.5)
    
    # แสดง centroids
    centroids_pca = pca.transform(kmeans.cluster_centers_)
    ax.scatter(centroids_pca[:, 0], centroids_pca[:, 1], 
              c='red', marker='X', s=300, 
              label='Centroids', 
              edgecolors='black', linewidth=2, zorder=5)
    
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', fontsize=12)
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', fontsize=12)
    ax.set_title(f'K-Means Clustering (k={n_clusters})', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    
    st.info(f"💡 PCA explains {sum(pca.explained_variance_ratio_)*100:.1f}% of variance")

# ============================================================
# TAB 3: ข้อมูลแต่ละกลุ่ม
# ============================================================
with tab3:
    st.subheader(" Cluster Analysis")
    
    selected_cluster = st.selectbox("Select Cluster", range(n_clusters))
    
    cluster_data = df[df['Cluster'] == selected_cluster]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Records", f"{len(cluster_data)}")
    with col2:
        st.metric("Percentage", f"{len(cluster_data)/len(df)*100:.1f}%")
    with col3:
        if 'sales_amount' in cluster_data.columns:
            st.metric("Avg Sales", f"${cluster_data['sales_amount'].mean():,.0f}")
    with col4:
        if 'satisfaction_score' in cluster_data.columns:
            st.metric("Avg Satisfaction", f"{cluster_data['satisfaction_score'].mean():.2f}")
    
    st.markdown("---")
    st.markdown(f"### 📊 Statistics for Cluster {selected_cluster}")
    
    cluster_stats = cluster_data[selected_features].describe().round(2)
    
    # แก้ PyArrow Error
    cluster_stats_display = cluster_stats.copy()
    for col in cluster_stats_display.columns:
        cluster_stats_display[col] = cluster_stats_display[col].astype(str)
    
    st.dataframe(cluster_stats_display, use_container_width=True)
    
    st.markdown("---")
    st.markdown(f"###  Sample Data (First 10)")
    
    sample_data = cluster_data[selected_features + ['Cluster']].head(10).copy()
    
    # แก้ PyArrow Error: แปลงทุกคอลัมน์เป็น string
    for col in sample_data.columns:
        sample_data[col] = sample_data[col].astype(str)
    
    st.dataframe(sample_data, use_container_width=True)

# ============================================================
# TAB 4: ตารางข้อมูล
# ============================================================
with tab4:
    st.subheader("📋 Full Data Table")
    
    display_cols = st.multiselect(
        "Select columns to display",
        df.columns.tolist(),
        default=['Cluster'] + selected_features
    )
    
    if display_cols:
        display_df = df[display_cols].copy()
        
        # แก้ PyArrow Error: แปลงทุกคอลัมน์เป็น string
        for col in display_df.columns:
            display_df[col] = display_df[col].astype(str)
        
        st.dataframe(display_df, use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV with Cluster Labels",
            data=csv,
            file_name='data_with_clusters.csv',
            mime='text/csv'
        )

# Footer
st.markdown("---")
st.markdown("*Developed with ❤️ using K-Means Clustering*")