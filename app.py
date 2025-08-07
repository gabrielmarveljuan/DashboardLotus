import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# ========================
# Streamlit App Configuration
# ========================
st.set_page_config(layout="wide", page_title="Dashboard Analisis Penjualan")

st.sidebar.markdown("📤 **Upload File Laporan (per barang 5-7.xlsx - Report 01.csv)**")
uploaded_file = st.sidebar.file_uploader("Unggah file .csv", type=['csv'])

# ========================
# Load Data & Preprocessing (Diselaraskan dengan file baru)
# ========================
df = pd.DataFrame()
if uploaded_file:
    try:
        # Memuat file CSV yang diunggah, melewati 4 baris pertama yang berisi header tidak relevan
        df_raw = pd.read_csv(uploaded_file, skiprows=4)
        
        # Mengganti nama kolom agar mudah diakses
        df_raw.rename(columns={'NAMA BARANG': 'Nama Produk', 'TOTAL': 'Jumlah Terjual'}, inplace=True)
        
        # Membersihkan baris yang kosong atau tidak relevan di kolom 'Nama Produk'
        df = df_raw.dropna(subset=['Nama Produk']).copy()
        
    except Exception as e:
        st.error(f"Gagal memproses file. Terjadi kesalahan: {e}. Pastikan format file sesuai.")
        st.stop()
else:
    # Jika tidak ada file diunggah, gunakan file default (misalnya file yang Anda berikan)
    try:
        df_raw = pd.read_csv("per barang 5-7.xlsx - Report 01.csv", skiprows=4)
        df_raw.rename(columns={'NAMA BARANG': 'Nama Produk', 'TOTAL': 'Jumlah Terjual'}, inplace=True)
        df = df_raw.dropna(subset=['Nama Produk']).copy()
    except FileNotFoundError:
        st.info("Unggah file CSV untuk memulai analisis penjualan.")
        st.stop()
        
