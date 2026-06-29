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
        {"Invoice_ID": "INV-003", "Client": "Gamma Inc", "Due_Date": "2026-05-15
