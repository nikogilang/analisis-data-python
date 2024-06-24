import streamlit as st
import pandas as pd
import plotly.graph_objects as go  # Ganti baris impor ini
import plotly.express as px
import types

# Load data
@st.cache_data(hash_funcs={types.FunctionType: id})
def load_data():
    day_url = 'https://raw.githubusercontent.com/nikogilang/analisis-data-python/main/Bike-sharing-dataset/day.csv'
    df_day = pd.read_csv(day_url)
    return df_day

df_day = load_data()

# Set page title
st.title("Bike Share Dashboard")

# Display sidebar information
st.sidebar.title("Informasi:")
st.sidebar.markdown("**• Nama: Nico Gilang Aprully**")

st.sidebar.title("Dataset Bike Share")
# Show the dataset if selected in the sidebar
if st.sidebar.checkbox("Tampilkan Dataset"):
    st.subheader("Data Mentah")
    st.write(df_day)

# Display summary statistics if selected in the sidebar
if st.sidebar.checkbox("Tampilkan Statistik Ringkas"):
    st.subheader("Statistik Ringkas")
    st.write(df_day.describe())

# Sidebar
st.sidebar.title("Pilihan Visualisasi")
visualization_option = st.sidebar.radio("Pilih visualisasi:", ["Penggunaan Sepeda Berdasarkan Musim",
                                                               "Tanggal vs Jumlah Sewa Sepeda",
                                                               "Rata-rata Penggunaan Sepeda pada Akhir Pekan vs. Hari Kerja"])

season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
df_day['season'] = df_day['season'].map(season_mapping)

week_mapping = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
df_day['weekday'] = df_day['weekday'].map(week_mapping)

if visualization_option == "Penggunaan Sepeda Berdasarkan Musim":
    st.header("Grafik Penyewaan Sepeda Berdasarkan Musim")
    fig = px.pie(df_day, names='season', values='registered', title='Jumlah Pengguna Terdaftar Berdasarkan Musim (2011-2012)')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)

elif visualization_option == "Tanggal vs Jumlah Sewa Sepeda":
    st.header("Pola Penyewaan Sepeda Sepanjang Tahun")
    fig_scatter = px.scatter(df_day, x="dteday", y=["registered", "casual"], title="Hubungan Tanggal dengan Jumlah Pengguna Registered dan Casual")
    fig_scatter.update_xaxes(title="Tanggal")
    fig_scatter.update_yaxes(title="Jumlah Pengguna")
    st.plotly_chart(fig_scatter)
    fig_line = px.line(df_day, x="dteday", y=["registered", "casual"], title="Hubungan Tanggal dengan Jumlah Pengguna Registered dan Casual")
    fig_line.update_xaxes(title="Tanggal")
    fig_line.update_yaxes(title="Jumlah Pengguna")
    st.plotly_chart(fig_line)

else:
    st.header("Rata-rata Penggunaan Sepeda pada Akhir Pekan vs. Hari Kerja")
    fig = px.bar(df_day, x="weekday", y="cnt", title="Grafik Hari dengan Jumlah Pengguna")
    fig.update_xaxes(title="Hari")
    fig.update_yaxes(title="Jumlah Pengguna")
    st.plotly_chart(fig)
    
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    df_day['day_of_week'] = df_day['dteday'].dt.dayofweek
    df_day['is_weekend'] = df_day['day_of_week'].isin([5, 6]).astype(int)
    df_weekend = df_day.groupby('is_weekend')['cnt'].mean().reset_index()
    fig = go.Figure(data=go.Bar(x=df_weekend['is_weekend'], y=df_weekend['cnt']))
    fig.update_layout(title='Rata-rata Penggunaan Sepeda pada Akhir Pekan vs. Hari Kerja',
                      xaxis_title='Hari Libur (0: Tidak, 1: Ya)',
                      yaxis_title='Rata-rata Jumlah Sewa Sepeda')
    fig.update_xaxes(tickvals=[0, 1], ticktext=['Hari Kerja', 'Akhir Pekan'])
    st.plotly_chart(fig)
