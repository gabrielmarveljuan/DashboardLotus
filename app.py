import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# Helper: Extract Dynamic Data
# ========================
def extract_sales_data_dynamic(df_raw):
    try:
        # Temukan baris header berdasarkan kemunculan "TGL NOTA"
        header_row_idx = df_raw[df_raw.apply(lambda row: row.astype(str).str.contains("TGL NOTA", na=False).any(), axis=1)].index[0]
        df = df_raw.iloc[header_row_idx + 1:].copy()
        df.columns = df_raw.iloc[header_row_idx]
        df = df.reset_index(drop=True)

        records = []
        current_date = None
        current_customer = None
        current_kota = None

        for _, row in df.iterrows():
            try:
                if pd.to_datetime(row['TGL NOTA'], errors='coerce') is not pd.NaT:
                    current_date = pd.to_datetime(row['TGL NOTA'])
                    current_customer = row['NAMA CUSTOMER']
                    current_kota = row['KOTA']
                else:
                    nama_produk = row['TGL NOTA']
                    jumlah = row['KD LGN']
                    harga_satuan = row['NAMA CUSTOMER']
                    if pd.notna(nama_produk) and pd.notna(jumlah):
                        records.append({
                            'Tanggal': current_date,
                            'Customer': current_customer,
                            'Kota': current_kota,
                            'Nama Produk': str(nama_produk).strip(),
                            'Jumlah Terjual': int(jumlah),
                            'Harga Satuan': int(harga_satuan),
                            'Total Harga': int(harga_satuan) * int(jumlah),
                            'Bulan': current_date.to_period('M').strftime('%Y-%m')
                        })
            except Exception:
                continue

        return pd.DataFrame(records)
    except Exception as e:
        st.warning(f"Gagal memproses file: {e}")
        return pd.DataFrame()

