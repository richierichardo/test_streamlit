import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
from PIL import Image, ImageDraw

# Load foto
foto_path = "foto richie.jpg"
original_image = Image.open(foto_path)

# Resize dan crop foto menjadi bentuk bulat
resized_image = original_image.resize((300, 300))
mask = Image.new('L', (300, 300), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, 300, 300), fill=255)
rounded_image = Image.new('RGB', (300, 300))
rounded_image.paste(resized_image, mask=mask)

# Menampilkan foto dan header
col1, col2 = st.columns(2)
with col1:
    st.image(rounded_image, use_column_width=True)

with col2:
    # Header
    st.title("Richie Richardo")
    st.subheader("Email: richierichardo777@gmail.com")
    st.subheader("Id Dicoding: \nrichie richardo")

# Menambahkan garis sebagai pemisah
st.markdown("---")

# Lanjutkan dengan konten di bawah header
st.write("Selamat datang di halaman Streamlit saya. Di sini saya akan menampilkan Analisis Data dengan dataset Bike Sharing.")
# Menyisipkan teks dengan link
teks_dengan_link = "Berikut adalah [link dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)."

# Menampilkan teks dengan link menggunakan st.markdown()
st.markdown(teks_dengan_link)

# Load data
day = pd.read_csv('day.csv')  # Ganti dengan path sesuai lokasi file day.csv
drop_col = ['instant', 'dteday']
for i in day.columns:
  if i in drop_col:
    day.drop(labels = i, axis=1, inplace=True)

day['weathersit'] = day['weathersit'].map({1: 'cerah', 2:'berawan', 3:'hujan ringan', 4:'hujan lebat'})
day['season'] = day['season'].map({1: 'spring', 2:'summer', 3:'fall', 4:'winter'})
day['weekday'] = day['weekday'].map({0:'minggu', 1:'senen', 2:'selasa', 3:'rabu', 4:'kamis', 5:'jumat', 6:'sabtu'})
day['mnth'] = day['mnth'].map({1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'mei', 6:'jun', 7:'jul', 8:'ags', 9:'sep', 10:'okt', 11:'nov', 12:'des'})

# Menampilkan 5 data pertama dari DataFrame day
st.table(day.head(5))
st.markdown(
  """
  Tabel diatas merupakan hasil dataset setelah dilakukan proses Data Wrangling, Saya hanya menampilkan 5 index dari dataset
  """
)

st.markdown("---")

cont_var = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered']

st.markdown("Tampilan dibawah ini adalah diagram yang menunjukan analisa yang saya lakukan")


# Create subplot grid 1
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
fig.suptitle('Analisis dasar dari target variabel (cnt)'.upper(), weight='bold', fontsize=24)

# Population plot 1
sns.boxplot(y=day['cnt'], ax=ax[0], palette='viridis')
ax[0].set_title('Boxplot menunjukan statistik dasar dari target variable'.upper(),
                fontsize=14, fontweight=16, y=1.02)
ax[0].set_ylabel(' ')
ax[0].set_xlabel(' ')

# Population plot 2
sns.distplot(day['cnt'], ax=ax[1], color='pink')
ax[1].set_title('Distribusi plot dari target variable (cnt)'.upper(),
                fontsize=14, fontweight=16, y=1.02)
ax[1].set_ylabel(' ')
ax[1].set_xlabel(' ')

plt.tight_layout()
st.pyplot(fig)  # Menampilkan subplot grid 1 di Streamlit

st.markdown("---")

# Create subplot grid 2
fig1, ax1 = plt.subplots(nrows=1, ncols=len(cont_var), figsize=(12, 5))
plt.suptitle('Boxplot trend cuaca'.upper(), fontsize=20)

for i in range(len(cont_var)):
    sns.boxplot(y=day[cont_var[i]], ax=ax1[i], palette='inferno')
    ax1[i].set_title(f'{cont_var[i].upper()}', fontsize=14)
    ax1[i].set_ylabel(' ')

plt.tight_layout()
st.pyplot(fig1)  # Menampilkan subplot grid 2 di Streamlit

st.markdown("---")

fig2, ax2= plt.subplots(nrows=1, ncols= len(cont_var), figsize=(40,10))
plt.suptitle('displot trend cuaca'.upper(), fontsize=20)

for i in range(len(cont_var)):
  sns.histplot(day[cont_var[i]], ax= ax2[i], color='green', label="100% Equities",  kde=True, stat="density", linewidth=0)
  ax2[i].set_title(f'{cont_var[i].upper()}', fontsize=14)
  ax2[i].set_ylabel(' ')
  ax2[i].set_xlabel(' ')

plt.tight_layout()
st.pyplot(fig2)

st.markdown("---")

