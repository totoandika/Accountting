import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman Utama
st.set_page_config(page_title="FinAnlytica Enterprise - Rupiah & AI Engine", layout="wide")
st.title("📈 FinAnlytica Enterprise: Pencatatan Transaksi & Analisis AI")

# Konteks Tanggal untuk Umur Piutang (Pertengahan 2026)
today = pd.to_datetime('2026-06-29')

# --- 1. DATABASE DUMMY INVOICE (PENDAPATAN JANUARI - JUNI) ---
if 'invoices' not in st.session_state:
    st.session_state.invoices = pd.DataFrame([
        {'Invoice_ID': 'INV-001', 'Client': 'Alpha Corp', 'Due_Date': '2026-05-31', 'Amount': 50000000.0, 'Tax_Rate_%': 10, 'Status': 'Paid'},
        {'Invoice_ID': 'INV-002', 'Client': 'Beta LLC', 'Due_Date': '2026-07-01', 'Amount': 35000000.0, 'Tax_Rate_%': 10, 'Status': 'Unpaid'},
        {'Invoice_ID': 'INV-003', 'Client': 'Gamma Inc', 'Due_Date': '2026-05-15', 'Amount': 12000000.0, 'Tax_Rate_%': 5, 'Status': 'Unpaid'},
        {'Invoice_ID': 'INV-004', 'Client': 'Delta Co', 'Due_Date': '2026-03-10', 'Amount': 25000000.0, 'Tax_Rate_%': 10, 'Status': 'Unpaid'},
    ])
    st.session_state.invoices['Due_Date'] = pd.to_datetime(st.session_state.invoices['Due_Date'])

# --- 2. DATABASE DUMMY EXPENSE (PENGELUARAN JANUARI - JUNI) ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame([
        {'Expense_ID': 'EXP-001', 'Vendor': 'AWS Cloud', 'Category': 'Software/Tech', 'Date': '2026-06-01', 'Amount': 4000000.0, 'Tax_Paid': 400000.0, 'Receipt': 'Uploaded'},
        {'Expense_ID': 'EXP-002', 'Vendor': 'WeWork', 'Category': 'Rent/Office', 'Date': '2026-06-05', 'Amount': 15000000.0, 'Tax_Paid': 1500000.0, 'Receipt': 'Uploaded'},
        {'Expense_ID': 'EXP-003', 'Vendor': 'Google Ads', 'Category': 'Marketing', 'Date': '2026-06-15', 'Amount': 6000000.0, 'Tax_Paid': 0.0, 'Receipt': 'Missing'},
    ])
    st.session_state.expenses['Date'] = pd.to_datetime(st.session_state.expenses['Date'])

# Fungsi dekorator warna tabel untuk kuitansi yang hilang
def highlight_missing_receipt(val):
    color = '#ffcccc' if val == 'Missing' else ''
    return f'background-color: {color}'

# Menyalin data untuk pemrosesan sesi saat ini
inv_df = st.session_state.invoices.copy()
exp_df = st.session_state.expenses.copy()

# --- KALKULASI FINANSIAL & PAJAK ---
# Perhitungan Sisi Pendapatan / Invoice
inv_df['Tax_Collected'] = inv_df['Amount'] * (inv_df['Tax_Rate_%'] / 100)
total_collected_tax = inv_df[inv_df['Status'] == 'Paid']['Tax_Collected'].sum()
total_pending_tax = inv_df[inv_df['Status'] == 'Unpaid']['Tax_Collected'].sum()
gross_tax_liability = total_collected_tax + total_pending_tax

# Perhitungan Sisi Pengeluaran
total_expenses_value = exp_df['Amount'].sum()
total_tax_offsets = exp_df['Tax_Paid'].sum()

# Mesin Penghitung Bersih Utang Pajak (Offset Engine)
net_tax_owed = gross_tax_liability - total_tax_offsets

# Logika Pengelompokan Umur Piutang (Invoice Aging)
def calculate_aging_bucket(row):
    if row['Status'] == 'Paid': 
        return 'Paid'
    days = (today - row['Due_Date']).days
    if days <= 0: 
        return 'Current (Not Due)'
    elif days <= 30: 
        return '1 - 30 Days'
    elif days <= 60: 
        return '31 - 60 Days'
    else: 
        return '61+ Days (Critical)'

inv_df['Aging_Bucket'] = inv_df.apply(calculate_aging_bucket, axis=1)

# --- PANEL INTERAKSI SIDEBAR (KONTROL INPUT) ---
st.sidebar.title("🎮 Action Control Panel")
app_mode = st.sidebar.radio("Pilih Modul Halaman:", ["📊 Dashboard & Tax Engine", "🧾 Input Pengeluaran & Nota", "➕ Input Invoice Baru"])

