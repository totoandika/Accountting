import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman Utama
st.set_page_config(page_title="FinAnlytica Enterprise", layout="wide")

# Konteks Tanggal untuk Umur Piutang (Pertengahan 2026)
today = pd.to_datetime('2026-06-29')

# --- 1. FITUR PILIHAN BAHASA (LANGUAGE SELECTOR) ---
st.sidebar.title("🌐 Language / Bahasa")
lang = st.sidebar.selectbox("Choose Language / Pilih Bahasa:", ["Indonesia", "English"])

# Kamus Teks Dua Bahasa
txt = {
    "Indonesia": {
        "title": "📈 FinAnlytica Enterprise: Pencatatan Transaksi & Analisis AI",
        "subtitle": "🏛️ Dashboard Akuntansi & Penyeimbang Pajak (Rupiah)",
        "kpi_gross": "Kewajiban Pajak Kotor",
        "kpi_offset": "Total Kompensasi Pajak (Offset)",
        "kpi_net_owed": "Net Utang Pajak Setor",
        "kpi_net_refund": "Surplus Pajak (Lebih Bayar)",
        "kpi_status_pay": "Wajib Disetor Ke Kas Negara",
        "kpi_status_ref": "Dapat Dikompensasikan Bulan Depan",
        "kpi_expense": "Total Biaya Operasional",
        "chart_aging_title": "⏳ Analisis Umur Piutang (Invoice Belum Lunas)",
        "chart_expense_title": "🍕 Distribusi Anggaran Pengeluaran Operasional",
        "tab_sales": "📂 Sales & Invoices Ledger",
        "tab_expenses": "🧾 Operational Expenses & Receipts",
        "tab_ai": "🤖 AI Financial Analysis",
        "ai_title": "🤖 Hasil Analisis Finansial Otomatis AI (Januari - Juni)",
        "ai_summary": "📋 Ringkasan Arus Kas",
        "ai_revenue": "Total Pendapatan Terlog",
        "ai_expense": "Total Pengeluaran Terlog",
        "ai_net": "Arus Kas Bersih (Net Cashflow)",
        "ai_ratio": "Rasio Beban Operasional",
        "ai_rec": "💡 Rekomendasi & Temuan Strategis AI",
        "ai_caption": "*Analisis data ini dihasilkan secara instan berdasarkan data historis buku kas perusahaan dari Januari s.d Juni 2026.*",
        "side_menu": "Pilih Modul Halaman:",
        "menu_dash": "📊 Dashboard & Tax Engine",
        "menu_exp": "🧾 Input Pengeluaran & Nota",
        "menu_inv": "➕ Input Invoice Baru",
        "form_inv_title": "Buat Invoice Penjualan Baru",
        "form_client": "Nama Klien / Perusahaan",
        "form_amount": "Nominal Bersih (Rp)",
        "form_tax": "Tarif Pajak (%)",
        "form_due": "Tanggal Jatuh Tempo",
        "form_status": "Status Pembayaran",
        "form_btn_inv": "Simpan Invoice",
        "form_exp_title": "Catat Pengeluaran & Nota Baru",
        "form_vendor": "Nama Vendor / Supplier",
        "form_cat": "Kategori Pengeluaran",
        "form_exp_amount": "Nominal Dasar Pengeluaran (Rp)",
        "form_tax_paid": "Pajak Masukan (Rp)",
        "form_file": "Unggah Bukti Nota/Kuitansi (PDF, PNG, JPG)",
        "form_btn_exp": "Simpan Pengeluaran",
        "msg_inv_success": "Invoice Penjualan Berhasil Tersimpan!",
        "msg_exp_success": "Pengeluaran Berhasil Dipetakan Sebagai Pengurang Pajak!"
    },
    "English": {
        "title": "📈 FinAnlytica Enterprise: Transaction Logging & AI Analysis",
        "subtitle": "🏛️ Accounting Dashboard & Tax Balancing Engine (Rupiah)",
        "kpi_gross": "Gross Tax Liability",
        "kpi_offset": "Total Tax Offsets",
        "kpi_net_owed": "Net Tax Payable",
        "kpi_net_refund": "Net Tax Refund / Credit",
        "kpi_status_pay": "Payable to Tax Authority",
        "kpi_status_ref": "Tax Credit Carry-forward",
        "kpi_expense": "Total Operating Expenses",
        "chart_aging_title": "⏳ Accounts Receivable Aging (Unpaid Invoices)",
        "chart_expense_title": "🍕 Operating Expenses Breakdown",
        "tab_sales": "📂 Sales & Invoices Ledger",
        "tab_expenses": "🧾 Operational Expenses & Receipts",
        "tab_ai": "🤖 AI Financial Analysis",
        "ai_title": "🤖 Automated AI Financial Analysis (January - June)",
        "ai_summary": "📋 Cash Flow Executive Summary",
        "ai_revenue": "Total Logged Revenue",
        "ai_expense": "Total Logged Expenses",
        "ai_net": "Net Cashflow",
        "ai_ratio": "Operating Expense Ratio",
        "ai_rec": "💡 AI Strategic Insights & Recommendations",
        "ai_caption": "*This data analysis was instantly generated based on historical cash ledger data from January to June 2026.*",
        "side_menu": "Go to Module:",
        "menu_dash": "📊 Dashboard & Tax Engine",
        "menu_exp": "🧾 Log Expense & Receipt",
        "menu_inv": "➕ Log New Invoice",
        "form_inv_title": "Create New Sales Invoice",
        "form_client": "Client Name",
        "form_amount": "Net Amount (Rp)",
        "form_tax": "Tax Rate (%)",
        "form_due": "Due Date",
        "form_status": "Payment Status",
        "form_btn_inv": "Log Invoice",
        "form_exp_title": "Log New Operating Expense",
        "form_vendor": "Vendor / Supplier",
        "form_cat": "Expense Category",
        "form_exp_amount": "Expense Base Amount (Rp)",
        "form_tax_paid": "Input VAT / Tax Paid (Rp)",
        "form_file": "Attach Receipt Proof (PDF, PNG, JPG)",
        "form_btn_exp": "Log Expense",
        "msg_inv_success": "Sales Invoice Successfully Logged!",
        "msg_exp_success": "Expense Successfully Mapped for Tax Offset!"
    }
}

