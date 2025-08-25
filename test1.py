import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('datavalidasi_cleaned.csv')

# Clean up any potential issues with column names
data.columns = data.columns.str.strip()

# Convert 'Tanggal Input' to datetime format for proper handling
data['Tanggal Input'] = pd.to_datetime(data['Tanggal Input'], format='%d/%m/%Y')

# Sidebar: Select the period (month) to filter by
period_choices = sorted(data['PERIODE'].unique())
selected_period = st.sidebar.selectbox("Pilih Periode", period_choices)

# Filter the data based on the selected period
filtered_data = data[data['PERIODE'] == selected_period]

# Hapus baris dengan nilai kosong di 'Eksisting / New Customer'
filtered_data = filtered_data.dropna(subset=['Eksisting / New Customer'])

# Show filtered data
st.title(f"Data untuk Periode {selected_period}")
st.write(f"Menampilkan data untuk bulan {selected_period}")
st.dataframe(filtered_data)

# Group data by 'Nama AM' and count existing and new customers
customer_counts = (
    filtered_data
    .groupby(['Nama AM', 'Eksisting / New Customer'])
    .size()
    .unstack(fill_value=0)
)

# Display customer counts for each AM
st.subheader("Jumlah Customer per Nama AM")
st.dataframe(customer_counts)

# Filter the data untuk menampilkan jumlah kegiatan sesuai bulan yang dipilih
month_data = data[data['Tanggal Input'].dt.month == filtered_data['Tanggal Input'].dt.month.iloc[0]]

# Group by 'Nama AM' and count the number of activities
activity_counts = month_data.groupby(['Nama AM', 'PERIODE']).size().unstack(fill_value=0)

# Display activity counts for each AM
st.subheader(f"Jumlah Kegiatan per Nama AM ({selected_period})")
st.dataframe(activity_counts)






# Grafik Jumlah Customer per Nama AM
st.subheader("Jumlah Customer per Nama AM")
customer_counts = (
    filtered_data
    .groupby(['Nama AM', 'Eksisting / New Customer'])
    .size()
    .unstack(fill_value=0)
)

# Visualisasi dengan Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))
customer_counts.plot(kind='bar', stacked=True, ax=ax)
plt.title("Jumlah Customer per Nama AM")
plt.xlabel("Nama AM")
plt.ylabel("Jumlah Customer")
plt.xticks(rotation=45)
st.pyplot(fig)



# Grafik Jumlah Kegiatan per Nama AM
st.subheader(f"Jumlah Kegiatan per Nama AM ({selected_period})")
activity_counts = month_data.groupby(['Nama AM', 'PERIODE']).size().unstack(fill_value=0)

# Visualisasi dengan Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))
activity_counts.plot(kind='bar', ax=ax)
plt.title(f"Jumlah Kegiatan per Nama AM ({selected_period})")
plt.xlabel("Nama AM")
plt.ylabel("Jumlah Kegiatan")
plt.xticks(rotation=45)
st.pyplot(fig)



# Grafik Tren Aktivitas per Bulan
st.subheader("Tren Jumlah Kegiatan per Bulan")
monthly_activity = data.groupby(data['Tanggal Input'].dt.to_period('M')).size()

# Visualisasi dengan Line Chart
fig, ax = plt.subplots(figsize=(10, 6))
monthly_activity.plot(kind='line', marker='o', ax=ax)
plt.title("Tren Jumlah Kegiatan per Bulan")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Kegiatan")
st.pyplot(fig)




# Grafik Customer Terbanyak per Nama AM
st.subheader("Customer Terbanyak per Nama AM")
top_am_customers = customer_counts.sum(axis=1).sort_values(ascending=False)

# Visualisasi dengan Horizontal Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))
top_am_customers.plot(kind='barh', ax=ax)
plt.title("Customer Terbanyak per Nama AM")
plt.xlabel("Jumlah Customer")
plt.ylabel("Nama AM")
st.pyplot(fig)
