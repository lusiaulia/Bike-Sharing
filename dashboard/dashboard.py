import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='white')

# Load cleaned data
hour_df = pd.read_csv("Hour.csv")
day_df = pd.read_csv("Day.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

# Filter data
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

#jam
hr_df = hour_df.groupby(by="hr").agg({
    "casual": "sum",
    "registered": "sum"
}) 
hr_df = hr_df.rename_axis('Jam')
#hari
weekday = day_df.groupby(by="weekday").agg({
    "casual": "sum",
    "registered": "sum"
})
weekday.index = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis','Jumat','Sabtu']
#bulan
month_df = day_df.groupby(by="mnth").agg({
    "casual": "sum",
    "registered": "sum"
})
month_df = month_df.rename_axis('Bulan')
month_df.index = ['Jan', 'Feb', 'Mar', 'April',
            'Mei', 'Juni', 'Juli', 'Agu', 'Sept', 'Okt', 'Nov', 'Des']

with st.sidebar:
    st.header("Bike Sharing")
    st.image("bbk.jpg")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]


st.header('Bike Sharing')
st.subheader("1. Plot Keterkaitan Waktu(Jam, Hari, Bulan) terhadap Jumlah Pengendara")
tab1, tab2, tab3= st.tabs(["Jam", "Hari", "Bulan"])

with tab1:
    st.subheader("Jumlah Pengendara per Jam")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        hr_df,
        marker='o', 
        linewidth=4,
        )
    ax.legend(['Casual','Registered'])
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)
    with st.expander("Lihat Penjelasan"):
        st.write(
            """
            Aktivitas jumlah pengendara terbanyak berdasar jam terlihat pada pukul 08:00 dan 17:00 
            pada grafik pengendara 'Terdaftar'. Kemungkinan hal tersebut terjadi dikarenakan waktu tersebut merupakan waktu berangkat dan pulang para pekerja. Kemudian terlihat baik kedua plot 'Casual' 
            dan 'Terdaftar' menunjukkan aktivitas pengendara meningkat saat di jam kerja 
            (08:00 - 17:00) dan menurun di luar jam tersebut. Jika dibandingkan antara jumlah pengendara 'Casual' dan 'Terdaftar', pengendara 'Terdaftar' memiliki jumlah yang lebih banyak.""")


with tab2:
    st.subheader("Jumlah Pengendara per Hari")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        weekday,
        marker='o', 
        linewidth=4,
    )
    ax.legend(['Casual','Registered'])
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)
    with st.expander("Lihat Penjelasan"):
        st.write(
        """
        Hal menarik terlihat pada plot jumlah 
        pengendara per hari dalam seminggu, terlihat 
        plot aktivitas jumlah pengendara 'Casual' dan 
        'Terdaftar' saling berkebalikan. Plot pengendara 
        'Casual' cekung ke atas dengan hari Sabtu dan 
        Minggu memiliki jumlah pengendara terbanyak. 
        Kemudian plot pengendara 'Terdaftar' cekung ke bawah, 
        dengan hari Sabtu dan Minggu memiliki jumlah pengendara 
        tersedikit dibanding hari-hari lainnya. Menunjukkan pengendara 'Teregistrasi' 
        lebih sering menggunakan sepeda dibanding dengan pengendara 'Casual',
        sehingga masuk akal jika lebih menguntungkan menjadi pengendara 'Teregistrasi'. 
        Pengendara 'Casual' sendiri lebih banyak menggunakan sepeda pada hari 
        libur (weekend : umumnya hari Sabtu dan Minggu). Tergantung tujuan penggunaan 
        dan tempat, lonjakan pada hari Sabtu dan Minggu bisa oleh pengendara 'Casual' 
        seperti penggunaan singkat sepeda di tempat wisata, 
        acara olahraga atau sekedar menikmati weekends dengan bersepeda. Untuk hari kerja, 
        penggunaan sepeda memungkinkan pekerja lebih mudah terhindar kemacetan atau 
        alternative kendaraan mencapai tempat kerja, serta merupakan
        bentuk kepedulian terhadap lingkungan. Namun, tentu masih ada pekerja yang sering 
        menggunakan sepeda tanpa menjadi pengendara 'Terdaftar'. """
        )   