st.title(txt[lang]["title"])

# --- 2. DATABASE DUMMY INVOICE ---
if 'invoices' not in st.session_state:
    st.session_state.invoices = pd.DataFrame([
        {"Invoice_ID": "INV-001", "Client": "Alpha Corp", "Due_Date": "2026-05-31", "Amount": 50000000.0, "Tax_Rate_%": 10, "Status": "Paid"},
        {"Invoice_ID": "INV-002", "Client": "Beta LLC", "Due_Date": "2026-07-01", "Amount": 35000000.0, "Tax_Rate_%": 10, "Status": "Unpaid"},
        {"Invoice_ID": "INV-003", "Client": "Gamma Inc", "Due_Date": "2026-05-15", "Amount": 12000000.0, "Tax_Rate_%": 5, "Status": "Unpaid"},
        {"Invoice_ID": "INV-004", "Client": "Delta Co", "Due_Date": "2026-03-10", "Amount": 25000000.0, "Tax_Rate_%": 10, "Status": "Unpaid"},
    ])
    st.session_state.invoices['Due_Date'] = pd.to_datetime(st.session_state.invoices['Due_Date'])

# --- 3. DATABASE DUMMY EXPENSE ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame([
        {"Expense_ID": "EXP-001", "Vendor": "AWS Cloud", "Category": "Software/Tech", "Date": "2026-06-01", "Amount": 4000000.0, "Tax_Paid": 400000.0, "Receipt": "Uploaded"},
        {"Expense_ID": "EXP-002", "Vendor": "WeWork", "Category": "Rent/Office", "Date": "2026-06-05", "Amount": 15000000.0, "Tax_Paid": 1500000.0, "Receipt": "Uploaded"},
        {"Expense_ID": "EXP-003", "Vendor": "Google Ads", "Category": "Marketing", "Date": "2026-06-15", "Amount": 6000000.0, "Tax_Paid": 0.0, "Receipt": "Missing"},
    ])
    st.session_state.expenses['Date'] = pd.to_datetime(st.session_state.expenses['Date'])

def highlight_missing_receipt(val):
    color = '#ffcccc' if val == 'Missing' else ''
    return f'background-color: {color}'

inv_df = st.session_state.invoices.copy()
exp_df = st.session_state.expenses.copy()

# --- KALKULASI FINANSIAL ---
inv_df['Tax_Collected'] = inv_df['Amount'] * (inv_df['Tax_Rate_%'] / 100)
total_collected_tax = inv_df[inv_df['Status'] == 'Paid']['Tax_Collected'].sum()
total_pending_tax = inv_df[inv_df['Status'] == 'Unpaid']['Tax_Collected'].sum()
gross_tax_liability = total_collected_tax + total_pending_tax