st.title('Relasi Variabel'.upper())
st.subheader('Dalam diagram ini dilakukan pembanding dengan variabel Jumlah Sewa')
for var in cont_var:
    # Membuat subplot untuk setiap variabel kontinu
    fig3, ax3 = plt.subplots(figsize=(15, 5))
    sns.regplot(x=day[var], y=day['cnt'], scatter_kws={'color': 'yellow'}, line_kws={'color': 'red'})
    ax3.set_title(f'Relasi {var.upper()} dengan Jumlah Sewa', fontsize=16)
    ax3.set_ylabel('Jumlah Sewa')
    ax3.set_xlabel(var.upper())

    # Menampilkan setiap chart satu per satu
    st.pyplot(fig3)
    st.write("---")  # Garis pemisah antara setiap chart

#Pertanyaan Analisis Data
st.markdown(
  """
  Berdasarkan Exploratory Dataset tersebut terdapat beberapa pertanyaan bisnis, seperti
    - pertanyaan 1 : Bagaimana growth(pertumbuhan) dari perbandingan tahun 2011 dan 2012
    - pertanyaan 2 : Bagaimana hubungan antara musim dan jumlah sewa sepeda harian ?
    - pertanyaan 3 : Bagaimana pengaruh cuaca (weathersit) terhadap jumlah sewa sepeda harian?
  """
)

st.markdown(
  """
  Untuk menjawab pertanyaan Nomor 1, dapat dilihat bahwa perkembangan tertinggi berada pada bulan Maret antara tahun 2011 dan 2012
  """
)
growth_pd= day.pivot_table(index='mnth', columns='yr', values='cnt', aggfunc='mean')
growth_pd.columns=  ['2011','2012']
growth_pd['percent growth']= round(((growth_pd['2012']-growth_pd['2011'])/growth_pd['2011'])*100,2)
growth_pd= growth_pd.sort_values(by='percent growth', ascending = False)


st.table(growth_pd)
st.write("---")

data1 = {'mnth': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        '2011': [1231, 1721, 2065, 3162, 4381, 4783, 4559, 4409, 4247, 3984, 3405, 2816],
        '2012': [3120, 3556, 5318, 5807, 6318, 6761, 6567, 6919, 7285, 6414, 5088, 3990]}


growth_pd = pd.DataFrame(data1)
growth_pd.set_index('mnth', inplace=True)

# Menghitung persentase pertumbuhan
growth_pd['percent growth'] = round(((growth_pd['2012'] - growth_pd['2011']) / growth_pd['2011']) * 100, 2)

# Membuat diagram garis dengan Plotly Express
fig = px.line(growth_pd, x=growth_pd.index, y='percent growth',
              labels={'value': 'Pertumbuhan Persentase', 'index': 'Bulan'},
              title='Pertumbuhan Persentase Antara Tahun 2011 dan 2012',
              line_shape='linear', template='plotly_white',
              line_dash_sequence=['solid'], color_discrete_sequence=['green'])

# Menampilkan diagram garis di Streamlit
st.plotly_chart(fig)
st.write("---")

st.markdown(
  """
  Untuk menjawab pertanyaan Nomor 2, dapat di lihat bahwa jumlah sewa sepeda lebih banyak pada musim semi(Spring) dan terendah pada musim panas(Summer).

  """
)

data2 = {'season': ['Spring', 'Summer', 'Fall', 'Winter'],
        'cnt': [5500, 2500, 5000, 4800]}  # Gantilah dengan data sesuai dengan kebutuhan

day1 = pd.DataFrame(data2)

# Plotting bar chart
plt.bar(day1['season'], day1['cnt'])
plt.xlabel('Musim')
plt.ylabel('Rata-rata Jumlah Sewa Harian')
plt.title('Pengaruh Musim Terhadap Jumlah Sewa Sepeda Harian')

# Menampilkan grafik di Streamlit
st.bar_chart(day1.set_index('season'))

st.markdown("---")

st.markdown(
  """
  Untuk menjawab pertanyaan Nomor 3, dapat di lihat bahwa jumlah sewa sepeda tertinggi terjadi ketika cuaca cerah lalu disusul berawan dan hujan ringan. Hujan lebat disini menyebabkan tidak adanya penyewaan sepeda sama sekali
  """
)
# Proporsi setiap kategori pada variabel 'weathersit'
weathersit_counts = day['weathersit'].value_counts()

# Membuat pie chart dengan plotly
fig7 = px.pie(weathersit_counts, values=weathersit_counts.values, names=weathersit_counts.index,
             title='Proporsi Weathersit',
             color_discrete_sequence=['lightblue', 'lightgreen', 'lightcoral', 'lightgray'])

# Mengganti ukuran font title
fig7.update_layout(title_font=dict(size=24))

# Menambahkan informasi ketika kursor diarahkan ke bagian chart
fig7.update_traces(hoverinfo='label+percent+value')

# Menambahkan informasi jumlah sewa pada chart pie
fig7.update_layout(annotations=[
    dict(text=f"Total Sewa: {day['weathersit'].count()}", showarrow=False)
])
# Menampilkan chart pie menggunakan Streamlit
st.plotly_chart(fig7)



st.markdown("---")
st.caption('Richie Richardo 2023')