# --- Pembersihan Data (untuk kolom yang mungkin tidak ada) ---
if not df.empty:
    # Karena data baru tidak memiliki kolom 'Tanggal', 'Customer', 'Kota', dll.
    # kita hanya akan menampilkan analisis yang relevan.
    
    # Pastikan kolom 'Jumlah Terjual' adalah numerik
    df['Jumlah Terjual'] = pd.to_numeric(df['Jumlah Terjual'], errors='coerce')
    df = df.dropna(subset=['Jumlah Terjual'])
    
    # Aplikasikan Kategorisasi Produk (jika diperlukan)
    def categorize_products(product_list):
        # ... (fungsi categorize_products tetap sama seperti kode Anda)
        product_to_category_map = {}
        initial_categorization_list = {
            'Label & Sticker': [
                'LABEL BOOK STICKER FANCY'
            ],
            'Box & Storage': [
                'BOXFILE MEDIUM BF112 M.BLUE',
                'BOXFILE MEDIUM BF113 BLACK',
                'BOXFILE MEDIUM BF114 DARK BLUE',
                'BOXFILE MEDIUM BF115 RED',
                'BOXFILE MEDIUM BF116 GREEN',
                'BOX FILE MOTIF MUDA',
                'BOX FILE MARMER',
                'BOX FILE JUMBO BF 303 HITAM',
                'BOX FILE JUMBO BF 305 MERAH',
                'BOXFILE LACI BF603 HITAM',
                'BOXFILE LACI BF605 MERAH',
                'BOXFILE PESANAN JITU MASTER',
                'BOXFILE LACI COKLAT PESANAN',
                'BOX AKSESORIS PESANAN 30 X 20'
            ],
            'Display & Holder': [
                'D.BROSUR ACRILIC 10X21 HITAM',
                'D.BROSUR A4 3 SUSUN PESANAN',
                'BOYKO DB WALL A6',
                'BOYKO DB WALL A5',
                'BOYKO DISPLAY BROSUR MDF A6',
                'BOYKO D. BROSUR A6 + DECOVIL',
                'BOYKO DISPLAY BROSUR MDF A5',
                'BOYKO D. BROSUR A5 + DECOVIL',
                'D.BROSUR ACRILIC PUTIH F4',
                'D.BROSUR ACRILIC PUTIH A5',
                'D.BROSUR ACRILIC PUTIH A6',
                'BOYKO D.BROSUR ACR A6 2SUSUN',
                'BOYKO D.BROSUR ACR A5 2SUSUN',
                'BOYKO DESKSET ACR DS003',
                'BOYKO DEST SET 115 (1/2 L )',
                'BOYKO DESK SET 116',
                'BOYKO DESK SET 117',
                'BOYKO DESK SET 118',
                'DESKSET 180 ABS PEACH',
                'DESKSET 180 ABS ABU',
                'STAND UP SIGN HOLDER A5',
                'STAND UP SIGN HOLDER F4',
                'STAND UP SIGN HOLDER 10X12',
                'STAND UP HORISONTAL F4',
                'STAND UP HORISONTAL A5',
                'STAND UP HORISONTAL A4',
                'STAND UP SIGN 10X15',
                'STAND UP SIGN HOLDER A4',
                'ACR NOMER MEJA ALAS SEGITIGA',
                'STAND UP ALAS SEGITIGA',
                'LEAN SIGN HOLDER A5',
                'LEAN SIGN HOLDER F4',
                'LEAN SIGN HOLDER 10X12',
                'LEAN SIGN HOLDER A4',
                'LEAN SIGN HOLDER 11X21',
                'BOYKO SIGN HOLDER NO MEJA'
            ],
            'Signage & Name Plate': [
                'ACR BE OPEN-CLOSE RANTAI',
                'ACR BE BUKA-TUTUP RANTAI',
                'ACR BE BUKA-ISTIRAHAT RANTAI',
                'ACR BE BATAS SUCI',
                'ACR BE KASIR',
                'ACR BE HIMBAUAN',
                'ACR BE MUSHOLLA',
                'ACR BE JAGALAH KEBERSIHAN',
                'ACR BE SELAIN KRYWN',
                'ACR BE STAFF ONLY',
                'ACR BE DLRG PARKIR',
                'ACR BE TOLIET T/D',
                'ACR BE TOILET PRIA T/D',
                'ACR BE TOILET WNT T/D',
                'ACR BE NO SMOKING T/D',
                'ACR BE AREA MEROKOK T/D',
                'ACR BE ARAH KIBLAT (KIRI) T/D',
                'ACR BE ARAH KIBLAT (KANAN) T/D',
                'ACR BE DORONG',
                'ACR BE TARIK',
                'ACR BE GESER (KIRI)',
                'ACR BE GESER (KANAN)',
                'ACR BE TRMKSH TDK PRKR FOL',
                'ACR BE DRLG PARKIR FOL',
                'ACR BE CCTV 20X15',
                'ACR BE BUKA-TUTUP 20X15',
                'ACR BE TARIK DORONG',
                'ACRILIC BOYKO HIMBAUAN TOILET',
                'ACRILIC TOILET',
                'ACRILIC RUANGAN BER-AC',
                'ACR BUKA-TUTUP+RANTAI',
                'ACR. OPEN-CLOSE+RANTAI',
                'ACR. DILARANG.P.DPINTU',
                'ACRILIC KELUAR- MASUK',
                'ACR.RUANG BEBAS ASAP ROKOK',
                'ACR. JAGALAH KEBERSIHAN',
                'ACRILIC ANAK PANAH [SET]',
                'ACRILIC GESER [SET]',
                'ACRILIC BUKA-TUTUP FORMAL',
                'ACRILIC OPEN-CLOSE FORMAL',
                'ACRILIC TEMPAT WUDHU',
                'ACRILIC HP HRP DIMATIKAN',
                'ACRILIC KAMAR CEWEK',
                'ACRILIC KAMAR COWOK',
                'ACRILIC UKS',
                'ACRILIC RUANG TUNGGU',
                'ACRILIC RUANG KEPSEK',
                'ACRILIC KANTIN',
                'ACRLIC BATAS SUCI',
                'ACRILIC ARAH KIBLAT',
                'ACRILIC DILRG B\'BCR SKHTB',
                'ACRILIC RUANG KOMPUTER',
                'ACRILIC STAFF ONLY',
                'AC SELAIN KRYWN DILRG MSK',
                'ACRILIC TAMU HRP LAPOR SATPAM',
                'ACRILIC KLS I',
                'ACRILIC KLS II',
                'ACRILIC KLS III',
                'ACRILIC KLS IV',
                'ACRILIC KLS V',
                'ACRILIC KLS VI',
                'ACRILIC KLS IX',
                'ACR.ALAS KAKI HRP DILEPAS',
                'ACR.ISTIRAHAT BUKA +RANTAI',
                'ACRILIC AWAS KACA',
                'ACRILIC RUANG TU',
                'ACRILIC TOILET PRIA',
                'ACRILIC TOILET WANITA',
                'ACRILIC LADIES/WANITA 10X15',
                'ACRILIC GENT/PRIA 10X15',
                'ACR.D.MEROKOK/NO SMOKING',
                'ACRILIC OFFICE/KANTOR',
                'ACRILIC MUSHOLA [FORMAL]',
                'ACRILIC MUSHOLA',
                'ACRILIC KASIR',
                'ACRILIC FREE- WIFI',
                'ACR BUDAYAKAN MENGANTRI',
                'JAGA DAN AWASI BAWAAN ANDA',
                'ACRILIC BELL 10X15',
                'ACR. DILARANG MEMOTRET',
                'ACR AREA MEROKOK',
                'ACR BUANG SMPAH PD TMPT',
                'ACRYLIC EXIT (KANAN)',
                'ACRYLIC EXIT (KIRI)',
                'DILRG MEMBWA MAKANAN DR LUAR',
                'DILRG PARKIR DPN PNT UK.FOLIO',
                'ACR TITIK KUMPUL UK.FOLIO',
                'ACR PARKING AREA UK.FOLIO',
                'ACR APAR FIRE EXTING 10X15',
                'ACRILIC DISABILITAS 10X15',
                'ACRILIC NO PETS 10X15',
                'ACR CUCI TGN DGN SABUN 10X15',
                'ACR HRP CUCI TGN SBLM MSK',
                'ACR MASKER KU MASKER MU',
                'ACR JAGA JARAK AMAN 20X15',
                'ACR KAWASAN WAJIB MASKER 20X15',
                'ACR PROTOKOL 5M UK.FOLIO',
                'ACR CUTTING NO RUMAH 1',
                'ACR CUTTING NO RUMAH 2',
                'ACR CUTTING NO RUMAH 3',
                'ACR CUTTING NO RUMAH 4',
                'ACR CUTTING NO RUMAH 5',
                'ACR CUTTING NO RUMAH 6',
                'ACR CUTTING NO RUMAH 7',
                'ACR CUTTING NO RUMAH 8',
                'ACR CUTTING NO RUMAH 9',
                'ACR CUTTING NO RUMAH 0',
                'ACR FOSFOR EXIT',
                'ACR FOSFOR FOLIO DLRG P D PINT',
                'ACR FOSFOR FOLIO TITIK KUMPUL',
                'ACR FOS JLR EVAKUASI KANAN',
                'ACR FOS JLR EVAKUASI KIRI',
                'ACRILIC EXIT',
                'ACRYLIC SATPAM',
                'ACRILIC PERPUSTAKAAN',
                'ACRILIC RUANG GURU',
                'ACRILIC TOILET (KANAN)',
                'ACRILIC TOILET (KIRI)',
                'ACRILIC T/D PUSH PULL [SET]',
                'ACR. TEMPAT WUDHU PRIA',
                'ACR. TEMPAT WUDHU WANITA',
                'ACRILIC JALUR EVAKUASI (KANAN)',
                'ACRILIC JALUR EVAKUASI (KIRI)',
                'ACR BUKA SHOLAT+RANTAI',
                'ACRILIC CCTV 20 X 15',
                'ACR WELCOME-THANKS 20X15',
                'ACR L/G BUKA-TUTUP +RANTAI',
                'ACR L/G OPEN-CLOSE +RANTAI',
                'ACRYLIC TOILET 20X15',
                'ACRILIC TEGANGAN TINGGI 20X15',
                'ACR BORMA BUANG SMPAH PD TMPT',
                'ACR DILRG MENGINJAK RUMPUT',
                'ACR DLRG BUANG PUNTUNG KETOILT',
                'ACRILIC GANTUNGAN KUNCI',
                'ACRILIC WALL PESANAN 40X60',
                'ACRILIC NAME PLATE 7 X 10',
                'ACRILIC NAME PLATE B/B 7X10',
                'ACRILIC NAME PLATE 7 X 15',
                'ACRILIC NAME PLATE B/B 7X15',
                'ACRILIC NAME PLATE 7X20',
                'ACRILIC NAME PLATE B/B 7X20',
                'ACRILIC NAME PLATE B/B 7 X 30',
                'ACRILIC NAME PLATE 7 X 30',
                'ACRILIC NAME PLATE 7  X 25',
                'ACRILIC NAME PLATE  7 X 25 B/B',
                'ACRILIC NAME PLATE LEAN 7X10',
                'ACRILIC NAME PLATE LEAN 7X15',
                'ACRILIC NAME PLATE LEAN 7X30',
                'ACRILIC NAME PLATE LEAN 6X25',
                'ACRILIC NAME PLATE LEAN 7X20',
                'ACRILIC NAME PLATE LEAN 7X25',
                'NAME PLATE MEIKO 8X25BB',
                'NAME PLATE MEIKO 8X30BB',
                'NAME PLATE WALL 8X25',
                'NAME PLATE WALL 8 X 35',
                'NAME PLATE WALL 8X35 + RANTAI',
                'ACRILIC NO RUMAH 0',
                'ACRILIC NO RUMAH 1',
                'ACRILIC NO RUMAH 2',
                'ACRILIC NO RUMAH 3',
                'ACRILIC NO RUMAH 4',
                'ACRILIC NO RUMAH 5',
                'ACRILIC NO RUMAH 6',
                'ACRILIC NO RUMAH 7',
                'ACRILIC NO RUMAH 8',
                'ACRILIC NO RUMAH 9',
                'ACRILIC NO RUMAH A',
                'ACRILIC NO RUMAH B',
                'ACRILIC NO RUMAH C',
                'ACRILIC NO RUMAH D',
                'ACRILIC NO RUMAH E',
                'ACRILIC NO RUMAH F',
                'ACRILIC NO RUMAH G',
                'ACRYLIC DILARANG MEROKOK 10X15',
                'DILRG BUANG SMPH TOILET 10X15',
                'ACR MATIKAN KERAN AIR 10X15',
                'ACRILIC NO RUMAH H',
                'ACRILIC NO RUMAH I',
                'ACRILIC NO RUMAH J',
                'ACRILIC NO RUMAH K',
                'ACRILIC NO RUMAH L',
                'ACRILIC NO RUMAH M',
                'ACRILIC NO RUMAH N',
                'ACRILIC NO RUMAH O',
                'ACRILIC NO RUMAH P',
                'ACRILIC NO RUMAH Q',
                'ACRILIC NO RUMAH R',
                'ACRILIC NO RUMAH S',
                'ACRILIC NO RUMAH T',
                'ACRILIC NO RUMAH U',
                'ACRILIC NO RUMAH V',
                'ACRILIC NO RUMAH W',
                'ACRILIC NO RUMAH X',
                'ACRILIC NO RUMAH Y',
                'ACRILIC NO RUMAH Z',
                'ACR JGLH KBRSIHAN T/D',
                'ACR NO SMOKING  T/D',
                'ACR AREA MEROKOK T/D',
                'ACR ARAH KIBLAT (KANAN) T/D',
                'ACR ARAH KIBLAT (KIRI) T/D',
                'ACR KASIR T/D',
                'ACR ORDER HERE T/D',
                'ACR TOILET T/D',
                'ACR TOILET PRIA T/D',
                'ACR TOILET WANITA T/D',
                'ACR TEMPAT WUDHU T/D',
                'ACR BATAS SUCI T/D',
                'ACR MUSHOLLA T/D',
                'ACR STAFF ONLY T/D',
                'AC OFFICE T/D',
                'ACR GESER HORIZON (KANAN) T/D',
                'ACR GESER HORIZON (KIRI) T/D',
                'ACR RECEPTION T/D',
                'ACR SECURITY T/D',
                'ACR TAMU HRP LAPOR T/D',
                'ACR DILRG MASUK T/D',
                'ACR CCTV T/D',
                'ACR BELL 20X5',
                'ACR KASIR 20X5 BORMA',
                'ACR TAMU HRP 20X5 BORMA',
                'ACR SECURITY 20X5 BORMA',
                'ACR DLRG MSK 20X5 BORMA',
                'ACR DILRG MEROKOK T/D',
                'ACR.PINTU HRP DITTUP KMBLI',
                'ACR OFFICE T/D'
            ],
            'Peralatan Kantor': [
                'CLIBOARD BOYKO MELAMINE PUTIH',
                'KLIB BOYKO LETTERING SERIES',
                'TUSUKAN BON',
                'DUAL BOARD BOYKO ( BARU)',
                'EASEL STAND BOYKO',
                'ACRYLIC WHITE BOARD 90 X120'
            ],
            'Alat Sekolah': [
                'LEM  KECIL BOYKO',
                'LEM TANGGUNG BOYKO',
                'BOYKO PENCASE MIKA JARING',
                'BOYKO PENCASE BULAT JARING',
                'BOYKO CASE BULAT JARING W/BAND',
                'BOYKO PENCASE 2WR KECIL',
                'BOYKO PENCASE 2WR BESAR',
                'PENCIL CASE MOTIF TIMBUL',
                'BOYKO PENCIL CASE RESLETING'
            ],
            'Packaging & Adhesives': [
                'JAGO CLEAR 2" X 90Y',
                'BUBBLE TAPE ISOLASI 1X100 YARD',
                'BUBBLE TAPE TAN (COKLAT) 2"'
            ],
            'Miscellaneous': [
                'PAPAN METERAN MDF BOYKO',
                'PAPAN METERAN NUMERIC BOYKO',
                'MASKER ICHINOSE EARLOOP BLACK'
            ],
            'Rak & Aksesoris Meja': [
                'RAK ACRILIC PUTAR',
                'RAK ACRYLIC BONGKAR PASANG',
                'RAK ACRYLIC UKURAN TD',
                'RAK LUBANG 16.5 X 10.3 X 5',
                'BOYKO RAK SPIDOL ACRILIC',
                'RAK BOLPOIN EVERLYN [ATAS]',
                'RAK BOLPOIN EVERLYN [BAWAH]',
                'RAK BOLPOIN UD. MANTEP PACITAN'
            ],
            'Custom Order': [
                'ACR PESANAN 10 X 25 + SIKU BES',
                'ACR PESANAN 28 X 8',
                'ACR PESANAN 24 X 8',
                'ACR PESANAN 40 X 25',
                'ACRILIC PESANAN 30 X 11',
                'ACR PESANAN 20X5',
                'ACRILIC PESANAN UK 10X15',
                'ACR PESANAN 9X25',
                'ACR PESANAN 9X25 + RANTAI',
                'ACR PESANAN 20X15',
                'ACR PESANAN FOLIO',
                'ACRILIC PESANAN UK 40X15'
            ]
        }
        product_to_category_map = {}
        for category, products in initial_categorization_list.items():
            for product in products:
                product_to_category_map[product] = category
        for product in product_list:
            if product in product_to_category_map:
                continue
            product_lower = product.lower()
            assigned = False
            if 'pesanan' in product_lower or 'custom' in product_lower:
                product_to_category_map[product] = 'Custom Order'
                assigned = True
            if not assigned and 'rak' in product_lower:
                product_to_category_map[product] = 'Rak & Aksesoris Meja'
                assigned = True
            if not assigned:
                product_to_category_map[product] = 'Miscellaneous'
        return product_to_category_map
    
    # Get unique product names from the loaded file
    all_unique_products = df['Nama Produk'].unique().tolist()
    product_to_category_map = categorize_products(all_unique_products)
    
    # Apply mapping
    df['Kategori'] = df['Nama Produk'].map(product_to_category_map).fillna('Uncategorized')