# ========================
# Helper: Product Categorization (New Function)
# ========================
def categorize_products(product_list):
    """
    Mengkategorikan produk berdasarkan daftar kategori yang telah ditentukan
    dan menggunakan kata kunci untuk 'Rak & Aksesoris Meja' dan 'Custom Order'.

    Args:
        product_list (list): Daftar nama produk.

    Returns:
        dict: Kamus kategori produk.
    """

    product_categories = {
        'Label & Sticker': [],
        'Box & Storage': [],
        'Display & Holder': [],
        'Signage & Name Plate': [],
        'Rak & Aksesoris Meja': [],
        'Peralatan Kantor': [],
        'Alat Sekolah': [],
        'Packaging & Adhesives': [],
        'Custom Order': [],
        'Miscellaneous': []
    }

    initial_categorization = {
        'LABEL BOOK STICKER FANCY': 'Label & Sticker',

        'BOXFILE MEDIUM BF112 M.BLUE': 'Box & Storage',
        'BOXFILE MEDIUM BF113 BLACK': 'Box & Storage',
        'BOXFILE MEDIUM BF114 DARK BLUE': 'Box & Storage',
        'BOXFILE MEDIUM BF115 RED': 'Box & Storage',
        'BOXFILE MEDIUM BF116 GREEN': 'Box & Storage',
        'BOX FILE MOTIF MUDA': 'Box & Storage',
        'BOX FILE MARMER': 'Box & Storage',
        'BOX FILE JUMBO BF 303 HITAM': 'Box & Storage',
        'BOX FILE JUMBO BF 305 MERAH': 'Box & Storage',
        'BOXFILE LACI BF603 HITAM': 'Box & Storage',
        'BOXFILE LACI BF605 MERAH': 'Box & Storage',
        'BOX AKSESORIS PESANAN 30 X 20': 'Box & Storage', 

        'D.BROSUR ACRILIC 10X21 HITAM': 'Display & Holder',
        'D.BROSUR A4 3 SUSUN PESANAN': 'Display & Holder',
        'BOYKO DB WALL A6': 'Display & Holder',
        'BOYKO DB WALL A5': 'Display & Holder',
        'BOYKO DISPLAY BROSUR MDF A6': 'Display & Holder',
        'BOYKO D. BROSUR A6 + DECOVIL': 'Display & Holder',
        'BOYKO DISPLAY BROSUR MDF A5': 'Display & Holder',
        'BOYKO D. BROSUR A5 + DECOVIL': 'Display & Holder',
        'D.BROSUR ACRILIC PUTIH F4': 'Display & Holder',
        'D.BROSUR ACRILIC PUTIH A5': 'Display & Holder',
        'D.BROSUR ACRILIC PUTIH A6': 'Display & Holder',
        'BOYKO D.BROSUR ACR A6 2SUSUN': 'Display & Holder',
        'BOYKO D.BROSUR ACR A5 2SUSUN': 'Display & Holder',
        'BOYKO DESKSET ACR DS003': 'Display & Holder',
        'BOYKO DEST SET 115 (1/2 L )': 'Display & Holder',
        'BOYKO DESK SET 116': 'Display & Holder',
        'BOYKO DESK SET 117': 'Display & Holder',
        'BOYKO DESK SET 118': 'Display & Holder',
        'DESKSET 180 ABS PEACH': 'Display & Holder',
        'DESKSET 180 ABS ABU': 'Display & Holder',
        'STAND UP SIGN HOLDER A5': 'Display & Holder',
        'STAND UP SIGN HOLDER F4': 'Display & Holder',
        'STAND UP SIGN HOLDER 10X12': 'Display & Holder',
        'STAND UP HORISONTAL F4': 'Display & Holder',
        'STAND UP HORISONTAL A5': 'Display & Holder',
        'STAND UP HORISONTAL A4': 'Display & Holder',
        'STAND UP SIGN 10X15': 'Display & Holder',
        'STAND UP SIGN HOLDER A4': 'Display & Holder',
        'ACR NOMER MEJA ALAS SEGITIGA': 'Display & Holder',
        'STAND UP ALAS SEGITIGA': 'Display & Holder',
        'LEAN SIGN HOLDER A5': 'Display & Holder',
        'LEAN SIGN HOLDER F4': 'Display & Holder',
        'LEAN SIGN HOLDER 10X12': 'Display & Holder',
        'LEAN SIGN HOLDER A4': 'Display & Holder',
        'LEAN SIGN HOLDER 11X21': 'Display & Holder',
        'BOYKO SIGN HOLDER NO MEJA': 'Display & Holder',

        # Signage & Name Plate (banyak yang spesifik)
        'ACR BE OPEN-CLOSE RANTAI': 'Signage & Name Plate',
        'ACR BE BUKA-TUTUP RANTAI': 'Signage & Name Plate',
        'ACR BE BUKA-ISTIRAHAT RANTAI': 'Signage & Name Plate',
        'ACR BE BATAS SUCI': 'Signage & Name Plate',
        'ACR BE KASIR': 'Signage & Name Plate',
        'ACR BE HIMBAUAN': 'Signage & Name Plate',
        'ACR BE MUSHOLLA': 'Signage & Name Plate',
        'ACR BE JAGALAH KEBERSIHAN': 'Signage & Name Plate',
        'ACR BE SELAIN KRYWN': 'Signage & Name Plate',
        'ACR BE STAFF ONLY': 'Signage & Name Plate',
        'ACR BE DLRG PARKIR': 'Signage & Name Plate',
        'ACR BE TOLIET T/D': 'Signage & Name Plate',
        'ACR BE TOILET PRIA T/D': 'Signage & Name Plate',
        'ACR BE TOILET WNT T/D': 'Signage & Name Plate',
        'ACR BE NO SMOKING T/D': 'Signage & Name Plate',
        'ACR BE AREA MEROKOK T/D': 'Signage & Name Plate',
        'ACR BE ARAH KIBLAT (KIRI) T/D': 'Signage & Name Plate',
        'ACR BE ARAH KIBLAT (KANAN) T/D': 'Signage & Name Plate',
        'ACR BE DORONG': 'Signage & Name Plate',
        'ACR BE TARIK': 'Signage & Name Plate',
        'ACR BE GESER (KIRI)': 'Signage & Name Plate',
        'ACR BE GESER (KANAN)': 'Signage & Name Plate',
        'ACR BE TRMKSH TDK PRKR FOL': 'Signage & Name Plate',
        'ACR BE DRLG PARKIR FOL': 'Signage & Name Plate',
        'ACR BE CCTV 20X15': 'Signage & Name Plate',
        'ACR BE BUKA-TUTUP 20X15': 'Signage & Name Plate',
        'ACR BE TARIK DORONG': 'Signage & Name Plate',
        'ACRILIC BOYKO HIMBAUAN TOILET': 'Signage & Name Plate',
        'ACRILIC TOILET': 'Signage & Name Plate',
        'ACRILIC RUANGAN BER-AC': 'Signage & Name Plate',
        'ACR BUKA-TUTUP+RANTAI': 'Signage & Name Plate',
        'ACR. OPEN-CLOSE+RANTAI': 'Signage & Name Plate',
        'ACR. DILARANG.P.DPINTU': 'Signage & Name Plate',
        'ACRILIC KELUAR- MASUK': 'Signage & Name Plate',
        'ACR.RUANG BEBAS ASAP ROKOK': 'Signage & Name Plate',
        'ACR. JAGALAH KEBERSIHAN': 'Signage & Name Plate',
        'ACRILIC ANAK PANAH [SET]': 'Signage & Name Plate',
        'ACRILIC GESER [SET]': 'Signage & Name Plate',
        'ACRILIC BUKA-TUTUP FORMAL': 'Signage & Name Plate',
        'ACRILIC OPEN-CLOSE FORMAL': 'Signage & Name Plate',
        'ACRILIC TEMPAT WUDHU': 'Signage & Name Plate',
        'ACRILIC HP HRP DIMATIKAN': 'Signage & Name Plate',
        'ACRILIC KAMAR CEWEK': 'Signage & Name Plate',
        'ACRILIC KAMAR COWOK': 'Signage & Name Plate',
        'ACRILIC UKS': 'Signage & Name Plate',
        'ACRILIC RUANG TUNGGU': 'Signage & Name Plate',
        'ACRILIC RUANG KEPSEK': 'Signage & Name Plate',
        'ACRILIC KANTIN': 'Signage & Name Plate',
        'ACRLIC BATAS SUCI': 'Signage & Name Plate',
        'ACRILIC ARAH KIBLAT': 'Signage & Name Plate',
        'ACRILIC DILRG B\'BCR SKHTB': 'Signage & Name Plate',
        'ACRILIC RUANG KOMPUTER': 'Signage & Name Plate',
        'ACRILIC STAFF ONLY': 'Signage & Name Plate',
        'AC SELAIN KRYWN DILRG MSK': 'Signage & Name Plate',
        'ACRILIC TAMU HRP LAPOR SATPAM': 'Signage & Name Plate',
        'ACRILIC KLS I': 'Signage & Name Plate',
        'ACRILIC KLS II': 'Signage & Name Plate',
        'ACRILIC KLS III': 'Signage & Name Plate',
        'ACRILIC KLS IV': 'Signage & Name Plate',
        'ACRILIC KLS V': 'Signage & Name Plate',
        'ACRILIC KLS VI': 'Signage & Name Plate',
        'ACRILIC KLS IX': 'Signage & Name Plate',
        'ACR.ALAS KAKI HRP DILEPAS': 'Signage & Name Plate',
        'ACR.ISTIRAHAT BUKA +RANTAI': 'Signage & Name Plate',
        'ACRILIC AWAS KACA': 'Signage & Name Plate',
        'ACRILIC RUANG TU': 'Signage & Name Plate',
        'ACRILIC TOILET PRIA': 'Signage & Name Plate',
        'ACRILIC TOILET WANITA': 'Signage & Name Plate',
        'ACRILIC LADIES/WANITA 10X15': 'Signage & Name Plate',
        'ACRILIC GENT/PRIA 10X15': 'Signage & Name Plate',
        'ACR.D.MEROKOK/NO SMOKING': 'Signage & Name Plate',
        'ACRILIC OFFICE/KANTOR': 'Signage & Name Plate',
        'ACRILIC MUSHOLA [FORMAL]': 'Signage & Name Plate',
        'ACRILIC MUSHOLA': 'Signage & Name Plate',
        'ACRILIC KASIR': 'Signage & Name Plate',
        'ACRILIC FREE- WIFI': 'Signage & Name Plate',
        'ACR BUDAYAKAN MENGANTRI': 'Signage & Name Plate',
        'JAGA DAN AWASI BAWAAN ANDA': 'Signage & Name Plate',
        'ACRILIC BELL 10X15': 'Signage & Name Plate',
        'ACR. DILARANG MEMOTRET': 'Signage & Name Plate',
        'ACR AREA MEROKOK': 'Signage & Name Plate',
        'ACR BUANG SMPAH PD TMPT': 'Signage & Name Plate',
        'ACRYLIC EXIT (KANAN)': 'Signage & Name Plate',
        'ACRYLIC EXIT (KIRI)': 'Signage & Name Plate',
        'DILRG MEMBWA MAKANAN DR LUAR': 'Signage & Name Plate',
        'DILRG PARKIR DPN PNT UK.FOLIO': 'Signage & Name Plate',
        'ACR TITIK KUMPUL UK.FOLIO': 'Signage & Name Plate',
        'ACR PARKING AREA UK.FOLIO': 'Signage & Name Plate',
        'ACR APAR FIRE EXTING 10X15': 'Signage & Name Plate',
        'ACRILIC DISABILITAS 10X15': 'Signage & Name Plate',
        'ACRILIC NO PETS 10X15': 'Signage & Name Plate',
        'ACR CUCI TGN DGN SABUN 10X15': 'Signage & Name Plate',
        'ACR HRP CUCI TGN SBLM MSK': 'Signage & Name Plate',
        'ACR MASKER KU MASKER MU': 'Signage & Name Plate',
        'ACR JAGA JARAK AMAN 20X15': 'Signage & Name Plate',
        'ACR KAWASAN WAJIB MASKER 20X15': 'Signage & Name Plate',
        'ACR PROTOKOL 5M UK.FOLIO': 'Signage & Name Plate',
        'ACR CUTTING NO RUMAH 1': 'Signage & Name Plate',
        'ACR CUTTING NO RUMAH 2': 'Signage & Name Plate',
        'ACR CUTTING NO RUMAH 3': 'Signage & Name Plate',
        'ACR CUTTING NO RUMAH 4': 'Signage & Name Plate',
        'ACR CUTTING NO RUMAH 5': 'Signage & Name Plate',
        'ACR CUTTING NO RUMAH 6': 'Signage & Name Plate',
        'ACR CUTTING NO RUMAH 7': 'Signage & Name Plate',
        'ACR CUTTING NO RUMAH 8': 'Signage & Name Plate',
        'ACR CUTTING NO RUMAH 9': 'Signage & Name Plate',
        'ACR CUTTING NO RUMAH 0': 'Signage & Name Plate',
        'ACR FOSFOR EXIT': 'Signage & Name Plate',
        'ACR FOSFOR FOLIO DLRG P D PINT': 'Signage & Name Plate',
        'ACR FOSFOR FOLIO TITIK KUMPUL': 'Signage & Name Plate',
        'ACR FOS JLR EVAKUASI KANAN': 'Signage & Name Plate',
        'ACR FOS JLR EVAKUASI KIRI': 'Signage & Name Plate',
        'ACRILIC EXIT': 'Signage & Name Plate',
        'ACRYLIC SATPAM': 'Signage & Name Plate',
        'ACRILIC PERPUSTAKAAN': 'Signage & Name Plate',
        'ACRILIC RUANG GURU': 'Signage & Name Plate',
        'ACRILIC TOILET (KANAN)': 'Signage & Name Plate',
        'ACRILIC TOILET (KIRI)': 'Signage & Name Plate',
        'ACRILIC T/D PUSH PULL [SET]': 'Signage & Name Plate',
        'ACR. TEMPAT WUDHU PRIA': 'Signage & Name Plate',
        'ACR. TEMPAT WUDHU WANITA': 'Signage & Name Plate',
        'ACRILIC JALUR EVAKUASI (KANAN)': 'Signage & Name Plate',
        'ACRILIC JALUR EVAKUASI (KIRI)': 'Signage & Name Plate',
        'ACR BUKA SHOLAT+RANTAI': 'Signage & Name Plate',
        'ACRILIC CCTV 20 X 15': 'Signage & Name Plate',
        'ACR WELCOME-THANKS 20X15': 'Signage & Name Plate',
        'ACR L/G BUKA-TUTUP +RANTAI': 'Signage & Name Plate',
        'ACR L/G OPEN-CLOSE +RANTAI': 'Signage & Name Plate',
        'ACRYLIC TOILET 20X15': 'Signage & Name Plate',
        'ACRILIC TEGANGAN TINGGI 20X15': 'Signage & Name Plate',
        'ACR BORMA BUANG SMPAH PD TMPT': 'Signage & Name Plate',
        'ACR DILRG MENGINJAK RUMPUT': 'Signage & Name Plate',
        'ACR DLRG BUANG PUNTUNG KETOILT': 'Signage & Name Plate',
        'ACRILIC GANTUNGAN KUNCI': 'Signage & Name Plate',
        'ACRILIC WALL PESANAN 40X60': 'Signage & Name Plate',
        'ACRILIC NAME PLATE 7 X 10': 'Signage & Name Plate',
        'ACRILIC NAME PLATE B/B 7X10': 'Signage & Name Plate',
        'ACRILIC NAME PLATE 7 X 15': 'Signage & Name Plate',
        'ACRILIC NAME PLATE B/B 7X15': 'Signage & Name Plate',
        'ACRILIC NAME PLATE 7X20': 'Signage & Name Plate',
        'ACRILIC NAME PLATE B/B 7X20': 'Signage & Name Plate',
        'ACRILIC NAME PLATE B/B 7 X 30': 'Signage & Name Plate',
        'ACRILIC NAME PLATE 7 X 30': 'Signage & Name Plate',
        'ACRILIC NAME PLATE 7 X 25': 'Signage & Name Plate',
        'ACRILIC NAME PLATE  7 X 25 B/B': 'Signage & Name Plate',
        'ACRILIC NAME PLATE LEAN 7X10': 'Signage & Name Plate',
        'ACRILIC NAME PLATE LEAN 7X15': 'Signage & Name Plate',
        'ACRILIC NAME PLATE LEAN 7X30': 'Signage & Name Plate',
        'ACRILIC NAME PLATE LEAN 6X25': 'Signage & Name Plate',
        'ACRILIC NAME PLATE LEAN 7X20': 'Signage & Name Plate',
        'ACRILIC NAME PLATE LEAN 7X25': 'Signage & Name Plate',
        'NAME PLATE MEIKO 8X25BB': 'Signage & Name Plate',
        'NAME PLATE MEIKO 8X30BB': 'Signage & Name Plate',
        'NAME PLATE WALL 8X25': 'Signage & Name Plate',
        'NAME PLATE WALL 8 X 35': 'Signage & Name Plate',
        'NAME PLATE WALL 8X35 + RANTAI': 'Signage & Name Plate',
        'ACRILIC NO RUMAH 0': 'Signage & Name Plate',
        'ACRILIC NO RUMAH 1': 'Signage & Name Plate',
        'ACRILIC NO RUMAH 2': 'Signage & Name Plate',
        'ACRILIC NO RUMAH 3': 'Signage & Name Plate',
        'ACRILIC NO RUMAH 4': 'Signage & Name Plate',
        'ACRILIC NO RUMAH 5': 'Signage & Name Plate',
        'ACRILIC NO RUMAH 6': 'Signage & Name Plate',
        'ACRILIC NO RUMAH 7': 'Signage & Name Plate',
        'ACRILIC NO RUMAH 8': 'Signage & Name Plate',
        'ACRILIC NO RUMAH 9': 'Signage & Name Plate',
        'ACRILIC NO RUMAH A': 'Signage & Name Plate',
        'ACRILIC NO RUMAH B': 'Signage & Name Plate',
        'ACRILIC NO RUMAH C': 'Signage & Name Plate',
        'ACRILIC NO RUMAH D': 'Signage & Name Plate',
        'ACRILIC NO RUMAH E': 'Signage & Name Plate',
        'ACRILIC NO RUMAH F': 'Signage & Name Plate',
        'ACRILIC NO RUMAH G': 'Signage & Name Plate',
        'ACRYLIC DILARANG MEROKOK 10X15': 'Signage & Name Plate',
        'DILRG BUANG SMPH TOILET 10X15': 'Signage & Name Plate',
        'ACR MATIKAN KERAN AIR 10X15': 'Signage & Name Plate',
        'ACRILIC NO RUMAH H': 'Signage & Name Plate',
        'ACRILIC NO RUMAH I': 'Signage & Name Plate',
        'ACRILIC NO RUMAH J': 'Signage & Name Plate',
        'ACRILIC NO RUMAH K': 'Signage & Name Plate',
        'ACRILIC NO RUMAH L': 'Signage & Name Plate',
        'ACRILIC NO RUMAH M': 'Signage & Name Plate',
        'ACRILIC NO RUMAH N': 'Signage & Name Plate',
        'ACRILIC NO RUMAH O': 'Signage & Name Plate',
        'ACRILIC NO RUMAH P': 'Signage & Name Plate',
        'ACRILIC NO RUMAH Q': 'Signage & Name Plate',
        'ACRILIC NO RUMAH R': 'Signage & Name Plate',
        'ACRILIC NO RUMAH S': 'Signage & Name Plate',
        'ACRILIC NO RUMAH T': 'Signage & Name Plate',
        'ACRILIC NO RUMAH U': 'Signage & Name Plate',
        'ACRILIC NO RUMAH V': 'Signage & Name Plate',
        'ACRILIC NO RUMAH W': 'Signage & Name Plate',
        'ACRILIC NO RUMAH X': 'Signage & Name Plate',
        'ACRILIC NO RUMAH Y': 'Signage & Name Plate',
        'ACRILIC NO RUMAH Z': 'Signage & Name Plate',
        'ACR JGLH KBRSIHAN T/D': 'Signage & Name Plate',
        'ACR NO SMOKING  T/D': 'Signage & Name Plate',
        'ACR AREA MEROKOK T/D': 'Signage & Name Plate',
        'ACR ARAH KIBLAT (KANAN) T/D': 'Signage & Name Plate',
        'ACR ARAH KIBLAT (KIRI) T/D': 'Signage & Name Plate',
        'ACR KASIR T/D': 'Signage & Name Plate',
        'ACR ORDER HERE T/D': 'Signage & Name Plate',
        'ACR TOILET T/D': 'Signage & Name Plate',
        'ACR TOILET PRIA T/D': 'Signage & Name Plate',
        'ACR TOILET WANITA T/D': 'Signage & Name Plate',
        'ACR TEMPAT WUDHU T/D': 'Signage & Name Plate',
        'ACR BATAS SUCI T/D': 'Signage & Name Plate',
        'ACR MUSHOLLA T/D': 'Signage & Name Plate',
        'ACR STAFF ONLY T/D': 'Signage & Name Plate',
        'AC OFFICE T/D': 'Signage & Name Plate',
        'ACR GESER HORIZON (KANAN) T/D': 'Signage & Name Plate',
        'ACR GESER HORIZON (KIRI) T/D': 'Signage & Name Plate',
        'ACR RECEPTION T/D': 'Signage & Name Plate',
        'ACR SECURITY T/D': 'Signage & Name Plate',
        'ACR TAMU HRP LAPOR T/D': 'Signage & Name Plate',
        'ACR DILRG MASUK T/D': 'Signage & Name Plate',
        'ACR CCTV T/D': 'Signage & Name Plate',
        'ACR BELL 20X5': 'Signage & Name Plate',
        'ACR KASIR 20X5 BORMA': 'Signage & Name Plate',
        'ACR TAMU HRP 20X5 BORMA': 'Signage & Name Plate',
        'ACR SECURITY 20X5 BORMA': 'Signage & Name Plate',
        'ACR DLRG MSK 20X5 BORMA': 'Signage & Name Plate',
        'ACR DILRG MEROKOK T/D': 'Signage & Name Plate',

        'CLIBOARD BOYKO MELAMINE PUTIH': 'Peralatan Kantor',
        'KLIB BOYKO LETTERING SERIES': 'Peralatan Kantor',
        'TUSUKAN BON': 'Peralatan Kantor',
        'DUAL BOARD BOYKO ( BARU)': 'Peralatan Kantor',
        'EASEL STAND BOYKO': 'Peralatan Kantor',
        'ACRYLIC WHITE BOARD 90 X120': 'Peralatan Kantor',

        'LEM KECIL BOYKO': 'Alat Sekolah',
        'LEM TANGGUNG BOYKO': 'Alat Sekolah',
        'BOYKO PENCASE MIKA JARING': 'Alat Sekolah',
        'BOYKO PENCASE BULAT JARING': 'Alat Sekolah',
        'BOYKO CASE BULAT JARING W/BAND': 'Alat Sekolah',
        'BOYKO PENCASE 2WR KECIL': 'Alat Sekolah',
        'BOYKO PENCASE 2WR BESAR': 'Alat Sekolah',
        'PENCIL CASE MOTIF TIMBUL': 'Alat Sekolah',
        'BOYKO PENCIL CASE RESLETING': 'Alat Sekolah',

        'JAGO CLEAR 2" X 90Y': 'Packaging & Adhesives',
        'BUBBLE TAPE ISOLASI 1X100 YARD': 'Packaging & Adhesives',
        'BUBBLE TAPE TAN (COKLAT) 2"': 'Packaging & Adhesives',

        'PAPAN METERAN MDF BOYKO': 'Miscellaneous',
        'PAPAN METERAN NUMERIC BOYKO': 'Miscellaneous',
        'MASKER ICHINOSE EARLOOP BLACK': 'Miscellaneous'
    }

    # Isi kategori dengan produk dari initial_categorization
    for product, category in initial_categorization.items():
        if product not in product_categories[category]: # Avoid re-adding if already there for some reason
            product_categories[category].append(product)

    # Proses sisa produk dan terapkan aturan kata kunci
    # Menggunakan set untuk nama produk yang sudah dikategorikan untuk efisiensi
    categorized_product_names = set(p for sublist in product_categories.values() for p in sublist)

    for product in product_list:
        if product in categorized_product_names:
            continue # Skip if already categorized by initial_categorization

        product_lower = product.lower()
        
        assigned_to_keyword_category = False

        # Prioritas: Custom Order
        if 'pesanan' in product_lower or 'custom' in product_lower:
            product_categories['Custom Order'].append(product)
            categorized_product_names.add(product)
            assigned_to_keyword_category = True
        
        # Prioritas: Rak & Aksesoris Meja (jika belum masuk custom order)
        if not assigned_to_keyword_category and 'rak' in product_lower:
            product_categories['Rak & Aksesoris Meja'].append(product)
            categorized_product_names.add(product)
            assigned_to_keyword_category = True
            
        # Jika produk belum terkategorikan oleh initial_categorization atau kata kunci,
        # tambahkan ke Miscellaneous (jika belum ada di categorized_product_names)
        if not assigned_to_keyword_category and product not in categorized_product_names:
            product_categories['Miscellaneous'].append(product)
            categorized_product_names.add(product)

    return product_categories


