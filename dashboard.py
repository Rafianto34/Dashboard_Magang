import pandas as pd
import streamlit as st

# Memuat data dari CSV
data = pd.read_csv("datavalidasi_cleaned.csv")

# Menyediakan pemilihan bulan
bulan = st.selectbox("Pilih Bulan", ["JUNI", "JULI", "AGUSTUS"])

# Filter data berdasarkan bulan yang dipilih
filtered_data = data[data['PERIODE'] == bulan]

# Menampilkan tabel data untuk bulan yang dipilih
st.write(filtered_data)

# Menambahkan pewarnaan pada setiap kolom yang ada persentasenya
def color_positive(val):
    if val >= 100:
        return 'background-color: green; color: white'
    elif val >= 50:
        return 'background-color: yellow; color: black'
    else:
        return 'background-color: red; color: white'


# Mengisi kolom MAPS Customer dengan 5
filtered_data["MAPS Customer %Ach"] = 5

# Menghitung total aktivitas berdasarkan jumlah input per AM (jumlah baris untuk tiap AM)
filtered_data["Total Activity"] = filtered_data.groupby('Nama AM')['Nama AM'].transform('count')

# Menghitung persentase Activity Adventure berdasarkan banyaknya data per AM
max_activity = filtered_data.groupby('Nama AM')['Nama AM'].transform('count').max()  # Max aktivitas
filtered_data["Activity Adventure %Ach"] = (filtered_data["Total Activity"] / max_activity) * 100

# Menambahkan kolom New Customer yang berasal dari kolom "Eksisting / New Customer"
filtered_data["New Customer %Ach"] = filtered_data["Eksisting / New Customer"]

# Input manual untuk Produk Digital dan Sales Bandwidth
produk_digital = st.number_input("Masukkan Produk Digital (%)", min_value=0, max_value=100)
sales_bandwidth = st.number_input("Masukkan Sales Bandwidth (%)", min_value=0, max_value=100)

# Mengupdate kolom Produk Digital dan Sales Bandwidth pada data
filtered_data["Produk Digital %Ach"] = produk_digital
filtered_data["Sales Bandwidth %Ach"] = sales_bandwidth

# Menambahkan skor untuk setiap kategori
filtered_data["Produk Digital Skor"] = filtered_data["Produk Digital %Ach"] * 0.15  # 15% bobot
filtered_data["Activity Adventure Skor"] = filtered_data["Activity Adventure %Ach"] * 0.30  # 30% bobot
filtered_data["Unlock New Customer Skor"] = filtered_data["New Customer %Ach"] * 0.20  # 20% bobot
filtered_data["MAPS Customer Skor"] = filtered_data["MAPS Customer %Ach"] * 0.15  # 15% bobot
filtered_data["Sales Bandwidth Skor"] = filtered_data["Sales Bandwidth %Ach"] * 0.20  # 20% bobot

# Menghitung Total Skor dan Total Ach
filtered_data["Total Skor"] = (filtered_data["Produk Digital Skor"] +
                               filtered_data["Activity Adventure Skor"] +
                               filtered_data["Unlock New Customer Skor"] +
                               filtered_data["MAPS Customer Skor"] +
                               filtered_data["Sales Bandwidth Skor"])

# Menampilkan tabel dengan pewarnaan
st.title("Report AM Chess Master")
st.table(filtered_data.style.applymap(color_positive, subset=["Produk Digital %Ach", "Activity Adventure %Ach", 
                                                             "New Customer %Ach", "Sales Bandwidth %Ach"]))

# Tampilkan hasil perhitungan
st.write(f"Persentase Pencapaian: {(produk_digital + sales_bandwidth) / 2}%")
st.write(f"Skor: {(produk_digital + sales_bandwidth) / 2 * 0.3}")
