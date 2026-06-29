import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="FinAnlytica Enterprise - Tax Offset Engine", layout="wide")
st.title("📈 FinAnlytica Enterprise: Expense Tracking & Tax Offset Engine")

# Context Date for Aging Buckets
today = pd.to_datetime('2026-06-29')

# --- 1. SIMULATED INVOICE DATABASE ---
if 'invoices' not in st.session_state:
    st.session_state.invoices = pd.DataFrame([
        {'Invoice_ID': 'INV-001', 'Client': 'Alpha Corp', 'Due_Date': '2026-05-31', 'Amount': 5000.00, 'Tax_Rate_%': 10, 'Status': 'Paid'},
        {'Invoice_ID': 'INV-002', 'Client': 'Beta LLC', 'Due_Date': '2026-07-01', 'Amount': 3500.00, 'Tax_Rate_%': 10, 'Status': 'Unpaid'},
        {'Invoice_ID': 'INV-003', 'Client': 'Gamma Inc', 'Due_Date': '2026-05-15', 'Amount': 1200.00, 'Tax_Rate_%': 5, 'Status': 'Unpaid'},
        {'Invoice_ID': 'INV-004', 'Client': 'Delta Co', 'Due_Date': '2026-03-10', 'Amount': 2500.00, 'Tax_Rate_%': 10, 'Status': 'Unpaid'},
    ])
    st.session_state.invoices['Due_Date'] = pd.to_datetime(st.session_state.invoices['Due_Date'])

# --- 2. SIMULATED EXPENSE DATABASE ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame([
        {'Expense_ID': 'EXP-001', 'Vendor': 'AWS Cloud', 'Category': 'Software/Tech', 'Date': '2026-06-01', 'Amount': 400.00, 'Tax_Paid': 40.00, 'Receipt': 'Uploaded'},
        {'Expense_ID': 'EXP-002', 'Vendor': 'WeWork', 'Category': 'Rent/Office', 'Date': '2026-06-05', 'Amount': 1500.00, 'Tax_Paid': 150.00, 'Receipt': 'Uploaded'},
        {'Expense_ID': 'EXP-003', 'Vendor': 'Google Ads', 'Category': 'Marketing', 'Date': '2026-06-15', 'Amount': 600.00, 'Tax_Paid': 0.00, 'Receipt': 'Missing'},
    ])
    st.session_state.expenses['Date'] = pd.to_datetime(st.session_state.expenses['Date'])

# Copy dataframes for current session processing
inv_df = st.session_state.invoices.copy()
exp_df = st.session_state.expenses.copy()

# --- CALCULATIONS & MATH ---
# Invoices Calculations
inv_df['Tax_Collected'] = inv_df['Amount'] * (inv_df['Tax_Rate_%'] / 100)
total_collected_tax = inv_df[inv_df['Status'] == 'Paid']['Tax_Collected'].sum()
total_pending_tax = inv_df[inv_df['Status'] == 'Unpaid']['Tax_Collected'].sum()
gross_tax_liability = total_collected_tax + total_pending_tax

# Expense Calculations
total_expenses_value = exp_df['Amount'].sum()
total_tax_offsets = exp_df['Tax_Paid'].sum()

# Net Tax Liability Engine
net_tax_owed = gross_tax_liability - total_tax_offsets

# Invoice Aging Logic
def calculate_aging_bucket(row):
    if row['Status'] == 'Paid': return 'Paid'
    days = (today - row['Due_Date']).days
    if days <= 0: return 'Current (Not Due)'
    elif days <= 30: return '1 - 30 Days'
    elif days <= 60: return '31 - 60 Days'
    else: return '61+ Days (Critical)'

inv_df['Aging_Bucket'] = inv_df.apply(calculate_aging_bucket, axis=1)

# --- SIDEBAR INTERACTION PANELS ---
st.sidebar.title("🎮 Action Control Panel")
app_mode = st.sidebar.radio("Go to module:", ["📊 Dashboard & Tax Engine", "🧾 Add New Expense/Receipt", "➕ Add New Invoice"])

if app_mode == "➕ Add New Invoice":
    st.sidebar.subheader("New Sales Invoice")
    with st.sidebar.form("inv_form", clear_on_submit=True):
        client = st.text_input("Client Name")
        amount = st.number_input("Net Amount (Rp)", min_value=0.0, step=100.0)
        tax_rate = st.slider("Tax Rate (%)", 0, 20, 10)
        due_d = st.date_input("Due Date", value=today)
        status = st.selectbox("Status", ["Unpaid", "Paid"])
        if st.form_submit_with_checkbox("Log Invoice") and client:
            new_inv = {'Invoice_ID': f"INV-00{len(inv_df)+1}", 'Client': client, 'Due_Date': pd.to_datetime(due_d), 'Amount': amount, 'Tax_Rate_%': tax_rate, 'Status': status}
            st.session_state.invoices = pd.concat([st.session_state.invoices, pd.DataFrame([new_inv])], ignore_index=True)
            st.success("Invoice added successfully!")
            st.rerun()

