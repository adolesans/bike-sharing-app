# -*- coding: utf-8 -*-
"""Analisis Sewa Sepeda  26mar.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1p1gnJlA5Rx9e8NPhuzKFdp3TVjsRopPL

# Proyek Analisis Data: [Analisis Sewa Sepeda]
- **Nama:** Annisa Dewiyanti
- **Email:** annisadewiyanti6@gmail.com
- **ID Dicoding:** andwynt

## Menentukan Pertanyaan Bisnis

1. Bagaimana perbandingan rata-rata jumlah penyewaan sepeda antara hari kerja dan bukan hari libur, serta bagaimana pengaruh hari libur terhadap keduanya?
2. Faktor apa yang memiliki korelasi paling kuat terhadap jumlah penyewa sepeda?

## Import Semua Packages/Library yang Digunakan
"""

import os
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests 

github_raw_url = "https://github.com/adolesans/bike-sharing-app/blob/main/combined-dataset.csv"  
csv_filename = "dataset.csv"

response = requests.get(github_raw_url)
response.raise_for_status()

with open(csv_filename, "wb") as f:
    f.write(response.content)

print(f"File CSV berhasil diunduh sebagai {csv_filename}")

csv_path = os.path.join(extract_path, 'day.csv')
df = pd.read_csv(csv_path) 
"""## Data Wrangling

### Gathering Data
"""

print(df.head())

print(df.info())

"""**Insight:**

- Ada dua jenis pengguna sepeda: **Casual** (tidak terdaftar) dan **Registered** (terdaftar).
- Dataset mencakup dua tahun (2011 dan 2012)


*   Musim (season)
*  Hari Kerja vs. Akhir Pekan (Workingday)
* Cuaca (weathersit)
* Distribusi Variabel Cuaca (temp, atemp, hum, windspeed)

### Assessing Data
"""

print("Info DataFrame:")
print(df.info())

print("Statistik Deskriptif:")
print(df.describe())

print("Jumlah Nilai yang Hilang per Kolom:")
print(df.isnull().sum())

print("Jumlah Duplikat:")
print(df.duplicated().sum())

kolom_kategorikal = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
print("Nilai Unik Kolom Kategorikal:")
for kolom in kolom_kategorikal:
    print(f"{kolom}: {df[kolom].unique()}")

kolom_numerik = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
print("Rentang Nilai Kolom Numerik:")
for kolom in kolom_numerik:
    print(f"{kolom}: min={df[kolom].min()}, max={df[kolom].max()}")

print("Jumlah Tanggal Unik di 'dteday':")
print(df['dteday'].nunique())
print(f"Jumlah Baris: {len(df)}")

"""**Insight:**

Dari hasil pemeriksaan dataset penyewaan sepeda, semua tipe data sudah sesuai, namun kolom tanggal sebaiknya diubah ke format *datetime* agar lebih mudah dianalisis. Tidak ada data yang kosong (missing values) atau data ganda (duplikat), jadi kualitas datanya cukup baik. Statistik menunjukkan bahwa jumlah penyewa memiliki rata-rata yang wajar dan tidak ditemukan nilai ekstrem (outlier) yang mencurigakan. Selain itu, kategori seperti musim (*season*), hari libur (*holiday*), dan hari kerja (*workingday*) memiliki nilai yang benar dan konsisten. Dengan data yang bersih ini, analisis lebih lanjut tentang pola penyewaan bisa dilakukan dengan lebih akurat.

### Cleaning Data
"""

# Konversi Tipe Data

df['dteday'] = pd.to_datetime(df['dteday'])
df['season'] = df['season'].astype('category')
df['yr'] = df['yr'].astype('category')
df['mnth'] = df['mnth'].astype('category')
df['holiday'] = df['holiday'].astype('category')
df['weekday'] = df['weekday'].astype('category')
df['workingday'] = df['workingday'].astype('category')
df['weathersit'] = df['weathersit'].astype('category')

kolom_tidak_digunakan = ['instant']
df = df.drop(kolom_tidak_digunakan, axis=1)

# Ubah Nama Kolom

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
    'casual' : 'penyewa_casual',
    'registered' : 'penyewa_registered',
    'cnt': 'jumlah_sewa'
}, inplace=True)

print("\nDataFrame After Cleaning:")
print(df.head())

"""**Insight:**

* Konversi tipe data dan perubahan nama kolom mempermudah analisis dan visualisasi.

## Exploratory Data Analysis (EDA)

### Explore ...
"""