# ========================
# Sidebar: Global Filters
# ========================
if not df.empty:
    available_categories = sorted(df['Kategori'].unique())
    kategori_filter = st.sidebar.multiselect(
        "📂 Kategori Produk",
        options=available_categories,
        default=available_categories # Select all by default
    )
    
    filtered_df = df[df['Kategori'].isin(kategori_filter)].copy()
    
    if filtered_df.empty:
        st.warning("Tidak ada data yang cocok dengan filter yang dipilih. Harap sesuaikan filter.")
        st.stop()

    # ========================
    # KPI Summary
    # ========================
    with st.expander("📊 Ringkasan Kinerja (KPI)"):
        total_penjualan = filtered_df['Jumlah Terjual'].sum()
        total_produk = filtered_df['Nama Produk'].nunique()

        col1, col2 = st.columns(2)
        col1.metric("📦 Produk Terjual", total_penjualan)
        col2.metric("📋 Produk Unik", total_produk)

    # ========================
    # Analysis Menu Options
    # ========================
    st.title("📈 Dashboard Analisis Penjualan")
    menu = st.selectbox(
        "📌 Pilih Jenis Analisis:",
        [
            "Top 3 Produk Terlaris",
            "Top 3 Produk Terendah",
            "Produk Deadstock"
        ]
    )

    # ========================
    # Analysis based on menu selection
    # ========================

    # 1. Top Produk Terlaris
    if menu == "Top 3 Produk Terlaris":
        st.header("🏆 Top 3 Produk Terlaris per Kategori")
        # Ensure 'Jumlah Terjual' is numeric
        top_products = filtered_df.groupby(['Kategori', 'Nama Produk'])['Jumlah Terjual'].sum().reset_index()
        top3 = top_products.sort_values(['Kategori', 'Jumlah Terjual'], ascending=[True, False]).groupby('Kategori').head(3)
        st.dataframe(top3, use_container_width=True)

    # 2. Top Produk Terendah
    elif menu == "Top 3 Produk Terendah":
        st.header("⬇️ Top 3 Produk Penjualan Terendah per Kategori")
        # Ensure 'Jumlah Terjual' is numeric
        low_products = filtered_df.groupby(['Kategori', 'Nama Produk'])['Jumlah Terjual'].sum().reset_index()
        low3 = low_products.sort_values(['Kategori', 'Jumlah Terjual'], ascending=[True, True]).groupby('Kategori').head(3)
        st.dataframe(low3, use_container_width=True)

    # 3. Produk Deadstock
    elif menu == "Produk Deadstock":
        st.header("📦 Produk Deadstock (Jumlah Terjual = 0)")
        # Menggunakan df asli yang sudah dimuat dari file laporan untuk mencari deadstock, 
        # karena file ini berisi daftar semua produk, termasuk yang tidak laku.
        deadstock_df = df[df['Jumlah Terjual'] == 0]
        
        if not deadstock_df.empty:
            st.dataframe(deadstock_df[['Nama Produk', 'Jumlah Terjual', 'Kategori']], use_container_width=True)
        else:
            st.info("Tidak ada produk deadstock yang ditemukan.")