total_expenses_value = exp_df['Amount'].sum()
total_tax_offsets = exp_df['Tax_Paid'].sum()
net_tax_owed = gross_tax_liability - total_tax_offsets

def calculate_aging_bucket(row):
    if row['Status'] == 'Paid': return 'Paid'
    days = (today - row['Due_Date']).days
    if days <= 0: return 'Current (Not Due)'
    elif days <= 30: return '1 - 30 Days'
    elif days <= 60: return '31 - 60 Days'
    else: return '61+ Days (Critical)'

inv_df['Aging_Bucket'] = inv_df.apply(calculate_aging_bucket, axis=1)

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.title("🎮 Action Control Panel")
app_mode = st.sidebar.radio(txt[lang]["side_menu"], [txt[lang]["menu_dash"], txt[lang]["menu_exp"], txt[lang]["menu_inv"]])

if app_mode == txt[lang]["menu_inv"]:
    st.sidebar.subheader(txt[lang]["form_inv_title"])
    with st.sidebar.form("inv_form", clear_on_submit=True):
        client = st.text_input(txt[lang]["form_client"])
        amount = st.number_input(txt[lang]["form_amount"], min_value=0.0, step=1000000.0)
        tax_rate = st.slider(txt[lang]["form_tax"], 0, 20, 11)
        due_d = st.date_input(txt[lang]["form_due"], value=today)
        status = st.selectbox(txt[lang]["form_status"], ["Unpaid", "Paid"])
        submit_inv = st.form_submit_button(txt[lang]["form_btn_inv"])
        if submit_inv and client:
            new_inv = {'Invoice_ID': f"INV-00{len(inv_df)+1}", 'Client': client, 'Due_Date': pd.to_datetime(due_d), 'Amount': amount, 'Tax_Rate_%': tax_rate, 'Status': status}
            st.session_state.invoices = pd.concat([st.session_state.invoices, pd.DataFrame([new_inv])], ignore_index=True)
            st.sidebar.success(txt[lang]["msg_inv_success"])
            st.rerun()

elif app_mode == txt[lang]["menu_exp"]:
    st.sidebar.subheader(txt[lang]["form_exp_title"])
    with st.sidebar.form("exp_form", clear_on_submit=True):
        vendor = st.text_input(txt[lang]["form_vendor"])
        category = st.selectbox(txt[lang]["form_cat"], ["Software/Tech", "Rent/Office", "Marketing", "Travel & Meals", "Legal/Admin"])
        exp_amount = st.number_input(txt[lang]["form_exp_amount"], min_value=0.0, step=500000.0)
        tax_paid = st.number_input(txt[lang]["form_tax_paid"], min_value=0.0, step=50000.0)
        uploaded_file = st.file_uploader(txt[lang]["form_file"], type=["pdf", "png", "jpg"])
        submit_exp = st.form_submit_button(txt[lang]["form_btn_exp"])
        if submit_exp and vendor:
            receipt_status = "Uploaded" if uploaded_file is not None else "Missing"
            new_exp = {'Expense_ID': f"EXP-00{len(exp_df)+1}", 'Vendor': vendor, 'Category': category, 'Date': today, 'Amount': exp_amount, 'Tax_Paid': tax_paid, 'Receipt': receipt_status}
            st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_exp])], ignore_index=True)
            st.sidebar.success(txt[lang]["msg_exp_success"])
            st.rerun()