kolom_numerik = ['suhu', 'suhu_terasa', 'kelembaban', 'kecepatan_angin', 'penyewa_casual', 'penyewa_registered', 'jumlah_sewa']
print("\nDistribusi Kolom Numerik:")
plt.figure(figsize=(12, 10))
for i, kolom in enumerate(kolom_numerik):
    plt.subplot(3, 3, i + 1)
    sns.histplot(df[kolom])
    plt.title(f"Distribusi {kolom}", fontsize=10)
plt.tight_layout()
plt.show()

"""1. Suhu (**temp**): Kebanyakan suhu berada di tengah-tengah (sekitar 0,4–0,6), artinya penyewaan sepeda sering terjadi di suhu sedang.
2. Suhu yang dirasakan (**atemp**): Kebanyakan suhu yang dirasakan berada di antara 0,4 hingga 0,6. Sala seperti temp.
Kelembapan (**hum**): Sebagian besar hari memiliki kelembapan cukup tinggi (sekitar 0,6–0,8).
3. Kecepatan angin (**windspeed**): Kebanyakan kecepatan angin rendah (sekitar 0,1–0,3), jarang ada angin kencang.
4. Penyewa tidak terdaftar (**casual**): Mayoritas penyewa dari kategori ini jumlahnya kecil (kurang dari 3000 orang).
5. Penyewa terdaftar (**registered**): Sebagian besar penyewa berasal dari pengguna yang sudah terdaftar (antara 2000–6000 orang).
6. Total penyewa (**cnt**): Jumlah penyewa paling sering berada di kisaran 4000–6000 orang.

Kesimpulannya, kebanyakan penyewaan sepeda terjadi di suhu sedang, kelembapan tinggi, dan sebagian besar penyewa adalah pengguna yang sudah terdaftar.
"""

kolom_kategorikal = ['musim', 'tahun', 'bulan', 'hari_libur', 'hari_minggu', 'hari_kerja', 'kondisi_cuaca']  # Updated column names
print("\nDistribusi Kolom Kategorikal:")
plt.figure(figsize=(12, 10))  # Ukuran figure untuk semua plot
for i, kolom in enumerate(kolom_kategorikal):
    plt.subplot(3, 3, i + 1)  # Tata letak 3x3
    sns.countplot(x=df[kolom])
    plt.title(f"Distribusi {kolom}", fontsize=10)  # Ukuran font judul
plt.tight_layout()  # Menyesuaikan tata letak agar plot tidak tumpang tindih
plt.show()

"""**Insight**

1. season (musim): Data terbagi rata di keempat musim (1 = semi, 2 = panas, 3 = gugur, 4 = dingin), menunjukkan jumlah data hampir sama di setiap musim.
2. yr (tahun): Data terbagi secara seimbang di dua tahun, yaitu 0 (tahun pertama) dan 1 (tahun kedua).
3. mnth (bulan): Data dari Januari (1) hingga Desember (12) cukup merata, menunjukkan data mencakup semua bulan dalam setahun.
4. holiday (hari libur): Sebagian besar data berasal dari hari biasa (0 = bukan hari libur), sementara hanya sedikit yang berasal dari hari libur (1 = hari libur).
5. weekday (hari dalam seminggu): Data tersebar merata dari Senin (0) hingga Minggu (6), menunjukkan tidak ada hari tertentu yang mendominasi.
6. workingday (hari kerja): Lebih banyak data berasal dari hari kerja (1 = hari kerja) dibandingkan hari libur atau akhir pekan (0 = bukan hari kerja).
7. weathersit (kondisi cuaca): Mayoritas data berasal dari cuaca cerah atau berawan ringan (kategori 1), lebih sedikit pada cuaca berkabut (kategori 2), dan sangat sedikit pada cuaca buruk (kategori 3).

Kesimpulannya, sebagian besar penyewaan terjadi pada hari kerja, dalam cuaca baik, dan dataset mencakup semua musim, bulan, dan hari dalam seminggu secara cukup merata.
"""

plt.figure(figsize=(8, 6))
sns.boxplot(x='hari_kerja', y='jumlah_sewa', data=df, hue='hari_libur') # Changed 'holiday' to 'hari_libur'
plt.title("Pola Penyewaan Sepeda Berdasarkan Hari Kerja dan Hari Libur", fontsize=10)
plt.xlabel("Hari Kerja (0: Bukan Hari Kerja, 1: Hari Kerja)", fontsize=8)
plt.ylabel("Jumlah Sewa Sepeda (jumlah_sewa)", fontsize=8) # Update y-axis label
plt.show()