elif app_mode == "🧾 Add New Expense/Receipt":
    st.sidebar.subheader("New Expense & Receipt Log")
    with st.sidebar.form("exp_form", clear_on_submit=True):
        vendor = st.text_input("Vendor / Supplier")
        category = st.selectbox("Expense Category", ["Software/Tech", "Rent/Office", "Marketing", "Travel & Meals", "Legal/Admin"])
        exp_amount = st.number_input("Expense Base Amount ($)", min_value=0.0, step=10.0)
        tax_paid = st.number_input("Tax Paid on Purchase ($)", min_value=0.0, step=5.0)
        uploaded_file = st.file_uploader("Attach Receipt (PDF, PNG)", type=["pdf", "png", "jpg"])
        
        if st.form_submit_with_checkbox("Log Expense & Receipt") and vendor:
            receipt_status = "Uploaded" if uploaded_file is not None else "Missing"
            new_exp = {'Expense_ID': f"EXP-00{len(exp_df)+1}", 'Vendor': vendor, 'Category': category, 'Date': today, 'Amount': exp_amount, 'Tax_Paid': tax_paid, 'Receipt': receipt_status}
            st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_exp])], ignore_index=True)
            st.success("Expense registered and mapped for Tax Offset!")
            st.rerun()

# --- MAIN DASHBOARD INTERFACE ---
if app_mode == "📊 Dashboard & Tax Engine":
    
    # ROW 1: Real-time Financial Health & Tax Engine Cards
    st.subheader("🏛️ Core Accounting & Tax Balancing Engine")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    kpi1.metric("Gross Tax Owed (Sales)", f"${gross_tax_liability:,.2f}", help="Total tax applied to your client invoices.")
    kpi2.metric("Total Tax Offsets (Expenses)", f"${total_tax_offsets:,.2f}", delta=f"-${total_tax_offsets:,.2f}", delta_color="inverse", help="Tax you have already paid on business operations. This directly subtracts from what you owe.")
    
    # Dynamic styling depending on whether you owe money or get a refund
    if net_tax_owed >= 0:
        kpi3.metric("Net Tax Liability Owed", f"${net_tax_owed:,.2f}", delta="Payable to Authority")
    else:
        kpi3.metric("Net Tax Refund Due", f"${abs(net_tax_owed):,.2f}", delta="Tax Credit Carry-forward", delta_color="normal")
        
    kpi4.metric("Total Operating Expenses", f"${total_expenses_value:,.2f}")
    
    st.markdown("---")
    
    # ROW 2: Analytics & Graphs
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.subheader("⏳ Accounts Receivable Aging (Unpaid Invoices)")
        unpaid_df = inv_df[inv_df['Status'] == 'Unpaid']
        aging_summary = unpaid_df.groupby('Aging_Bucket')['Amount'].sum().reset_index()
        all_buckets = pd.DataFrame({'Aging_Bucket': ['Current (Not Due)', '1 - 30 Days', '31 - 60 Days', '61+ Days (Critical)']})
        aging_summary = pd.merge(all_buckets, aging_summary, on='Aging_Bucket', how='left').fillna(0)
        
        fig_aging = px.bar(aging_summary, x='Aging_Bucket', y='Amount', color='Aging_Bucket',
                           color_discrete_map={'Current (Not Due)': '#2ecc71', '1 - 30 Days': '#f1c40f', '31 - 60 Days': '#e67e22', '61+ Days (Critical)': '#e74c3c'})
        st.plotly_chart(fig_aging, use_container_width=True)
        
    with col_graph2:
        st.subheader("🍕 Corporate Operating Expenses Breakdown")
        if not exp_df.empty:
            fig_exp = px.pie(exp_df, values='Amount', names='Category', hole=0.4,
                             color_discrete_sequence=px.colors.sequential.YlOrRd_r)
            st.plotly_chart(fig_exp, use_container_width=True)
        else:
            st.write("No operational expenses tracked yet.")
            
    st.markdown("---")
    
    # ROW 3: Separate Financial Ledgers
    tab1, tab2 = st.tabs(["📂 Sales & Invoices Ledger", "🧾 Operational Expenses & Receipts"])
    
    with tab1:
        st.dataframe(inv_df.style.format({'Amount': '${:,.2f}', 'Tax_Collected': '${:,.2f}', 'Tax_Rate_%': '{:.0f}%'}), use_container_width=True)
        
    with tab2:
        # Highlight lines missing receipts in soft red for tax audit safety
        def highlight_missing_receipt(val):
            color = '#ffcccc' if val == 'Missing' else 'clear'
            return f'background-color: {color}'
            
        st.dataframe(exp_df.style.applymap(highlight_missing_receipt, subset=['Receipt']).format({'Amount': '${:,.2f}', 'Tax_Paid': '${:,.2f}'}), use_container_width=True)