if app_mode == "➕ Input Invoice Baru":
    st.sidebar.subheader("Buat Invoice Penjualan Baru")
    with st.sidebar.form("inv_form", clear_on_submit=True):
        client = st.text_input("Nama Klien / Perusahaan")
        amount = st.number_input("Nominal Bersih (Rp)", min_value=0.0, step=1000000.0)
        tax_rate = st.slider("Tarif Pajak (%)", 0, 20, 11)
        due_d = st.date_input("Tanggal Jatuh Tempo", value=today)
        status = st.selectbox("Status Pembayaran", ["Unpaid", "Paid"])
        if st.form_submit_with_checkbox("Simpan Invoice") and client:
            new_inv = {'Invoice_ID': f"INV-00{len(inv_df)+1}", 'Client': client, 'Due_Date': pd.to_datetime(due_d), 'Amount': amount, 'Tax_Rate_%': tax_rate, 'Status': status}
            st.session_state.invoices = pd.concat([st.session_state.invoices, pd.DataFrame([new_inv])], ignore_index=True)
            st.success("Invoice Penjualan Berhasil Tersimpan!")
            st.rerun()

elif app_mode == "🧾 Input Pengeluaran & Nota":
    st.sidebar.subheader("Catat Pengeluaran & Nota Baru")
    with st.sidebar.form("exp_form", clear_on_submit=True):
        vendor = st.text_input("Nama Vendor / Supplier")
        category = st.selectbox("Kategori Pengeluaran", ["Software/Tech", "Rent/Office", "Marketing", "Travel & Meals", "Legal/Admin"])
        exp_amount = st.number_input("Nominal Dasar Pengeluaran (Rp)", min_value=0.0, step=500000.0)
        tax_paid = st.number_input("Pajak Masukan Masuk Masukan (Rp)", min_value=0.0, step=50000.0)
        uploaded_file = st.file_uploader("Unggah Bukti Nota/Kuitansi (PDF, PNG, JPG)", type=["pdf", "png", "jpg"])
        if st.form_submit_with_checkbox("Simpan Pengeluaran") and vendor:
            receipt_status = "Uploaded" if uploaded_file is not None else "Missing"
            new_exp = {'Expense_ID': f"EXP-00{len(exp_df)+1}", 'Vendor': vendor, 'Category': category, 'Date': today, 'Amount': exp_amount, 'Tax_Paid': tax_paid, 'Receipt': receipt_status}
            st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_exp])], ignore_index=True)
            st.success("Pengleluaran Berhasil Dipetakan Sebagai Pengurang Pajak!")
            st.rerun()