"""**Insight:**

1. Hari kerja (1) memiliki sebaran jumlah penyewa yang cenderung lebih tinggi dan konsisten dibandingkan hari libur.
2. Bukan hari kerja (0) menunjukkan variasi jumlah penyewa yang lebih besar, tetapi median (nilai tengah) lebih rendah dibandingkan hari kerja.
3. Penyewaan sepeda pada hari libur (oranye) lebih bervariasi, ada hari dengan jumlah penyewa yang rendah dan tinggi.

**Kesimpulan:**
* Penyewaan sepeda cenderung lebih banyak di hari kerja dibandingkan hari libur atau akhir pekan.
* Di hari libur, jumlah penyewaan lebih bervariasi, tetapi sebagian besar lebih rendah daripada hari kerja.
"""

plt.figure(figsize=(8, 6))

kolom_korelasi = ['musim', 'tahun', 'bulan', 'hari_libur', 'hari_minggu', 'hari_kerja', 'kondisi_cuaca', 'suhu', 'suhu_terasa', 'kelembaban', 'kecepatan_angin']
sns.heatmap(df[kolom_korelasi + ['jumlah_sewa']].corr(), annot=True, cmap='coolwarm', annot_kws={"size": 8})
plt.title("Korelasi Antar Variabel", fontsize=10)
plt.show()

"""Insight:

1. Faktor yang Paling Berhubungan dengan Jumlah Penyewa (cnt):

* **atemp** (0.63): Suhu yang dirasakan memiliki hubungan paling kuat dan positif terhadap jumlah penyewa. Artinya, saat suhu nyaman, jumlah penyewa meningkat.
* **temp** (0.63): Suhu aktual juga memiliki korelasi yang cukup tinggi.
* **season** (0.41): Musim juga memengaruhi jumlah penyewa. Biasanya, musim yang nyaman (musim semi/panas) meningkatkan penyewaan.
* **humidity** (-0.30): Kelembapan memiliki korelasi negatif, artinya saat kelembapan tinggi, jumlah penyewa cenderung menurun.
* **windspeed** (-0.23): Kecepatan angin juga memiliki hubungan negatif meskipun lebih lemah.


2. Kesimpulan:

* **Suhu (temp dan atemp)** adalah faktor yang paling memengaruhi jumlah penyewaan sepeda—semakin nyaman suhunya, semakin banyak penyewa.
* **Kelembapan (humidity)** dan kecepatan angin (windspeed) cenderung mengurangi jumlah penyewaan sepeda.
* **Tidak ada hubungan signifikan antara hari kerja** (workingday) atau hari libur (holiday) dengan jumlah penyewa di heatmap ini.
"""

plt.figure(figsize=(8, 6))
sns.boxplot(x='musim', y='jumlah_sewa', data=df)  # Changed 'season' to 'musim' and 'cnt' to 'jumlah_sewa'
plt.title("Pengaruh Musim terhadap Jumlah Sewa Sepeda", fontsize=10)
plt.xlabel("Musim (1: Musim Semi, 2: Musim Panas, 3: Musim Gugur, 4: Musim Dingin)", fontsize=8)
plt.ylabel("Jumlah Sewa Sepeda (cnt)", fontsize=8)
plt.show()

"""Insight:

jumlah penyewaan sepeda dipengaruhi oleh musim. Penyewaan paling banyak terjadi di musim panas, kemungkinan karena cuaca yang hangat dan nyaman untuk bersepeda. Musim gugur juga menunjukkan jumlah penyewaan yang cukup tinggi. Sebaliknya, di musim dingin dan musim semi, jumlah penyewaan cenderung lebih rendah, mungkin karena cuaca yang lebih dingin atau kurang mendukung untuk beraktivitas di luar ruangan. Jadi, cuaca yang hangat dan nyaman mendorong lebih banyak orang untuk menyewa sepeda.
"""

plt.figure(figsize=(8, 6))
sns.boxplot(x='kondisi_cuaca', y='jumlah_sewa', data=df)
plt.title("Pengaruh Cuaca terhadap Jumlah Sewa Sepeda", fontsize=10)
plt.xlabel("Cuaca (1: Cerah, 2: Kabut, 3: Hujan Ringan, 4: Hujan Lebat)", fontsize=8)
plt.ylabel("Jumlah Sewa Sepeda (cnt)", fontsize=8)
plt.show()

"""Dari diagram ini, terlihat bahwa cuaca sangat memengaruhi jumlah penyewaan sepeda. Ketika cuaca cerah (kategori 1), jumlah penyewaan sepeda cenderung paling tinggi. Saat cuaca berkabut atau hujan ringan (kategori 2 dan 3), jumlah penyewaan menurun secara signifikan. Ini menunjukkan bahwa orang lebih suka menyewa sepeda saat cuaca baik, sedangkan cuaca buruk seperti hujan mengurangi minat untuk bersepeda.

## Visualization & Explanatory Analysis

### Pertanyaan 1:
"""