else:
    st.info("Unggah file CSV untuk memulai analisis penjualan."

    # 4. Segmentasi Wilayah
    elif menu == "Segmentasi Wilayah":
        st.header("🌍 Segmentasi Penjualan Berdasarkan Kota")
        if 'Kota' in filtered_df.columns:
            sales_by_city = pd.pivot_table(filtered_df, values='Jumlah Terjual', index='Nama Produk', columns='Kota', aggfunc='sum', fill_value=0)
            st.dataframe(sales_by_city, use_container_width=True)
        else:
            st.warning("Kolom 'Kota' tidak ditemukan dalam data. Pastikan data memiliki informasi kota.")

    # 5. Tren Penjualan Bulanan
    elif menu == "Tren Penjualan Bulanan":
        st.header("📆 Tren Penjualan Bulanan")
        monthly_sales = filtered_df.groupby('Bulan')['Total Harga'].sum().reset_index()
        # Ensure correct sorting of months
        monthly_sales['Bulan_Sort'] = pd.to_datetime(monthly_sales['Bulan'])
        monthly_sales = monthly_sales.sort_values('Bulan_Sort').drop('Bulan_Sort', axis=1)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(monthly_sales['Bulan'], monthly_sales['Total Harga'], marker='o', linestyle='-', color='skyblue')
        ax.set_title('Tren Penjualan Bulanan', fontsize=16)
        ax.set_xlabel('Bulan', fontsize=12)
        ax.set_ylabel('Total Penjualan (Rp)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout() # Adjust layout to prevent labels from overlapping
        st.pyplot(fig)

    # 6. Klasifikasi ABC
    elif menu == "Klasifikasi ABC":
        st.header("🏷️ Klasifikasi ABC (Pareto 80/15/5)")
        abc_df = filtered_df.groupby('Nama Produk')['Total Harga'].sum().reset_index()
        abc_df = abc_df.sort_values(by='Total Harga', ascending=False)
        
        # Handle case where total_harga_sum is zero to avoid division by zero
        total_harga_sum = abc_df['Total Harga'].sum()
        if total_harga_sum == 0:
            st.warning("Total penjualan adalah nol, tidak dapat melakukan klasifikasi ABC.")
            st.stop()

        abc_df['Persentase'] = 100 * abc_df['Total Harga'] / total_harga_sum
        abc_df['Kumulatif'] = abc_df['Persentase'].cumsum()

        def assign_abc(kumulatif):
            if kumulatif <= 80:
                return 'A'
            elif kumulatif <= 95:
                return 'B'
            else:
                return 'C'

        abc_df['Kelas ABC'] = abc_df['Kumulatif'].apply(assign_abc)

        st.subheader("📈 Ringkasan Jumlah Produk & Kontribusi")
        abc_summary = abc_df.groupby('Kelas ABC').agg(
            Jumlah_Produk=('Nama Produk', 'count'),
            Total_Penjualan=('Total Harga', 'sum')
        ).reset_index()
        
        abc_summary['Kontribusi (%)'] = 100 * abc_summary['Total_Penjualan'] / total_harga_sum
        st.dataframe(abc_summary.round(2), use_container_width=True) # Round for better display

        st.subheader("📋 Detail Produk per Kelas ABC")
        kelas_order_abc = ['A', 'B', 'C'] # Define explicit order
        for kelas in kelas_order_abc:
            kelas_df = abc_df[abc_df['Kelas ABC'] == kelas]
            st.markdown(f"**Kelas {kelas}** — {len(kelas_df)} Produk")
            st.dataframe(kelas_df[['Nama Produk', 'Total Harga', 'Persentase', 'Kumulatif']].round(2), use_container_width=True)

    # 7. Repeat Order Pelanggan
    elif menu == "Repeat Order Pelanggan":
        st.header("🔁 Repeat Order Pelanggan")
        # Use filtered_df directly as it already applies month range
        repeat_df = filtered_df.copy() 
        
        metode = st.radio(
            "📌 Metode Analisis Loyalitas",
            ["Berdasarkan Hari Unik", "Berdasarkan Total Transaksi"],
            horizontal=True
        )

        trx_summary = repeat_df.groupby('Customer').agg(
            Jumlah_Hari_Transaksi=('Tanggal_Hari', 'nunique'),
            Jumlah_Total_Transaksi=('Tanggal', 'count'),
            Total_Belanja=('Total Harga', 'sum')
        ).reset_index()

        def klasifikasi_hari(hari):
            if hari >= 4:
                return 'Kelas 1 (Sangat Loyal)'
            elif hari == 3:
                return 'Kelas 2 (Loyal)'
            elif hari == 2:
                return 'Kelas 3 (Potensial Loyal)'
            else:
                return 'Kelas 4 (Baru)'

        def klasifikasi_total(trx):
            if trx >= 4:
                return 'Kelas 1 (Sangat Loyal)'
            elif trx == 3:
                return 'Kelas 2 (Loyal)'
            elif trx == 2:
                return 'Kelas 3 (Potensial Loyal)'
            else:
                return 'Kelas 4 (Baru)'

        trx_summary['Kelas'] = trx_summary['Jumlah_Hari_Transaksi'].apply(klasifikasi_hari) if metode == "Berdasarkan Hari Unik" else trx_summary['Jumlah_Total_Transaksi'].apply(klasifikasi_total)

        st.subheader("📈 Ringkasan Jumlah Customer per Kelas")
        ringkasan = trx_summary.groupby('Kelas')['Customer'].count().reset_index(name='Jumlah Customer')
        # Ensure consistent order for display
        kelas_order = ['Kelas 1 (Sangat Loyal)', 'Kelas 2 (Loyal)', 'Kelas 3 (Potensial Loyal)', 'Kelas 4 (Baru)']
        ringkasan['Kelas'] = pd.Categorical(ringkasan['Kelas'], categories=kelas_order, ordered=True)
        ringkasan = ringkasan.sort_values('Kelas')
        st.dataframe(ringkasan, use_container_width=True)

        st.subheader("📋 Daftar Customer per Kelas")
        for kelas in kelas_order:
            data_kelas = trx_summary[trx_summary['Kelas'] == kelas]
            if not data_kelas.empty:
                daftar_customer = '; '.join(sorted(data_kelas['Customer'].tolist()))
                st.markdown(f"**{kelas}** — {len(data_kelas)} customer")
                st.code(daftar_customer, language='text')
            else:
                st.markdown(f"**{kelas}** — Tidak ada customer")
else:
    st.info("Unggah file Excel untuk memulai analisis penjualan.")
