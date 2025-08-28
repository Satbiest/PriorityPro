import streamlit as st
import pandas as pd
import plotly.express as px

# === Page config ===
st.set_page_config(
    page_title="Ultra Cyberpunk Glow Dashboard",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === Load Data ===
try:
    df = pd.read_csv("test.csv")
except FileNotFoundError:
    st.error("File 'test.csv' tidak ditemukan. Pastikan Anda telah mengunggahnya.")
    st.stop()

# ========================
# ===== Feature Engineering =====
# ========================
def prepare_data(df):
    df = df.copy()
    df['Total_PT'] = df['Jumlah PTN'] + df['Jumlah PTS']
    df['Total_Mahasiswa'] = df['Jumlah Mahasiswa PTN'] + df['Jumlah Mahasiswa PTS']
    df['Rasio_Penduduk_Miskin'] = df['Jumlah Penduduk Miskin ( Ribu Jiwa )'] / df['Jumlah Penduduk ( Ribu Jiwa )']
    df['Mahasiswa_per_1000'] = df['Total_Mahasiswa'] / df['Jumlah Penduduk ( Ribu Jiwa )']
    df['Rata2_Tingkat_Penyelesaian'] = df[['SD / Sederajat','SMP / Sederajat','SMA / Sederajat']].mean(axis=1)
    df['Jumlah Penduduk (Juta Jiwa)'] = df['Jumlah Penduduk ( Ribu Jiwa )'] / 1000
    df['APBN (Triliun)'] = df['APBD ( Ribu Rupiah)'] / 1e9
    # Optional: Delta KPI columns
    if 'Delta_TPT' not in df.columns:
        df['Delta_TPT'] = 0
    if 'Delta_TPAK' not in df.columns:
        df['Delta_TPAK'] = 0
    return df

df = prepare_data(df)


# ========================
# ===== Cyberpunk Colors =====
# ========================
colors = {
    "bg": "#0B0F1A",
    "text": "#00FFFF",
    "primary": "#00CED1",
    "secondary": "#00BFFF",
    "accent": "#FF00FF",
    "success": "#39FF14"
}

# ========================
# ===== CSS Styling =====
# ========================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
body, h1, h2, h3, h4, h5, h6, p, span, div, th, td, label, .stDataFrame {{
    font-family: 'Poppins', sans-serif !important;
    color: {colors['text']};
    background-color: {colors['bg']};
}}
.stButton>button {{
    background-color: {colors['accent']};
    color: {colors['text']};
    font-weight: bold;
    font-family: 'Poppins', sans-serif;
}}
.kpi-card {{
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    color: {colors['text']};
    background-color: transparent;
    border: 2px solid {colors['primary']};
    box-shadow: 0 0 15px {colors['primary']}, 0 0 30px {colors['secondary']};
    transition: all 0.3s ease-in-out;
    margin: 10px;
    cursor: default;
}}
.kpi-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 0 30px {colors['secondary']}, 0 0 50px {colors['primary']};
    filter: brightness(1.3);
}}
.kpi-title {{
    font-size: 18px;
    font-weight: 600;
}}
.kpi-value {{
    font-size: 28px;
    font-weight: 700;
    color: {colors['accent']};
}}
.delta-kpi-card {{
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    color: {colors['text']};
    background-color: transparent;
    font-family: 'Poppins', sans-serif;
    transition: all 0.3s ease-in-out;
    margin: 10px;
    cursor: default;
}}
.delta-kpi-card.positive {{
    border: 2px solid {colors['success']};
    box-shadow: 0 0 15px {colors['success']}, 0 0 30px {colors['success']};
}}
.delta-kpi-card.negative {{
    border: 2px solid {colors['accent']};
    box-shadow: 0 0 15px {colors['accent']}, 0 0 30px {colors['accent']};
}}
.delta-kpi-title {{
    font-size: 18px;
    font-weight: 600;
}}
.delta-kpi-value {{
    font-size: 28px;
    font-weight: 700;
}}
@keyframes neonBlink {{
    0% {{ box-shadow: 0 0 10px {colors['primary']}, 0 0 20px {colors['secondary']}, 0 0 30px {colors['accent']}; }}
    50% {{ box-shadow: 0 0 20px {colors['primary']}, 0 0 40px {colors['secondary']}, 0 0 60px {colors['accent']}; }}
    100% {{ box-shadow: 0 0 10px {colors['primary']}, 0 0 20px {colors['secondary']}, 0 0 30px {colors['accent']}; }}
}}
.neon-table-wrapper {{
    display: block;
    width: 100%;
    overflow-x: auto;
    padding: 16px;
    border-radius: 15px;
    margin-bottom: 20px;
    border: 2px solid {colors['primary']};
    box-sizing: border-box;
    background-color: transparent;
    animation: neonBlink 1.5s infinite;
}}
.neon-table {{
    border-collapse: collapse;
    width: 100%;
    table-layout: auto;
    font-family: 'Poppins', sans-serif;
    border-radius: 12px;
    overflow: hidden;
}}
.neon-table th {{
    padding: 12px;
    background-color: #111827;
    color: {colors['text']};
    font-weight: 600;
    text-align: center;
    text-shadow: 0 0 6px {colors['text']}, 0 0 12px {colors['primary']};
    border: 1px solid {colors['secondary']};
}}
.neon-table td {{
    padding: 10px;
    background-color: #0b1424;
    color: {colors['primary']};
    text-align: center;
    border: 1px solid {colors['secondary']};
    box-shadow: inset 0 0 8px {colors['primary']};
    transition: all 0.2s;
    white-space: nowrap;
}}
.neon-table td:hover {{
    color: {colors['accent']};
    text-shadow: 0 0 6px {colors['accent']}, 0 0 10px {colors['primary']};
    background-color: #1E2A44;
}}
</style>
""", unsafe_allow_html=True)

# ========================
# ===== Sidebar Navigation =====
# ========================
st.sidebar.title("🌌 Navigation")
page = st.sidebar.radio("Select Page", ["Home Dashboard", "Page Analysis"])
if 'selected_prov' not in st.session_state:
    st.session_state.selected_prov = "All"

# ========================
# ===== Functions =====
# ========================
def render_kpi_cards(kpi_data):
    for row in range(2):
        cols = st.columns(3)
        for i in range(3):
            kpi = kpi_data[row*3 + i]
            val_display = kpi.get("display", kpi['value'])
            with cols[i]:
                st.markdown(f"""
                <div class="kpi-card">
                    <div style="font-size:28px;">{kpi['icon']}</div>
                    <div class="kpi-title">{kpi['title']}</div>
                    <div class="kpi-value">{val_display}</div>
                </div>
                """, unsafe_allow_html=True)

def render_delta_kpi(delta_kpis):
    if not delta_kpis:
        return
    st.subheader("📈 Delta Metrics (Neon Glow)")
    cols = st.columns(len(delta_kpis))
    for i, kpi in enumerate(delta_kpis):
        val_display = kpi.get("display", f"{kpi['value']:.2f}")
        glow_class = "positive" if kpi['value'] >= 0 else "negative"
        with cols[i]:
            st.markdown(f"""
            <div class="delta-kpi-card {glow_class}">
                <div style="font-size:28px;">{kpi['icon']}</div>
                <div class="delta-kpi-title">{kpi['title']}</div>
                <div class="delta-kpi-value">{val_display}</div>
            </div>
            """, unsafe_allow_html=True)

def render_neon_table(df, columns_display):
    formatted_df = df[columns_display].copy()
    formatted_df['Jumlah Penduduk (Juta Jiwa)'] = formatted_df['Jumlah Penduduk (Juta Jiwa)'].apply(lambda x: f"{x:.2f}")
    formatted_df['Rasio_Penduduk_Miskin'] = formatted_df['Rasio_Penduduk_Miskin'].apply(lambda x: f"{x*100:.2f}%")
    formatted_df['APBN (Triliun)'] = formatted_df['APBN (Triliun)'].apply(lambda x: f"{x:.2f}")
    formatted_df['Total_PT'] = formatted_df['Total_PT'].apply(lambda x: f"{int(x)}")
    formatted_df['Total_Mahasiswa'] = formatted_df['Total_Mahasiswa'].apply(lambda x: f"{int(x):,}".replace(",", "."))
    formatted_df['Rata2_Tingkat_Penyelesaian'] = formatted_df['Rata2_Tingkat_Penyelesaian'].apply(lambda x: f"{x:.2f}")
    formatted_df['Mahasiswa_per_1000'] = formatted_df['Mahasiswa_per_1000'].apply(lambda x: f"{x:.2f}")

    table_html = '<div class="neon-table-wrapper">'
    table_html += '<table class="neon-table">'
    table_html += '<thead><tr>'
    for col in formatted_df.columns:
        table_html += f'<th>{col}</th>'
    table_html += '</tr></thead>'
    table_html += '<tbody>'
    for _, row in formatted_df.iterrows():
        table_html += '<tr>'
        for val in row:
            table_html += f'<td>{val}</td>'
        table_html += '</tr>'
    table_html += '</tbody></table></div>'
    st.markdown(table_html, unsafe_allow_html=True)

# ========================
# ===== HOME DASHBOARD =====
# ========================
if page == "Home Dashboard":
    st.title("Pemantauan Analisis Kondisi Sosial Ekonomi Wilayah di Indonesia ")

    prov_list = ["All"] + df['Provinsi'].tolist()
    prov_select = st.selectbox("Filter Provinsi", prov_list)
    st.session_state.selected_prov = prov_select
    df_filtered = df if prov_select == "All" else df[df['Provinsi'] == prov_select]

    kpi_data = [
    {"title": "Jumlah Penduduk (Juta Jiwa)", "value": df_filtered['Jumlah Penduduk (Juta Jiwa)'].sum(),
     "display": f"{df_filtered['Jumlah Penduduk (Juta Jiwa)'].sum():.2f}", "icon":"👥"},
    {"title": "Rasio Penduduk Miskin", "value": df_filtered['Rasio_Penduduk_Miskin'].mean(),
     "display": f"{df_filtered['Rasio_Penduduk_Miskin'].mean()*100:.2f}%", "icon":"💸"},
    {"title": "Total APBN (Triliun)", "value": df_filtered['APBN (Triliun)'].sum(),
     "display": f"{df_filtered['APBN (Triliun)'].sum():.2f}", "icon":"🏦"},
    {"title": "Jumlah PT", "value": df_filtered['Total_PT'].sum(),
     "display": f"{int(df_filtered['Total_PT'].sum())}", "icon":"🎓"},
    {"title": "Jumlah Mahasiswa", "value": df_filtered['Total_Mahasiswa'].sum(),
     "display": f"{int(df_filtered['Total_Mahasiswa'].sum()):,}".replace(",", "."), "icon":"🧑‍🎓"},
    {"title": "Mahasiswa per 1000", "value": df_filtered['Mahasiswa_per_1000'].mean(),
     "display": f"{df_filtered['Mahasiswa_per_1000'].mean():.2f}", "icon":"📊"}
]

    render_kpi_cards(kpi_data)

    

    # Delta KPI
    delta_kpis = []
    if prov_select != "All":
        delta_kpis = [
            {"title": "Delta TPT", "value": df_filtered['Delta_TPT'].iloc[0],
             "display": f"{df_filtered['Delta_TPT'].iloc[0]:.2f}",
             "icon":"▲" if df_filtered['Delta_TPT'].iloc[0]>=0 else "▼"},
            {"title": "Delta TPAK", "value": df_filtered['Delta_TPAK'].iloc[0],
             "display": f"{df_filtered['Delta_TPAK'].iloc[0]:.2f}",
             "icon":"▲" if df_filtered['Delta_TPAK'].iloc[0]>=0 else "▼"}
        ]
    render_delta_kpi(delta_kpis)
    

    st.markdown("---")
    st.subheader(f"Detail Provinsi {'- ' + prov_select if prov_select != 'All' else ''}")

    display_cols = [
        'Provinsi', 'Jumlah Penduduk (Juta Jiwa)', 'Rasio_Penduduk_Miskin',
        'APBN (Triliun)', 'Realisasi Anggaran Pendidikan ( % )',
        'Rata2_Tingkat_Penyelesaian', 'Total_PT', 'Total_Mahasiswa',
        'Mahasiswa_per_1000'
    ]
    render_neon_table(df_filtered, display_cols)

# =========================
# ===== PAGE ANALYSIS =====
# =========================
# =========================
# ===== PAGE ANALYSIS =====
# =========================
if page == "Page Analysis":
    st.title("Analsis Lanjutan Provinsi Indonesia")
    df_filtered = df if st.session_state.selected_prov=="All" else df[df['Provinsi']==st.session_state.selected_prov]

    neon_layout = dict(
        plot_bgcolor=colors['bg'],
        paper_bgcolor=colors['bg'],
        font_color=colors['text'],
        font=dict(family="Poppins")
    )

    # === Mapping Provinsi ke Pulau ===
    pulau_map = {
        # Sumatera
        "Aceh":"Sumatera","Sumatera Utara":"Sumatera","Sumatera Barat":"Sumatera",
        "Riau":"Sumatera","Jambi":"Sumatera","Sumatera Selatan":"Sumatera",
        "Bengkulu":"Sumatera","Lampung":"Sumatera",
        "Kepulauan Bangka Belitung":"Sumatera","Kepulauan Riau":"Sumatera",

        # Jawa
        "DKI Jakarta":"Jawa","Jawa Barat":"Jawa","Jawa Tengah":"Jawa",
        "DI Yogyakarta":"Jawa","Jawa Timur":"Jawa","Banten":"Jawa",

        # Bali & Nusa Tenggara
        "Bali":"Bali & NTT NTB","Nusa Tenggara Barat":"Bali & NTT NTB","Nusa Tenggara Timur":"Bali & NTT NTB",

        # Kalimantan
        "Kalimantan Barat":"Kalimantan","Kalimantan Tengah":"Kalimantan",
        "Kalimantan Selatan":"Kalimantan","Kalimantan Timur":"Kalimantan","Kalimantan Utara":"Kalimantan",

        # Sulawesi
        "Sulawesi Utara":"Sulawesi","Sulawesi Tengah":"Sulawesi","Sulawesi Selatan":"Sulawesi",
        "Sulawesi Tenggara":"Sulawesi","Gorontalo":"Sulawesi","Sulawesi Barat":"Sulawesi",

        # Maluku
        "Maluku":"Maluku","Maluku Utara":"Maluku",

        # Papua
        "Papua":"Papua","Papua Barat":"Papua","Papua Selatan":"Papua",
        "Papua Tengah":"Papua","Papua Pegunungan":"Papua","Papua Barat Daya":"Papua"
    }

    df['Pulau'] = df['Provinsi'].map(pulau_map)

    # === Bar Chart PTN vs PTS per Pulau ===
    st.markdown("<h3 style='color:#00BFFF;'>Jumlah PTN vs PTS per Pulau</h3>", unsafe_allow_html=True)
    pulau_df = df.groupby('Pulau')[['Jumlah PTN','Jumlah PTS']].sum().reset_index()
    pulau_melt = pulau_df.melt(id_vars='Pulau', var_name='Jenis_PT', value_name='Jumlah')

    fig_bar_pulau = px.bar(
        pulau_melt, x='Pulau', y='Jumlah', color='Jenis_PT', barmode='group', text='Jumlah',
        color_discrete_map={"Jumlah PTN": colors['secondary'], "Jumlah PTS": colors['accent']}
    )
    fig_bar_pulau.update_layout(**neon_layout)
    st.plotly_chart(fig_bar_pulau, use_container_width=True)

    # === Scatter Plot 1: APBN vs Rasio Penduduk Miskin ===
    st.markdown("<h3 style='color:#00BFFF;'>APBN vs Rasio Penduduk Miskin</h3>", unsafe_allow_html=True)
    fig_scatter1 = px.scatter(
        df, x='APBN (Triliun)', y='Rasio_Penduduk_Miskin', hover_name='Provinsi',
        size='Jumlah Penduduk (Juta Jiwa)', color='Rasio_Penduduk_Miskin',
        color_continuous_scale=[colors['primary'], colors['secondary']]
    )
    fig_scatter1.update_layout(**neon_layout)
    st.plotly_chart(fig_scatter1, use_container_width=True)

    # === Scatter Plot 2: Pendidikan vs Tingkat Penyelesaian ===
    st.markdown("<h3 style='color:#00BFFF;'>Realisasi Anggaran Pendidikan (%) vs Rata-rata Tingkat Penyelesaian</h3>", unsafe_allow_html=True)
    fig_scatter2 = px.scatter(
        df, x='Realisasi Anggaran Pendidikan ( % )', y='Rata2_Tingkat_Penyelesaian',
        hover_name='Provinsi', size='Total_Mahasiswa', color='Rata2_Tingkat_Penyelesaian',
        color_continuous_scale=[colors['accent'], colors['secondary']]
    )
    fig_scatter2.update_layout(**neon_layout)
    st.plotly_chart(fig_scatter2, use_container_width=True)


