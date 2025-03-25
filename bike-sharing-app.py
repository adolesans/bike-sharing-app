import os
import zipfile
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
st.set_page_config(layout="wide")

st.title("🚲 Dashboard Analisis Sewa Sepeda")

# --- Download dan ekstrak data ---
url = "https://drive.google.com/uc?export=download&id=1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ"
zip_path = "Bike-sharing-dataset.zip"
response = requests.get(url)
with open(zip_path, "wb") as f:
    f.write(response.content)

extract_path = "dataset"
os.makedirs(extract_path, exist_ok=True)
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# --- Load dataset ---
csv_path = os.path.join(extract_path, 'day.csv')
df = pd.read_csv(csv_path)

# --- Data cleaning ---
df['dteday'] = pd.to_datetime(df['dteday'])
df.rename(columns={
    'dteday': 'tanggal', 'season': 'musim', 'yr': 'tahun', 'mnth': 'bulan',
    'holiday': 'hari_libur', 'weekday': 'hari_minggu', 'workingday': 'hari_kerja',
    'weathersit': 'kondisi_cuaca', 'temp': 'suhu', 'atemp': 'suhu_terasa',
    'hum': 'kelembaban', 'windspeed': 'kecepatan_angin', 'casual': 'penyewa_casual',
    'registered': 'penyewa_registered', 'cnt': 'jumlah_sewa'
}, inplace=True)

# --- Sidebar ---
st.sidebar.header("Filter")
tahun = st.sidebar.selectbox("Pilih Hari:", sorted(df['tahun'].unique()))

filtered_df = df[df['tahun'] == tahun]

# --- Sidebar Filter Interaktif ---
st.sidebar.header("Filter Data")
tahun_filter = st.sidebar.multiselect("Pilih Tahun:", sorted(df['tahun'].unique()), default=sorted(df['tahun'].unique()))
bulan_filter = st.sidebar.multiselect("Pilih Bulan:", sorted(df['bulan'].unique()), default=sorted(df['bulan'].unique()))
musim_filter = st.sidebar.multiselect("Pilih Musim:", sorted(df['musim'].unique()), default=sorted(df['musim'].unique()))
hari_kerja_filter = st.sidebar.multiselect("Pilih Hari Kerja:", sorted(df['hari_kerja'].unique()), default=sorted(df['hari_kerja'].unique()))
hari_libur_filter = st.sidebar.multiselect("Pilih Hari Libur:", sorted(df['hari_libur'].unique()), default=sorted(df['hari_libur'].unique()))
kondisi_cuaca_filter = st.sidebar.multiselect("Pilih Kondisi Cuaca:", sorted(df['kondisi_cuaca'].unique()), default=sorted(df['kondisi_cuaca'].unique()))
hari_minggu_filter = st.sidebar.multiselect("Pilih Hari Minggu:", sorted(df['hari_minggu'].unique()), default=sorted(df['hari_minggu'].unique()))

# Filter DataFrame berdasarkan pilihan pengguna
filtered_df = df[df['tahun'].isin(tahun_filter) &
                  df['bulan'].isin(bulan_filter) &
                  df['musim'].isin(musim_filter) &
                  df['hari_kerja'].isin(hari_kerja_filter) &
                  df['hari_libur'].isin(hari_libur_filter) &
                  df['kondisi_cuaca'].isin(kondisi_cuaca_filter) &
                  df['hari_minggu'].isin(hari_minggu_filter)]

# --- Pilihan Visualisasi Interaktif ---
st.sidebar.header("Pilihan Visualisasi")
plot_type = st.sidebar.selectbox("Jenis Plot:", ["Bar Chart", "Heatmap Korelasi", "Distribusi", "Box Plot"])
group_by = st.sidebar.selectbox("Kelompokkan Berdasarkan (untuk Bar Chart/Box Plot):",
                                ["Hari Kerja", "Hari Libur", "Musim", "Kondisi Cuaca", "Bulan", "Hari Minggu"])
numeric_column = st.sidebar.selectbox("Kolom Numerik (untuk Distribusi/Box Plot):",
                                     ["jumlah_sewa", "penyewa_casual", "penyewa_registered", "suhu", "suhu_terasa", "kelembaban", "kecepatan_angin"])

# --- Visualisasi jumlah sewa berdasarkan hari kerja dan hari libur ---
st.subheader("📈 Rata-rata Jumlah Sewa Berdasarkan Hari Kerja & Hari Libur")
grouped_data = filtered_df.groupby(['hari_kerja', 'hari_libur'])['jumlah_sewa'].mean().reset_index()
fig1, ax1 = plt.subplots()
sns.barplot(x='hari_kerja', y='jumlah_sewa', hue='hari_libur', data=grouped_data, ax=ax1)
ax1.set_xlabel("Hari Kerja (0=Bukan Hari Kerja, 1=Hari Kerja)")
ax1.set_ylabel("Rata-rata Jumlah Sewa Sepeda")
ax1.set_title("Pola Penyewaan Sepeda")
st.pyplot(fig1)

# --- Heatmap korelasi ---
st.subheader("🧠 Korelasi Antar Variabel")
kolom_korelasi = ['musim', 'tahun', 'bulan', 'hari_libur', 'hari_minggu', 'hari_kerja',
                  'kondisi_cuaca', 'suhu', 'suhu_terasa', 'kelembaban', 'kecepatan_angin']
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.heatmap(filtered_df[kolom_korelasi + ['jumlah_sewa']].corr(), annot=True, cmap='coolwarm', ax=ax2)
ax2.set_title("Korelasi dengan Jumlah Sewa Sepeda")
st.pyplot(fig2)

# --- Distribusi jumlah penyewa ---
st.subheader("📊 Distribusi Jumlah Sewa Sepeda")
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.histplot(filtered_df['jumlah_sewa'], kde=True, ax=ax3)
ax3.set_title("Distribusi Jumlah Sewa")
ax3.set_xlabel("Jumlah Sewa Sepeda")
st.pyplot(fig3)

# --- Kesimpulan ---
st.markdown("""
### 📌 Kesimpulan:
- Jumlah penyewa sepeda cenderung **lebih tinggi pada hari kerja**.
- **Suhu terasa** dan **suhu aktual** merupakan faktor paling berkorelasi positif terhadap jumlah penyewa.
- Semakin **tinggi kelembaban dan kecepatan angin**, semakin **rendah** jumlah penyewa.
- Kondisi cuaca yang **baik (cerah)** mendorong peningkatan peminjaman sepeda.
""")