grouped_data = df.groupby(['hari_kerja', 'hari_libur'])['jumlah_sewa'].mean().reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(x='hari_kerja', y='jumlah_sewa', hue='hari_libur', data=grouped_data)

plt.title("Pola Penyewaan Sepeda Berdasarkan Hari Kerja dan Hari Libur (Bar Chart)")
plt.xlabel("Hari Kerja (0: Bukan Hari Kerja, 1: Hari Kerja)")
plt.ylabel("Rata-rata Jumlah Sewa Sepeda")
plt.show()

"""**Insight:**

**Jumlah Penyewaan di Hari Kerja vs. Hari Libur**

* **Hari Kerja** (workingday = 1) memiliki jumlah penyewaan yang cenderung lebih tinggi dibandingkan** hari libur** (workingday = 0).
Ini menunjukkan bahwa banyak orang menggunakan sepeda sebagai alat transportasi utama untuk aktivitas sehari-hari seperti pergi ke kantor atau sekolah.


* **Variasi Penyewaan**
di kedua kategori (hari kerja dan hari libur), terdapat variasi jumlah penyewaan yang cukup besar. Namun, penyewaan di hari kerja lebih konsisten dan cenderung lebih tinggi.
Penyewaan di hari libur terlihat memiliki sebaran yang lebih luas, menunjukkan adanya variasi jumlah penyewa yang lebih beragam di akhir pekan atau hari libur.


* **Kesimpulan:**
data menunjukan bahwa ada pola penyewaan yang berbeda antara hari kerja dan hari libur. Penyewaan lebih banyak terjadi di hari kerja, menunjukkan bahwa sepeda banyak digunakan untuk kebutuhan rutin. Namun, di hari libur, penyewaan tetap ada tetapi cenderung lebih bervariasi, kemungkinan karena digunakan untuk rekreasi atau aktivitas santai.

### Pertanyaan 2:
"""

plt.figure(figsize=(8, 6))

kolom_korelasi = ['musim', 'tahun', 'bulan', 'hari_libur', 'hari_minggu', 'hari_kerja', 'kondisi_cuaca', 'suhu', 'suhu_terasa', 'kelembaban', 'kecepatan_angin']
sns.heatmap(df[kolom_korelasi + ['jumlah_sewa']].corr(), annot=True, cmap='coolwarm', annot_kws={"size": 8})
plt.title("Korelasi Antar Variabel", fontsize=10)
plt.show()

