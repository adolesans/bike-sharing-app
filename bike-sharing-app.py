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

# --- nilai numerik menjadi nama ---
musim_map = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
bulan_map = {1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
             7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"}
hari_minggu_map = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}
hari_kerja_map = {0: "Bukan Hari Kerja", 1: "Hari Kerja"}
hari_libur_map = {0: "Bukan Hari Libur", 1: "Hari Libur"}
kondisi_cuaca_map = {1: "Cerah", 2: "Kabut/Berawan", 3: "Hujan Ringan/Salju Ringan", 4: "Hujan Lebat/Salju Lebat"}
tahun_map = {0: "2011", 1: "2012"}

# --- Sidebar ---
st.sidebar.header("Filter")
tahun = st.sidebar.selectbox("Pilih Hari:", sorted(df['tahun'].unique()))

filtered_df = df[df['tahun'] == tahun]

# --- Sidebar Filter ---
st.sidebar.header("Filter Data")
tahun_filter = st.sidebar.multiselect("Pilih Tahun:", sorted(df['tahun'].unique()), default=sorted(df['tahun'].unique()), format_func=lambda x: tahun_map.get(x, str(x)))
bulan_filter = st.sidebar.multiselect("Pilih Bulan:", sorted(df['bulan'].unique()), default=sorted(df['bulan'].unique()), format_func=lambda x: bulan_map.get(x, str(x)))
musim_filter = st.sidebar.multiselect("Pilih Musim:", sorted(df['musim'].unique()), default=sorted(df['musim'].unique()), format_func=lambda x: musim_map.get(x, str(x)))
hari_kerja_filter = st.sidebar.multiselect("Pilih Hari Kerja:", sorted(df['hari_kerja'].unique()), default=sorted(df['hari_kerja'].unique()), format_func=lambda x: hari_kerja_map.get(x, str(x)))
hari_libur_filter = st.sidebar.multiselect("Pilih Hari Libur:", sorted(df['hari_libur'].unique()), default=sorted(df['hari_libur'].unique()), format_func=lambda x: hari_libur_map.get(x, str(x)))
kondisi_cuaca_filter = st.sidebar.multiselect("Pilih Kondisi Cuaca:", sorted(df['kondisi_cuaca'].unique()), default=sorted(df['kondisi_cuaca'].unique()), format_func=lambda x: kondisi_cuaca_map.get(x, str(x)))
hari_minggu_filter = st.sidebar.multiselect("Pilih Hari Minggu:", sorted(df['hari_minggu'].unique()), default=sorted(df['hari_minggu'].unique()), format_func=lambda x: hari_minggu_map.get(x, str(x)))

# Filter DataFrame berdasarkan pilihan pengguna
filtered_df = df[df['tahun'].isin(tahun_filter) &
                  df['bulan'].isin(bulan_filter) &
                  df['musim'].isin(musim_filter) &
                  df['hari_kerja'].isin(hari_kerja_filter) &
                  df['hari_libur'].isin(hari_libur_filter) &
                  df['kondisi_cuaca'].isin(kondisi_cuaca_filter) &
                  df['hari_minggu'].isin(hari_minggu_filter)]

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

st.sidebar.header("Analisis & Insight")

st.sidebar.subheader("Pola Penyewaan")
if st.sidebar.checkbox("Tampilkan Insight Pola Penyewaan"):
    st.sidebar.markdown("""
    - **Hari Kerja Tinggi:** Menunjukkan penggunaan utama untuk transportasi rutin.
    - **Hari Libur Bervariasi:** Mengindikasikan penggunaan untuk rekreasi atau aktivitas santai.
    """)

st.sidebar.subheader("Faktor Utama")
if st.sidebar.checkbox("Tampilkan Insight Faktor Utama"):
    st.sidebar.markdown("""
    - **Suhu Nyaman:** Meningkatkan jumlah penyewa.
    - **Cuaca Baik:** Mendorong penyewaan.
    - **Angin Kencang:** Mengurangi penyewaan.
    - **Tren Positif:** Peningkatan penyewa dari waktu ke waktu.
    """)

st.sidebar.subheader("Rekomendasi Strategis")
if st.sidebar.checkbox("Tampilkan Rekomendasi"):
    st.sidebar.markdown("""
    - **Optimalkan Ketersediaan Hari Kerja.**
    - **Adakan Promosi Hari Libur.**
    - **Adaptasi Layanan dengan Cuaca.**
    """)