# ========================
# Sidebar: Upload File
# ========================
st.sidebar.markdown("📤 **Upload File Penjualan (Excel - bisa banyak file)**")
uploaded_files = st.sidebar.file_uploader("Unggah file .xlsx", type=['xlsx'], accept_multiple_files=True)

# ========================
# Load & Combine Data
# ========================
if uploaded_files:
    all_data = []
    for file in uploaded_files:
        df_raw = pd.read_excel(file, header=None)
        df_cleaned = extract_sales_data_dynamic(df_raw)
        if not df_cleaned.empty:
            all_data.append(df_cleaned)
    if all_data:
        df = pd.concat(all_data, ignore_index=True)
    else:
        st.stop()
else:
    # Gunakan data default (pastikan 'penjualan_bersih.csv' ada)
    try:
        df = pd.read_csv("penjualan_bersih.csv")
    except FileNotFoundError:
        st.error("File 'penjualan_bersih.csv' tidak ditemukan. Harap unggah file Excel.")
        st.stop()

# --- PENAMBAHAN KODE DI SINI ---
# Filter out "Padma Utama" from the DataFrame
if 'Customer' in df.columns:
    df = df[df['Customer'].astype(str).str.lower() != 'padma utama jadi cv']
    if df.empty:
        st.warning("Setelah memfilter 'Padma Utama', tidak ada data yang tersisa untuk dianalisis.")
        st.stop()
