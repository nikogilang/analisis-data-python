# -*- coding: utf-8 -*-
"""Proyek Analisis Data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19POkCWicgPWEuY1jiLnk-Lh4UucQ8iR_

# Proyek Analisis Data: Bike Sharing Dataset
- **Nama:** Nico Gilang Aprully
- **Email:** m180d4ky2887@bangkit.academy
- **ID Dicoding:** nikogilang

## Menentukan Pertanyaan Bisnis

1.   Apakah terdapat perbedaan pola penggunaan sepeda antara musim panas, musim gugur, musim dingin, dan musim semi?
2. Bagaimana perubahan pola penggunaan sepeda selama akhir pekan (hari libur) dibandingkan dengan hari kerja?

## Import Semua Packages/Library yang Digunakan
"""
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit babel plotly
import http
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import warnings
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

"""## Data Wrangling

### Gathering Data
"""

day_url = 'https://raw.githubusercontent.com/nikogilang/analisis-data-python/main/Bike-sharing-dataset/day.csv'
hour_url = 'https://raw.githubusercontent.com/nikogilang/analisis-data-python/main/Bike-sharing-dataset/hour.csv'

df_day = pd.read_csv(day_url, delimiter=",")
df_hour = pd.read_csv(hour_url, delimiter=",")

"""Keseluruhan dataframe Hari"""

df_day

"""Keseluruhan Dataframe Jam"""

df_hour

"""### Assessing Data"""

df_day.info()

df_hour.info()

"""Mencari nilai Missing Value pada dataframe"""

print('DataFrame Hari:')
print(df_day.isna().sum())

print('\nDataFrame Jam:')
print(df_hour.isna().sum())

"""Mencari nilai duplikasi pada Dataframe"""

print('DataFrame Hari:')
print(df_day.duplicated().sum())

print("DataFrame Jam:")
print(df_hour.duplicated().sum())

"""### Cleaning Data

Mengubah tipe data
"""

df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

print('dtday_day  : ', df_day['dteday'].dtype)
print('dtday_hour : ',df_hour['dteday'].dtype)

"""## Exploratory Data Analysis (EDA)

### Explore ...
"""

df_day.describe()

df_hour.describe()

# Plot korelasi hubungan antar variable

correlation_matrix = df_day.corr()
fig = px.imshow(correlation_matrix)
fig.update_traces(colorscale='balance')
fig.update_layout(width=1200, height=600)
fig.update_layout(title="Plot Korelasi Variabel Numerik")
fig.show()

# Plot Distribusi Variabel Numerik

var_numeric = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
for col in var_numeric:
    fig = px.histogram(df_day, x=col, title=f'Distribusi Variabel {col}')
    fig.update_yaxes(title_text="Jumlah")
    fig.update_layout(width=800, height=600)
    fig.show()

# Hubungan Season dan Jumlah Sewa

fig = px.box(df_day, x='season', y='cnt')
fig.update_layout(title='Hubungan Season dan Jumlah Sewa')
fig.show()

# Hubungan Weekday dan Jumlah Sewa

df_day['weekday'] = df_day['weekday'].astype('category')

fig = px.box(df_day, x='weekday', y='cnt')
fig.update_layout(title='Hubungan Hari dan Jumlah Sewa')
fig.show()

"""## Visualization & Explanatory Analysis

### Pertanyaan 1: Apakah terdapat perbedaan pola penggunaan sepeda antara musim panas, musim gugur, musim dingin, dan musim semi?
"""

# Ubah tipe data kolom 'dteday' menjadi tipe data datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

# Ekstrak bulan dari kolom 'dteday'
df_day['month'] = df_day['dteday'].dt.month

# Visualisasi penggunaan sepeda berdasarkan musim
fig = px.box(df_day, x='season', y='cnt', color='season',
             category_orders={'season': ['Spring', 'Summer', 'Fall', 'Winter']},
             labels={'season': 'Musim', 'cnt': 'Jumlah Sewa Sepeda'})
fig.update_layout(title='Penggunaan Sepeda Berdasarkan Musim',
                  xaxis_title='Musim', yaxis_title='Jumlah Sewa Sepeda')
fig.show()

# Ubah tipe data kolom 'dteday' menjadi tipe data datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

# Ekstrak bulan dari kolom 'dteday'
df_day['month'] = df_day['dteday'].dt.month