"""Insight :

Berdasarkan hasil analisis korelasi, ditemukan bahwa **faktor yang paling berpengaruh terhadap jumlah penyewa sepeda adalah suhu terasa (0.63)**. Hal ini menunjukkan bahwa ketika suhu terasa lebih nyaman, jumlah penyewa cenderung meningkat secara signifikan. Selain itu, **tahun (0.57)** juga memiliki hubungan positif yang cukup kuat, mengindikasikan adanya tren peningkatan penyewaan sepeda dari waktu ke waktu, kemungkinan dipengaruhi oleh perubahan gaya hidup atau kebijakan transportasi ramah lingkungan. **Kondisi cuaca (0.30)** juga memiliki korelasi positif, yang berarti cuaca yang lebih baik mendorong lebih banyak orang untuk menyewa sepeda. Sebaliknya, **kecepatan angin (-0.23)** menunjukkan korelasi negatif, di mana angin yang lebih kencang cenderung mengurangi jumlah penyewa karena bersepeda menjadi lebih sulit dan kurang nyaman. Faktor lain seperti musim, hari kerja, dan hari libur memiliki korelasi yang lemah terhadap jumlah penyewa, menunjukkan bahwa pengaruhnya tidak terlalu signifikan. Dengan demikian, suhu terasa, tahun, dan kondisi cuaca adalah faktor utama yang mendorong peningkatan penyewaan sepeda, sementara kecepatan angin menjadi penghambat.

Cuaca yang nyaman menjadi faktor utama yang mendorong peningkatan penyewaan sepeda.
Musim juga memengaruhi, di mana jumlah penyewa meningkat pada musim-musim dengan cuaca yang mendukung aktivitas luar ruangan.

## Analisis Lanjutan (Opsional)

1. Bagaimana perbandingan rata-rata jumlah penyewaan sepeda antara hari kerja dan bukan hari libur, serta bagaimana pengaruh hari libur terhadap keduanya?

Berdasarkan hasil analisis, ditemukan bahwa jumlah penyewaan sepeda cenderung lebih tinggi pada hari kerja dibandingkan hari libur. Hal ini menunjukkan bahwa sepeda digunakan secara signifikan sebagai alat transportasi utama untuk aktivitas rutin seperti pergi ke kantor atau sekolah.

* Konsistensi Penyewaan: Penyewaan di hari kerja menunjukkan pola yang lebih stabil dan konsisten, kemungkinan karena kebutuhan transportasi yang terjadwal secara rutin.

* Variasi di Hari Libur: Meskipun jumlah penyewaan lebih rendah di hari libur, terdapat variasi yang lebih besar dalam jumlah penyewa. Ini menunjukkan bahwa sepeda digunakan untuk aktivitas rekreasi atau perjalanan santai pada akhir pekan atau hari libur.

Implikasi Bisnis:

* Peningkatan ketersediaan sepeda di hari kerja akan memenuhi permintaan yang tinggi dari pengguna harian.

* Menawarkan promosi atau paket khusus di akhir pekan dapat menarik lebih banyak pelanggan yang menggunakan sepeda untuk aktivitas santai atau rekreasi.

2. Faktor Apa yang Paling Berpengaruh Terhadap Jumlah Penyewaan Sepeda?

* Suhu Terasa (r = 0.63): Faktor yang paling berpengaruh terhadap jumlah penyewa adalah suhu terasa. Ketika suhu terasa lebih nyaman, jumlah penyewa meningkat secara signifikan.

* Tahun (r = 0.57): Ada tren peningkatan jumlah penyewaan dari waktu ke waktu, yang menunjukkan bahwa semakin banyak orang menggunakan sepeda, kemungkinan karena kesadaran lingkungan atau perubahan gaya hidup.

* Kondisi Cuaca (r = 0.30): Cuaca yang baik mendorong lebih banyak penyewaan, sedangkan kondisi cuaca buruk dapat menghambat aktivitas bersepeda.

* Kecepatan Angin (r = -0.23): Kecepatan angin memiliki hubungan negatif, di mana angin yang lebih kencang cenderung menurunkan jumlah penyewaan karena bersepeda menjadi lebih sulit dan tidak nyaman.

* Faktor Lain (Musim, Hari Kerja, Hari Libur): Faktor ini memiliki korelasi yang lebih lemah, menunjukkan bahwa pengaruhnya terhadap jumlah penyewa relatif kecil dibandingkan faktor lingkungan seperti suhu dan cuaca.

**Implikasi Bisnis:**

* Menyediakan lebih banyak sepeda di musim dengan cuaca nyaman dapat meningkatkan jumlah penyewa.

* Menyesuaikan jumlah sepeda yang tersedia dan strategi promosi berdasarkan musim dan kondisi cuaca untuk memaksimalkan penyewaan.

* Memonitor tren tahunan dapat membantu dalam merencanakan ekspansi layanan atau menyesuaikan operasional sesuai kebutuhan pelanggan.

## Conclusion

Analisis menunjukkan bahwa pola penyewaan sepeda bervariasi secara signifikan antara hari kerja dan hari libur. Permintaan lebih tinggi di **hari kerja**, mengindikasikan bahwa sepeda banyak digunakan sebagai sarana transportasi rutin. Sebaliknya, di** hari libur**, penyewaan bersifat lebih fluktuatif, mencerminkan penggunaan untuk kebutuhan rekreasi atau aktivitas santai.

Faktor eksternal seperti **suhu terasa, cuaca, dan kecepatan angin** memiliki pengaruh langsung terhadap jumlah penyewa. **Suhu terasa** yang lebih nyaman dan kondisi cuaca yang baik meningkatkan permintaan, sementara **kecepatan angin yang tinggi** justru menurunkan minat penyewaan. Selain itu, analisis juga menunjukkan adanya tren kenaikan jumlah penyewa seiring waktu, yang mengisyaratkan potensi pertumbuhan pasar di masa depan.

Dengan memahami hubungan antara faktor lingkungan dan perilaku penyewa, perusahaan dapat mengambil langkah strategis seperti **meningkatkan ketersediaan sepeda di jam sibuk hari kerja**, **menawarkan promosi di hari libur, atau menyesuaikan layanan berdasarkan prakiraan cuaca.** Pendekatan berbasis data ini memungkinkan optimalisasi operasional, meningkatkan kepuasan pelanggan, dan mendorong pertumbuhan bisnis secara berkelanjutan
"""