# --- AKHIR PENAMBAHAN KODE ---


# ========================
# Apply New Categorization
# ========================
# Dapatkan daftar unik nama produk dari DataFrame
all_unique_products = df['Nama Produk'].unique().tolist()

# Lakukan kategorisasi menggunakan fungsi baru
categorized_product_dict = categorize_products(all_unique_products)

# Buat kamus pemetaan (mapping) produk ke kategori
product_to_category_map = {}
for category, products in categorized_product_dict.items():
    for product in products:
        product_to_category_map[product] = category

# Terapkan kategori ke DataFrame
df['Kategori'] = df['Nama Produk'].map(product_to_category_map).fillna('Uncategorized')


# Pastikan kolom Tanggal memiliki format datetime
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df['Tanggal_Hari'] = df['Tanggal'].dt.date
df['Bulan_Tahun'] = df['Tanggal'].dt.to_period('M').astype(str)

# ========================
# Sidebar: Filter Global
# ========================
bulan_list = sorted(df['Bulan'].unique())
bulan_dari = st.sidebar.selectbox("📆 Bulan Mulai", bulan_list, index=0)
bulan_sampai = st.sidebar.selectbox("📆 Bulan Sampai", bulan_list, index=len(bulan_list) - 1)
kategori_filter = st.sidebar.multiselect("📂 Kategori Produk", options=sorted(df['Kategori'].unique()), default=df['Kategori'].unique())