with tab3:
    st.subheader("Jumlah Pengendara per Bulan")
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        month_df,
        marker='o', 
        linewidth=4,
    )
    ax.legend(['Casual','Registered'])
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)
    with st.expander("Lihat Penjelasan"):
        st.write(
        """ Plot pengendara 'Casual' dan 'Terdaftar' memiliki pola yang hampir sama kali ini, 
        keduanya menunjukkan aktivitas paling sedikit bersepeda pada bulan Desember - Februari, 
        dan tertinggi pada bulan Juni-Agustus. 
        Hal ini juga dipengaruhi oleh lokasi dan musim yang terjadi pada bulan-bulan tersebut.
        """
        )

st.subheader("2. Cuaca & Musim terhadap Jumlah Pengendara")
#musim
season_df= day_df.groupby(by="season").agg({
    "casual": "sum",
    "registered": "sum"
})
season_df = season_df.reset_index()
season = ['musim semi','musim panas', 'musim gugur', 'musim dingin']
for i in range(len(season_df)):
  season_df.season[i] = season[i]

#cuaca
weather_df = hour_df.groupby(by="weathersit").agg({
    "casual": "sum",
    "registered": "sum"
})
weather_df.index = ['Cerah', 'Berkabut', 'Bersalju', 'Hujan Deras']
weather_df = weather_df.rename_axis('Cuaca')

col1, col2 = st.columns(2)
with col1:
    st.caption("Jumlah Pengunjung per Cuaca")
    st.bar_chart(weather_df)  
    with st.expander("Lihat Penjelasan"):
        st.write(
        """ 
        Cuaca cerah merupakan hari yang menyenangkan untuk bersepeda, tentu saja jika di banding dengan cuaca berkabut, bersalju, apalagi hujan deras. 
        Grafik menunjukkan perbedaan signifikan antara cuaca cerah dengan cuaca lainnya. 
        """
        )