# --- MAIN DASHBOARD INTERFACE ---
if app_mode == txt[lang]["menu_dash"]:
    st.subheader(txt[lang]["subtitle"])
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    kpi1.metric(txt[lang]["kpi_gross"], f"Rp {gross_tax_liability:,.0f}".replace(",", "."))
    kpi2.metric(txt[lang]["kpi_offset"], f"Rp {total_tax_offsets:,.0f}".replace(",", "."), delta=f"-Rp {total_tax_offsets:,.0f}".replace(",", "."), delta_color="inverse")
    
    if net_tax_owed >= 0:
        kpi3.metric(txt[lang]["kpi_net_owed"], f"Rp {net_tax_owed:,.0f}".replace(",", "."), delta=txt[lang]["kpi_status_pay"])
    else:
        kpi3.metric(txt[lang]["kpi_net_refund"], f"Rp {abs(net_tax_owed):,.0f}".replace(",", "."), delta=txt[lang]["kpi_status_ref"], delta_color="normal")
        
    kpi4.metric(txt[lang]["kpi_expense"], f"Rp {total_expenses_value:,.0f}".replace(",", "."))
    st.markdown("---")
    
    col_graph1, col_graph2 = st.columns(2)
    with col_graph1:
        st.subheader(txt[lang]["chart_aging_title"])
        unpaid_df = inv_df[inv_df['Status'] == 'Unpaid']
        aging_summary = unpaid_df.groupby('Aging_Bucket')['Amount'].sum().reset_index()
        all_buckets = pd.DataFrame({'Aging_Bucket': ['Current (Not Due)', '1 - 30 Days', '31 - 60 Days', '61+ Days (Critical)']})
        aging_summary = pd.merge(all_buckets, aging_summary, on='Aging_Bucket', how='left').fillna(0)
        fig_aging = px.bar(aging_summary, x='Aging_Bucket', y='Amount', color='Aging_Bucket',
                           labels={'Amount': 'Amount (Rp)', 'Aging_Bucket': 'Category'},
                           color_discrete_map={'Current (Not Due)': '#2ecc71', '1 - 30 Days': '#f1c40f', '31 - 60 Days': '#e67e22', '61+ Days (Critical)': '#e74c3c'})
        st.plotly_chart(fig_aging, use_container_width=True)
        
    with col_graph2:
        st.subheader(txt[lang]["chart_expense_title"])
        if not exp_df.empty:
            fig_exp = px.pie(exp_df, values='Amount', names='Category', hole=0.4, color_discrete_sequence=px.colors.sequential.YlOrRd_r)
            st.plotly_chart(fig_exp, use_container_width=True)
            
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs([txt[lang]["tab_sales"], txt[lang]["tab_expenses"], txt[lang]["tab_ai"]])
    with tab1:
        st.dataframe(inv_df.style.format({'Amount': 'Rp {:,.0f}', 'Tax_Collected': 'Rp {:,.0f}', 'Tax_Rate_%': '{:.0f}%'}), use_container_width=True)
    with tab2:
        st.dataframe(exp_df.style.map(highlight_missing_receipt, subset=['Receipt']).format({'Amount': 'Rp {:,.0f}', 'Tax_Paid': 'Rp {:,.0f}'}), use_container_width=True)
    with tab3:
        st.subheader(txt[lang]["ai_title"])
        total_pendapatan_bersih = inv_df['Amount'].sum()
        total_pengeluaran_bersih = exp_df['Amount'].sum()
        sisa_kas = total_pendapatan_bersih - total_pengeluaran_bersih
        rasio_pengeluaran = (total_pengeluaran_bersih / total_pendapatan_bersih * 100) if total_pendapatan_bersih > 0 else 0
        
        st.markdown(f"### {txt[lang]['ai_summary']}")
        col_ai1, col_ai2 = st.columns(2)
        with col_ai1:
            st.info(f"**{txt[lang]['ai_revenue']}:** Rp {total_pendapatan_bersih:,.0f}".replace(",", "."))
            st.warning(f"**{txt[lang]['ai_expense']}:** Rp {total_pengeluaran_bersih:,.0f}".replace(",", "."))
        with col_ai2:
            st.success(f"**{txt[lang]['ai_net']}:** Rp {sisa_kas:,.0f}".replace(",", "."))
            st.metric(txt[lang]["ai_ratio"], f"{rasio_pengeluaran:.1f}%")
            
        st.markdown(f"### {txt[lang]['ai_rec']}")
        if lang == "Indonesia":
            if rasio_pengeluaran > 50:
                st.write("⚠️ **Peringatan Efisiensi:** Rasio pengeluaran Anda melebihi 50% dari pendapatan. AI mendeteksi inefisiensi pada biaya operasional.")
            else:
                st.write("✅ **Kesehatan Keuangan Baik:** Rasio beban operasional terkendali dengan sangat baik di bawah batas aman 50%.")
            if total_pending_tax > 0:
                st.write(f"⏳ **Optimasi Arus Kas:** Terdapat modal terikat pada invoice *Unpaid* sebesar **Rp {total_pending_tax:,.0f}**. AI merekomendasikan penagihan aktif.")
        else:
            if rasio_pengeluaran > 50:
                st.write("⚠️ **Efficiency Alert:** Your expense ratio exceeds 50% of current revenue. AI detects potential operational budget leaks.")
            else:
                st.write("✅ **Good Financial Health:** Your operational expense ratio is safely maintained below the 50% threshold.")
            if total_pending_tax > 0:
                st.write(f"⏳ **Cash Flow Optimization:** There is uncollected cash tied up in unpaid invoices worth **Rp {total_pending_tax:,.0f}**. AI recommends proactive collections.")
                
        st.caption(txt[lang]["ai_caption"])