bulan_range = bulan_list[bulan_list.index(bulan_dari):bulan_list.index(bulan_sampai) + 1]
filtered_df = df[df['Bulan'].isin(bulan_range) & df['Kategori'].isin(kategori_filter)]

# ========================
# KPI Ringkasan
# ========================
with st.expander("📊 Ringkasan Kinerja (KPI)"):
    total_penjualan = filtered_df['Total Harga'].sum()
    total_transaksi = filtered_df.shape[0]
    total_customer = filtered_df['Customer'].nunique()
    total_produk = filtered_df['Nama Produk'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Penjualan", f"Rp {total_penjualan:,.0f}".replace(",", "."))
    col2.metric("🛒 Total Transaksi", total_transaksi)
    col3.metric("👥 Customer Unik", total_customer)
    col4.metric("📦 Produk Terjual", total_produk)

# ========================
# Pilihan Menu Analisis
# ========================
st.title("📈 Dashboard Analisis Penjualan")
menu = st.selectbox(
    "📌 Pilih Jenis Analisis:",
    [
        "Top 3 Produk Terlaris",
        "Top 3 Produk Terendah",
        "Produk Deadstock",
        "Segmentasi Wilayah",
        "Tren Penjualan Bulanan",
        "Klasifikasi ABC",
        "Repeat Order Pelanggan"
    ]
)

# ========================
# Analisis berdasarkan menu
# ========================

# 1. Top Produk Terlaris
if menu == "Top 3 Produk Terlaris":
    st.header("🏆 Top 3 Produk Terlaris per Kategori")
    top_products = filtered_df.groupby(['Kategori', 'Nama Produk'])['Jumlah Terjual'].sum().reset_index()
    top3 = top_products.sort_values(['Kategori', 'Jumlah Terjual'], ascending=[True, False]).groupby('Kategori').head(3)
    st.dataframe(top3, use_container_width=True)

# 2. Top Produk Terendah
elif menu == "Top 3 Produk Terendah":
    st.header("⬇️ Top 3 Produk Penjualan Terendah per Kategori")
    low_products = filtered_df.groupby(['Kategori', 'Nama Produk'])['Jumlah Terjual'].sum().reset_index()
    low3 = low_products.sort_values(['Kategori', 'Jumlah Terjual'], ascending=[True, True]).groupby('Kategori').head(3)
    st.dataframe(low3, use_container_width=True)

# 3. Produk Deadstock
elif menu == "Produk Deadstock":
    st.header("📦 Produk Deadstock (Jumlah Terjual ≤ 10)")
    produk_dead = filtered_df.groupby('Nama Produk')['Jumlah Terjual'].sum()
    deadstock = produk_dead[produk_dead <= 10].reset_index()
    st.dataframe(deadstock, use_container_width=True)

# 4. Segmentasi Wilayah
elif menu == "Segmentasi Wilayah":
    st.header("🌍 Segmentasi Penjualan Berdasarkan Kota")
    sales_by_city = pd.pivot_table(filtered_df, values='Jumlah Terjual', index='Nama Produk', columns='Kota', aggfunc='sum', fill_value=0)
    st.dataframe(sales_by_city, use_container_width=True)

# 5. Tren Penjualan Bulanan
elif menu == "Tren Penjualan Bulanan":
    st.header("📆 Tren Penjualan Bulanan")
    monthly_sales = filtered_df.groupby('Bulan')['Total Harga'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.plot(monthly_sales['Bulan'], monthly_sales['Total Harga'], marker='o')
    ax.set_title('Tren Penjualan Bulanan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Total Penjualan')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 6. Klasifikasi ABC
elif menu == "Klasifikasi ABC":
    st.header("🏷️ Klasifikasi ABC (Pareto 80/15/5)")
    abc_df = filtered_df.groupby('Nama Produk')['Total Harga'].sum().reset_index()
    abc_df = abc_df.sort_values(by='Total Harga', ascending=False)
    abc_df['Persentase'] = 100 * abc_df['Total Harga'] / abc_df['Total Harga'].sum()
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
    total_all = abc_df['Total Harga'].sum()
    abc_summary['Kontribusi (%)'] = 100 * abc_summary['Total_Penjualan'] / total_all
    st.dataframe(abc_summary, use_container_width=True)

    st.subheader("📋 Detail Produk per Kelas ABC")
    for kelas in ['A', 'B', 'C']:
        kelas_df = abc_df[abc_df['Kelas ABC'] == kelas]
        st.markdown(f"**Kelas {kelas}** — {len(kelas_df)} Produk")
        st.dataframe(kelas_df[['Nama Produk', 'Total Harga', 'Persentase', 'Kumulatif']], use_container_width=True)

# 7. Repeat Order Pelanggan
elif menu == "Repeat Order Pelanggan":
    st.header("🔁 Repeat Order Pelanggan")
    repeat_df = df[df['Bulan'].isin(bulan_range)]
    metode = st.radio("📌 Metode Analisis Loyalitas", ["Berdasarkan Hari Unik", "Berdasarkan Total Transaksi"], horizontal=True)

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
    st.dataframe(ringkasan, use_container_width=True)

    st.subheader("📋 Daftar Customer per Kelas")
    kelas_order = ['Kelas 1 (Sangat Loyal)', 'Kelas 2 (Loyal)', 'Kelas 3 (Potensial Loyal)', 'Kelas 4 (Baru)']
    for kelas in kelas_order:
        data_kelas = trx_summary[trx_summary['Kelas'] == kelas]
        if not data_kelas.empty:
            daftar_customer = '; '.join(sorted(data_kelas['Customer'].tolist()))
            st.markdown(f"**{kelas}** — {len(data_kelas)} customer")
            st.code(daftar_customer, language='text')
        else:
            st.markdown(f"**{kelas}** — Tidak ada customer")