# Ubah kolom season menjadi kategori dengan nama musim yang sesuai
df_day['season'] = df_day['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

# Visualisasi penggunaan sepeda berdasarkan musim dalam diagram balok
fig = px.bar(df_day, x='season', y='cnt', color='season',
             category_orders={'season': ['Spring', 'Summer', 'Fall', 'Winter']},
             labels={'season': 'Musim', 'cnt': 'Jumlah Sewa Sepeda'},
             title='Penggunaan Sepeda Berdasarkan Musim')

fig.update_layout(xaxis_title='Musim', yaxis_title='Jumlah Sewa Sepeda')
fig.show()

"""Visualisasi box plot dan bar plot menunjukkan variasi pola penggunaan sepeda berdasarkan musim. Dari grafik-grafik tersebut, terlihat bahwa jumlah sewa sepeda cenderung meningkat seiring pergantian musim dari musim semi hingga musim gugur, sementara menurun pada musim yang lebih dingin seperti musim dingin. Terdapat beberapa data outlier pada data tersebut, menunjukkan adanya kejadian yang memengaruhi jumlah sewa sepeda pada musim tertentu. Analisis visual ini memberikan informasi dan data berharga bagi pengelola layanan penyewaan sepeda untuk mengelola stok sepeda dan menyesuaikan strategi pemasaran berdasarkan tren penggunaan sepeda pada tiap musim.

### Pertanyaan 2: Bagaimana perubahan pola penggunaan sepeda selama akhir pekan (hari libur) dibandingkan dengan hari kerja?
"""

# Mengonversi tipe data kolom 'dteday' menjadi tipe data datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

# Ekstrak hari dari kolom 'dteday' (0: Sunday, 1: Monday, ..., 6: Saturday)
df_day['day_of_week'] = df_day['dteday'].dt.dayofweek

# Mengidentifikasi apakah hari adalah akhir pekan (0: Tidak, 1: Ya)
df_day['is_weekend'] = df_day['day_of_week'].isin([5, 6]).astype(int)

# Menghitung rata-rata jumlah sewa sepeda berdasarkan akhir pekan dan hari kerja
df_weekend = df_day.groupby('is_weekend')['cnt'].mean().reset_index()

# Visualisasi rata-rata penggunaan sepeda pada akhir pekan dan hari kerja menggunakan bar plot
fig = px.bar(df_weekend, x='is_weekend', y='cnt', color='is_weekend',
             labels={'is_weekend': 'Hari Libur (0: Tidak, 1: Ya)', 'cnt': 'Rata-rata Jumlah Sewa Sepeda'},
             title='Rata-rata Penggunaan Sepeda pada Akhir Pekan vs. Hari Kerja',
             text='cnt')
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(xaxis_title='Hari Libur (0: Tidak, 1: Ya)', yaxis_title='Rata-rata Jumlah Sewa Sepeda')
fig.update_xaxes(tickvals=[0, 1], ticktext=['Hari Kerja', 'Akhir Pekan'])
fig.show()

df_day['weekday'] = df_day['weekday'].astype('category')

# Ubah nilai weekday menjadi nama hari dalam seminggu
df_day['weekday'] = df_day['weekday'].map({0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'})

# Hitung rata-rata jumlah sewa untuk setiap hari dalam seminggu
weekday_counts = df_day.groupby('weekday')['cnt'].mean().reset_index()

# Visualisasi penggunaan sepeda berdasarkan hari dalam seminggu dalam diagram balok
fig = px.bar(weekday_counts, x='weekday', y='cnt',
             labels={'weekday': 'Hari', 'cnt': 'Jumlah Sewa Sepeda Rata-rata'},
             title='Hubungan Hari dan Jumlah Sewa')

fig.update_layout(xaxis_title='Hari', yaxis_title='Jumlah Sewa Sepeda Rata-rata')
fig.show()

"""Visualisasi box plot dan bar plot dari hari-hari yang berkaitan dengan jumlah sewa, dapat dilihat pada grafik pertama bahwa lebih banyak penyewaan sepeda di hari-hari kerja dibandingkan dengan hari libur. Sedangkan pada hari-hari dalam seminggu tampak adanya kenaikan dimulai dari hari minggu ke jumat, lalu turun lagi ketika di hari sabtu. Informasi dan data ini bisa digunakan oleh pihak penyewa sepeda untuk memaksimalkan target pasar dan strategi pemasaran.

## Conclusion

1. Terdapat perbedaan jumlah sewa sepeda cenderung meninggi dimulai dari musim semi hingga musim gugur, sementara cenderung menurun pada musim dingin. Hal ini bisa dikarenakan kondisi salju dan cuaca yang dingin yang mempersulit ketika menggunakan sepeda.
2. Rata-rata jumlah sewa sepeda cenderung lebih tinggi pada hari kerja dibandingkan dengan hari libur. Hal ini mungkin disebabkan oleh penggunaan sepeda sebagai mode transportasi untuk bepergian dan beraktivitas lebih banyak digunakan pada saat hari kerja.
"""
