import streamlit as st
import pandas as pd
import seaborn as sns
import requests
import os

# Fungsi untuk mengunduh dan memuat data
def load_data():
    github_raw_url = "https://raw.githubusercontent.com/adolesans/bike-sharing-app/main/combined-dataset.csv"  # URL mentah ke dataset Anda
    csv_filename = "dataset.csv"

    if not os.path.exists(csv_filename):
        response = requests.get(github_raw_url)
        response.raise_for_status()

        with open(csv_filename, "wb") as f:
            f.write(response.content)

        print(f"File CSV berhasil diunduh sebagai {csv_filename}")

    df = pd.read_csv(csv_filename)
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['season'] = df['season'].astype('category')
    df['yr'] = df['yr'].astype('category')
    df['mnth'] = df['mnth'].astype('category')
    df['holiday'] = df['holiday'].astype('category')
    df['weekday'] = df['weekday'].astype('category')
    df['workingday'] = df['workingday'].astype('category')
    df['weathersit'] = df['weathersit'].astype('category')
    df.rename(columns={
        'dteday': 'tanggal',
        'season': 'musim',
        'yr': 'tahun',
        'mnth': 'bulan',
        'holiday': 'hari_libur',
        'weekday': 'hari_minggu',
        'workingday': 'hari_kerja',
        'weathersit': 'kondisi_cuaca',
        'temp': 'suhu',
        'atemp': 'suhu_terasa',
        'hum': 'kelembaban',
        'windspeed': 'kecepatan_angin',
        'casual': 'penyewa_casual',
        'registered': 'penyewa_registered',
        'cnt': 'jumlah_sewa'
    }, inplace=True)
    return df

# Memuat data
df = load_data()

# Judul aplikasi
st.title("Analisis Data Penyewaan Sepeda")

# Sidebar untuk filter
st.sidebar.header("Filter Data")
musim_filter = st.sidebar.multiselect("Pilih Musim", options=df['musim'].unique(), default=df['musim'].unique())
tahun_filter = st.sidebar.multiselect("Pilih Tahun", options=df['tahun'].unique(), default=df['tahun'].unique())
hari_kerja_filter = st.sidebar.multiselect("Pilih Hari Kerja", options=df['hari_kerja'].unique(), default=df['hari_kerja'].unique())
kondisi_cuaca_filter = st.sidebar.multiselect("Pilih Kondisi Cuaca", options=df['kondisi_cuaca'].unique(), default=df['kondisi_cuaca'].unique())

# Filter data berdasarkan pilihan pengguna
filtered_df = df[df['musim'].isin(musim_filter) & 
                  df['tahun'].isin(tahun_filter) & 
                  df['hari_kerja'].isin(hari_kerja_filter) & 
                  df['kondisi_cuaca'].isin(kondisi_cuaca_filter)]

# Visualisasi
st.subheader("Distribusi Kolom Numerik")
kolom_numerik = ['suhu', 'suhu_terasa', 'kelembaban', 'kecepatan_angin', 'penyewa_casual', 'penyewa_registered', 'jumlah_sewa']
for kolom in kolom_numerik:
    fig, ax = plt.subplots()
    sns.histplot(filtered_df[kolom], ax=ax)
    st.pyplot(fig)

st.subheader("Distribusi Kolom Kategorikal")
kolom_kategorikal = ['musim', 'tahun', 'bulan', 'hari_libur', 'hari_minggu', 'hari_kerja', 'kondisi_cuaca']
for kolom in kolom_kategorikal:
    fig, ax = plt.subplots()
    sns.countplot(x=filtered_df[kolom], ax=ax)
    st.pyplot(fig)

st.subheader("Pola Penyewaan Sepeda Berdasarkan Hari Kerja dan Hari Libur")
fig, ax = plt.subplots()
sns.boxplot(x='hari_kerja', y='jumlah_sewa', data=filtered_df, hue='hari_libur', ax=ax)
st.pyplot(fig)

st.subheader("Korelasi Antar Variabel")
fig, ax = plt.subplots()
kolom_korelasi = ['musim', 'tahun', 'bulan', 'hari_libur', 'hari_minggu', 'hari_kerja', 'kondisi_cuaca', 'suhu', 'suhu_terasa', 'kelembaban', 'kecepatan_angin']
sns.heatmap(filtered_df[kolom_korelasi + ['jumlah_sewa']].corr(), annot=True, cmap='coolwarm', annot_kws={"size": 8}, ax=ax)
st.pyplot(fig)

st.subheader("Pengaruh Musim terhadap Jumlah Sewa Sepeda")
fig, ax = plt.subplots()
sns.boxplot(x='musim', y='jumlah_sewa', data=filtered_df, ax=ax)
st.pyplot(fig)

st.subheader("Pengaruh Cuaca terhadap Jumlah Sewa Sepeda")
fig, ax = plt.subplots()
sns.boxplot(x='kondisi_cuaca', y='jumlah_sewa', data=filtered_df, ax=ax)
st.pyplot(fig)

st.subheader("Pola Penyewaan Sepeda Berdasarkan Hari Kerja dan Hari Libur (Bar Chart)")
grouped_data = filtered_df.groupby(['hari_kerja', 'hari_libur'])['jumlah_sewa'].mean().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='hari_kerja', y='jumlah_sewa', hue='hari_libur', data=grouped_data, ax=ax)
st.pyplot(fig)