# --- TAMPILAN DASHBOARD UTAMA ---
if app_mode == "📊 Dashboard & Tax Engine":
    
    st.subheader("🏛️ Dashboard Akuntansi & Penyeimbang Pajak (Rupiah)")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    kpi1.metric("Kewajiban Pajak Kotor", f"Rp {gross_tax_liability:,.0f}".replace(",", "."))
    kpi2.metric("Total Kompensasi Pajak (Offset)", f"Rp {total_tax_offsets:,.0f}".replace(",", "."), delta=f"-Rp {total_tax_offsets:,.0f}".replace(",", "."), delta_color="inverse")
    
    if net_tax_owed >= 0:
        kpi3.metric("Net Utang Pajak Setor", f"Rp {net_tax_owed:,.0f}".replace(",", "."), delta="Wajib Disetor Ke Kas Negara")
    else:
        kpi3.metric("Surplus Pajak (Lebih Bayar)", f"Rp {abs(net_tax_owed):,.0f}".replace(",", "."), delta="Dapat Dikompensasikan Bulan Depan", delta_color="normal")
        
    kpi4.metric("Total Biaya Operasional", f"Rp {total_expenses_value:,.0f}".replace(",", "."))
    
    st.markdown("---")
    
    # Visualisasi Grafik
    col_graph1, col_graph2 = st.columns(2)
    with col_graph1:
        st.subheader("⏳ Analisis Umur Piutang (Invoice Belum Lunas)")
        unpaid_df = inv_df[inv_df['Status'] == 'Unpaid']
        aging_summary = unpaid_df.groupby('Aging_Bucket')['Amount'].sum().reset_index()
        all_buckets = pd.DataFrame({'Aging_Bucket': ['Current (Not Due)', '1 - 30 Days', '31 - 60 Days', '61+ Days (Critical)']})
        aging_summary = pd.merge(all_buckets, aging_summary, on='Aging_Bucket', how='left').fillna(0)
        fig_aging = px.bar(aging_summary, x='Aging_Bucket', y='Amount', color='Aging_Bucket',
                           labels={'Amount': 'Jumlah Piutang (Rp)', 'Aging_Bucket': 'Kategori Keterlambatan'},
                           color_discrete_map={'Current (Not Due)': '#2ecc71', '1 - 30 Days': '#f1c40f', '31 - 60 Days': '#e67e22', '61+ Days (Critical)': '#e74c3c'})
        st.plotly_chart(fig_aging, use_container_width=True)
        
    with col_graph2:
        st.subheader("🍕 Distribusi Anggaran Pengeluaran Operasional")
        if not exp_df.empty:
            fig_exp = px.pie(exp_df, values='Amount', names='Category', hole=0.4, color_discrete_sequence=px.colors.sequential.YlOrRd_r)
            st.plotly_chart(fig_exp, use_container_width=True)
        else:
            st.write("Belum ada pengeluaran operasional yang dicatat.")
            
    st.markdown("---")
    
    # Pembagian Tab Data & AI Analysis
    tab1, tab2, tab3 = st.tabs(["📂 Sales & Invoices Ledger", "🧾 Operational Expenses & Receipts", "🤖 AI Financial Analysis"])
    
    with tab1:
        st.dataframe(inv_df.style.format({'Amount': 'Rp {:,.0f}', 'Tax_Collected': 'Rp {:,.0f}', 'Tax_Rate_%': '{:.0f}%'}), use_container_width=True)
        
    with tab2:
        st.dataframe(exp_df.style.map(highlight_missing_receipt, subset=['Receipt']).format({'Amount': 'Rp {:,.0f}', 'Tax_Paid': 'Rp {:,.0f}'}), use_container_width=True)
        
    with tab3:
        st.subheader("🤖 Hasil Analisis Finansial Otomatis AI (Januari - Juni)")
        total_pendapatan_bersih = inv_df['Amount'].sum()
        total_pengeluaran_bersih = exp_df['Amount'].sum()
        sisa_kas = total_pendapatan_bersih - total_pengeluaran_bersih
        rasio_pengeluaran = (total_pengeluaran_bersih / total_pendapatan_bersih * 100) if total_pendapatan_bersih > 0 else 0
        
        st.markdown("### 📋 Ringkasan Arus Kas")
        col_ai1, col_ai2 = st.columns(2)
        with col_ai1:
            st.info(f"**Total Pendapatan Terlog:** Rp {total_pendapatan_bersih:,.0f}".replace(",", "."))
            st.warning(f"**Total Pengeluaran Terlog:** Rp {total_pengeluaran_bersih:,.0f}".replace(",", "."))
        with col_ai2:
            st.success(f"**Arus Kas Bersih (Net Cashflow):** Rp {sisa_kas:,.0f}".replace(",", "."))
            st.metric("Rasio Beban Operasional", f"{rasio_pengeluaran:.1f}%")
            
        st.markdown("### 💡 Rekomendasi & Temuan Strategis AI")
        insights = []
        if rasio_pengeluaran > 50:
            insights.append("⚠️ **Peringatan Efisiensi:** Rasio pengeluaran Anda melebihi 50% dari pendapatan berjalan. AI mendeteksi potensi inefisiensi pada biaya operasional. Disarankan untuk meninjau ulang vendor teknologi dan kantor.")
        else:
            insights.append("✅ **Kesehatan Keuangan Baik:** Rasio beban operasional terkendali dengan sangat baik di bawah ambang batas batas aman 50%. Pertahankan struktur biaya saat ini.")
            
        if total_pending_tax > 0:
            teks_piutang = f"⏳ **Optimasi Arus Kas:** Terdapat modal perusahaan terikat pada invoice *Unpaid* sebesar **Rp {total_pending_tax:,.0f}**. AI merekomendasikan untuk segera memprioritaskan penagihan pada daftar klien di kategori umur piutang *31-60 hari* dan *61+ hari* demi mengamankan ketersediaan kas operasional."
            insights.append(teks_piutang.replace(",", "."))
            
        if total_tax_offsets > 0:
            teks_offset = f"🛡️ **Klaim Pengurangan Pajak Berhasil:** Pengeluaran usaha Anda berhasil menghemat pajak legal sebesar **Rp {total_tax_offsets:,.0f}** via skema Tax Offset Pajak Masukan. Teruskan pencatatan nota demi efisiensi fiskal."
            insights.append(teks_offset.replace(",", "."))
            
        for insight in insights:
            st.write(insight)
            
        st.caption("*Analisis data ini dihasilkan secara instan berdasarkan data historis buku kas perusahaan dari Januari s.d Juni 2026.*")
