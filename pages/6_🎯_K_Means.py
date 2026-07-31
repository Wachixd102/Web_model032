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

st.markdown('<p class="main-header"> K-Means Clustering</p>', unsafe_allow_html=True)
st.markdown("### จัดกลุ่มข้อมูลการขายด้วย K-Means Clustering")
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
    st.error("❌ ไม่พบไฟล์ `mall_sales_eda_3000_records.csv`!")
    st.stop()

# ============================================================
# Sidebar
# ============================================================
st.sidebar.header("⚙️ Settings")
st.sidebar.markdown("---")

n_clusters = st.sidebar.slider("Number of Clusters (k)", 2, 10, 4)

st.sidebar.subheader("Select Features")
available_features = [
    'customers_count', 'employee_count', 'units_sold',
    'avg_price_per_unit', 'discount_rate', 'sales_amount',
    'cost_amount', 'gross_profit', 'satisfaction_score'
]

selected_features = st.sidebar.multiselect(
    "Choose features (min 2)",
    available_features,
    default=['customers_count', 'units_sold', 'sales_amount']
)

if len(selected_features) < 2:
    st.warning("⚠️ Please select at least 2 features")
    st.stop()

# ============================================================
# K-Means Clustering (Real-time)
# ============================================================
X = df[selected_features].copy()
X = X.fillna(X.median())

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10, max_iter=300)
clusters = kmeans.fit_predict(X_scaled)
df['Cluster'] = clusters

st.success(f"✅ Clustering complete! Found {n_clusters} clusters from {len(df)} records")

# ============================================================
# Tabs
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", 
    "📈 PCA Visualization", 
    "🔍 Cluster Details",
    "📋 Data Table"
])

# ============================================================
# TAB 1: Overview
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
    
    st.dataframe(cluster_means_display, width="stretch")

# ============================================================
# TAB 2: PCA Visualization
# ============================================================
with tab2:
    st.subheader(" PCA 2D Visualization")
    
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
# TAB 3: Cluster Details
# ============================================================
with tab3:
    st.subheader("🔍 Cluster Analysis")
    
    selected_cluster = st.selectbox("Select Cluster", range(n_clusters))
    
    cluster_data = df[df['Cluster'] == selected_cluster]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Records", f"{len(cluster_data)}")
    with col2:
        st.metric("Percentage", f"{len(cluster_data)/len(df)*100:.1f}%")
    with col3:
        if 'sales_amount' in cluster_data.columns:
            st.metric("Avg Sales", f"฿{cluster_data['sales_amount'].mean():,.0f}")
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
    
    st.dataframe(cluster_stats_display, width="stretch")
    
    st.markdown("---")
    st.markdown(f"### 📋 Sample Data (First 10)")
    
    sample_data = cluster_data[selected_features + ['Cluster']].head(10).copy()
    
    # แก้ PyArrow Error: แปลงทุกคอลัมน์เป็น string
    for col in sample_data.columns:
        sample_data[col] = sample_data[col].astype(str)
    
    st.dataframe(sample_data, width="stretch")

# ============================================================
# TAB 4: Data Table
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
        
        st.dataframe(display_df, width="stretch")
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name='mall_sales_with_clusters.csv',
            mime='text/csv'
        )

# Footer
st.markdown("---")
st.markdown("*Developed with ❤️ using K-Means Clustering*")