with col2:
    st.caption("Terbanyak dan Sedikit Jumlah Pengunjung Berdasar Musim")
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))

    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(x='season', y='casual',data=season_df.sort_values(by='casual',ascending=False), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Pengunjung Casual Terbanyak", loc="center", fontsize=10)
    ax[0].tick_params(axis ='y', labelsize=15)

    sns.barplot(x='season', y='registered',data=season_df.sort_values(by='registered',ascending=False), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("Pengunjung Terdaftar Terbanyak", loc="center", fontsize=10)
    ax[1].tick_params(axis ='y', labelsize=15)

    plt.suptitle("Jumlah Pengunjung Terbanyak Berdasar Musim", fontsize=12)
    st.pyplot(fig)

    with st.expander("Lihat Penjelasan"):
        s_df= day_df.groupby(by="season").agg({
        "casual": "count",
        "registered": "count"
        })
        s_df = s_df.reset_index()
        season = ['musim semi','musim panas', 'musim gugur', 'musim dingin']
        for i in range(len(s_df)):
            s_df.season[i] = season[i]
        st.table(data=s_df) 
        st.write(
        """
        Musim gugur memiliki jumlah pengendara terbanyak disusul dengan musim panas, musim dingin, dan musim semi. 
        Hal ini juga selaras dengan bedanya durasi tiap musim, terlihat musim gugur memiliki 188 hari (31 hari rata-rata tiap bulan, perhitungan terkadang bisa lebih atau kurang dari 3 bulan tergantung situasi). 
        Dibandingkan dengan musim dingin dengan 178 hari (29 hari rata-rata tiap bulan). 
        Tiap musim juga memiliki karakteristik masing-masing yang menyebabkan minat seseorang 
        untuk menaiki sepeda juga berbeda, seperti musim gugur merupakan waktu yang baik untuk bersepeda dikarenakan 
        suhunya yang cukup stabil dibanding musim semi. 
        Disusul pemandangan musim gugur yang indah, serta waktu beraktivitas setelah liburan musim panas. Musim panas juga, identik dengan libur sekolah dan cuacanya yang hangat membuat 
        meningkatnya aktivitas luar ruangan. Destinasi wisata yang banyak dikunjungi hingga festival musim panas yang diadakan di beragam daerah. Pada musim dingin, sepeda pun menjadi
        alternative terhindar dari kemacetan atau sulitnya akses jalan menunju lokasi sekolah atau kerja. Kemudian musim semi, memiliki cuaca yang cenderung tidak stabil karena merupakan musim transisi dari musim dingin ke musim panas, 
        jika hujan turun maka sesuai dengan grafik cuaca 'Hujan' memiliki tingkat pengendara paling sedikit.   
        
        """
        )   

st.subheader("3. Hari-hari tertentu terhadap jumlah pengendara")
#holiday
holiday = day_df.groupby(by="holiday").agg({
    "casual": "sum",
    "registered": "sum"
})
holiday.index = ['libur',' tidak libur']

#working
working = day_df.groupby(by="workingday").agg({
    "casual": "sum",
    "registered": "sum"
})
working.index = ['hari kerja', 'tidak']

col1, col2 = st.columns(2)
with col1:
    st.caption("Hari Libur terhadap Jumlah Pengendara")
    st.bar_chart(holiday)  
    with st.expander("Lihat Penjelasan"):
        st.write(
        """ 
        Hari libur didefinisikan sebagai hari weekend beserta hari libur nasional, 
        hari libur memiliki jumlah pengendara jauh lebih banyak dibanding tidak libur. 
        Hal ini bisa diakibatkan pengguna mengisi kegiatan libur dengan berolahraga sepeda (dibanding hari kerja mengingat jika jarak 
        tempat kerja cukup jauh tidak efektif menggunakan sepeda), ataupun berwisata. Jumlah pengendara 'Terdaftar' memiliki porsi lebih banyak dibanding pengendara 'Casual'.
        """
        )


with col2:
    st.caption("Hari Kerja terhadap Jumlah Pengendara")
    st.bar_chart(working)  
    with st.expander("Lihat Penjelasan"):
        st.write(
        """
        Memiliki pola yang sama dengan grafik hari libur, terlihat kebalikannya yakni hari kerja memiliki tingkat pengendara 
        lebih sedikit dibanding dengan bukan hari kerja. Terlihat juga masih terdapat pengendara 'Casual' dengan bagian lebih sedikit dibanding pengendara 'Terdaftar'.
        """)

st.subheader("4. Pemanfaatan media untuk Mempengaruhi Pengendara 'Casual' Agar Menjadi Pengendara 'Terdaftar'")
st.image('sosmed.png', width= 400, caption= 'Sosial Media, source : pngtree.com')
with st.expander("Lihat Penjelasan"):
    st.write(
    """
    Media menjadi salah satu langkah yang dapat digunakan untuk meningkatkan jumlah pengendara 'Terdaftar'.  Beberapa hal yang dapat dilakukan melalui media baik 
    sosial media maupun media lainnya (seperti koran, iklan, poster, baliho, dll) yaitu : 

    1. Melihat jumlah pengendara (khususnya pengendara 'Casual') terbanyak terjadi pada waktu kerja (08:00 - 17:00), hari libur, dan musim tertentu. Sehingga dapat dilakukan 
    promo ataupun diskon musiman pada waktu tersebut untuk pengendara 'Terdaftar' misalnya selama libur musim panas. Lalu informasi tersebut bisa diletakkan ditempat ramai pengendara sepeda seperti 
    stasiun sepeda ataupun lokasi wisata. 
    2. Selain promo musiman, promo di hari libur khusus Sabtu dan Minggu juga merupakan langkah yang baik. Promo ini bisa juga disebarluaskan melalui media sosial akun stasiun sepeda ataupun pada event khusus bersepeda, sekaligus mengangkat tema hidup sehat dan menjaga lingkungan sebagai branding penyepeda agar lebih menarik simpati masyarakat. 
    3. Promosi terhadap kalangan pengguna tertentu, seperti pelajar dan pekerja. Contohnya untuk pengguna 'Terdaftar' khusus pelajar bisa memperoleh potongan sekian % untuk berlangganan selama sekian waktu. Hal ini lebih efisien dipilih dibanding dengan pengendara 'Casual' yang harus
    membayar dengan harga normal dan lebih mahal jika sering menggunakan jasa sepedanya. 
    """)

st.subheader("Feedback")
values = st.slider(
    label='Gimana Dashboardnya? Hayuk beri nilai! (Skala 0: tidak menarik, tidak informatif. 1: menarik, informatif)',
    min_value=0, max_value=100, value=(0, 100))
st.write('Nilai:', values)
st.caption('Terima kasih ^_^')

st.caption('Submission Proyek Akhir-Lusi Aulia Jati')
