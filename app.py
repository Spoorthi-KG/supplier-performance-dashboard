"""
Supplier Performance & SLA Dashboard
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from database import SupplierDatabase
from kpi_calculator import calculate_overall_kpis, calculate_supplier_kpis

st.set_page_config(page_title="Supplier Performance Dashboard", page_icon="📊", layout="wide")

db = SupplierDatabase()

st.title("📊 Supplier Performance & SLA Dashboard")
st.markdown("---")

# Sidebar filters
st.sidebar.header("🔍 Filters")

suppliers_df = db.get_suppliers()
supplier_options = ['All Suppliers'] + suppliers_df['supplier_name'].tolist()
selected_suppliers = st.sidebar.multiselect("Select Suppliers", options=supplier_options, default=['All Suppliers'])

min_date_str, max_date_str = db.get_date_range()
min_date = datetime.strptime(min_date_str, '%Y-%m-%d').date()
max_date = datetime.strptime(max_date_str, '%Y-%m-%d').date()

date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

categories = ['All Categories'] + suppliers_df['category'].unique().tolist()
selected_category = st.sidebar.selectbox("Category", categories)

# Apply filters
start_date = date_range[0].strftime('%Y-%m-%d') if len(date_range) > 0 else None
end_date = date_range[1].strftime('%Y-%m-%d') if len(date_range) > 1 else None

if 'All Suppliers' not in selected_suppliers and len(selected_suppliers) > 0:
    supplier_ids = suppliers_df[suppliers_df['supplier_name'].isin(selected_suppliers)]['supplier_id'].tolist()
else:
    supplier_ids = None

if selected_category != 'All Categories':
    filtered_suppliers = suppliers_df[suppliers_df['category'] == selected_category]
    if supplier_ids:
        supplier_ids = [sid for sid in supplier_ids if sid in filtered_suppliers['supplier_id'].tolist()]
    else:
        supplier_ids = filtered_suppliers['supplier_id'].tolist()

invoices_df = db.get_invoices(start_date, end_date, supplier_ids)
outstanding_df = db.get_outstanding(supplier_ids)

if supplier_ids:
    filtered_suppliers_df = suppliers_df[suppliers_df['supplier_id'].isin(supplier_ids)]
else:
    filtered_suppliers_df = suppliers_df

overall_kpis = calculate_overall_kpis(invoices_df, outstanding_df)

# Display KPIs
st.subheader("📈 Overall Performance Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("On-Time Delivery", f"{overall_kpis['on_time_delivery']}%")
with col2:
    st.metric("Invoice Accuracy", f"{overall_kpis['invoice_accuracy']}%")
with col3:
    st.metric("Rejection Rate", f"{overall_kpis['rejection_rate']}%")
with col4:
    st.metric("Avg Payment Days", f"{overall_kpis['avg_payment_days']} days")
with col5:
    st.metric("Avg Outstanding", f"${overall_kpis['avg_outstanding']:,.0f}")

st.markdown("---")

# Supplier KPIs
st.subheader("🏢 Supplier Performance Breakdown")
supplier_kpis = calculate_supplier_kpis(invoices_df, outstanding_df, filtered_suppliers_df)

st.dataframe(
    supplier_kpis.style.format({
        'on_time_delivery': '{:.2f}%',
        'invoice_accuracy': '{:.2f}%',
        'rejection_rate': '{:.2f}%',
        'avg_payment_days': '{:.2f}',
        'avg_outstanding': '${:,.2f}',
        'total_amount': '${:,.2f}'
    }),
    use_container_width=True,
    height=300
)

st.markdown("---")

# Visualizations
st.subheader("📊 Visual Analytics")
tab1, tab2, tab3, tab4 = st.tabs(["Performance Comparison", "Trends", "Distribution", "Drill-Down"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        fig_delivery = px.bar(
            supplier_kpis.sort_values('on_time_delivery', ascending=False).head(10),
            x='supplier_name', y='on_time_delivery',
            title='Top 10 Suppliers - On-Time Delivery',
            color='on_time_delivery', color_continuous_scale='RdYlGn'
        )
        fig_delivery.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_delivery, use_container_width=True)
    
    with col2:
        fig_accuracy = px.bar(
            supplier_kpis.sort_values('invoice_accuracy', ascending=False).head(10),
            x='supplier_name', y='invoice_accuracy',
            title='Top 10 Suppliers - Invoice Accuracy',
            color='invoice_accuracy', color_continuous_scale='Blues'
        )
        fig_accuracy.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_accuracy, use_container_width=True)

with tab2:
    if len(invoices_df) > 0:
        invoices_df['invoice_date'] = pd.to_datetime(invoices_df['invoice_date'])
        monthly_stats = invoices_df.groupby(invoices_df['invoice_date'].dt.to_period('M')).agg({
            'delivery_delay_days': lambda x: ((x <= 0).sum() / len(x) * 100),
            'is_accurate': lambda x: (x.sum() / len(x) * 100),
            'is_rejected': lambda x: (x.sum() / len(x) * 100)
        }).reset_index()
        monthly_stats['invoice_date'] = monthly_stats['invoice_date'].dt.to_timestamp()
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=monthly_stats['invoice_date'], y=monthly_stats['delivery_delay_days'], name='On-Time Delivery %', line=dict(color='green', width=2)))
        fig_trend.add_trace(go.Scatter(x=monthly_stats['invoice_date'], y=monthly_stats['is_accurate'], name='Invoice Accuracy %', line=dict(color='blue', width=2)))
        fig_trend.add_trace(go.Scatter(x=monthly_stats['invoice_date'], y=monthly_stats['is_rejected'], name='Rejection Rate %', line=dict(color='red', width=2)))
        fig_trend.update_layout(title='Performance Trends Over Time', xaxis_title='Month', yaxis_title='Percentage (%)', hovermode='x unified')
        st.plotly_chart(fig_trend, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        category_kpis = supplier_kpis.groupby('category').agg({
            'on_time_delivery': 'mean',
            'invoice_accuracy': 'mean',
            'rejection_rate': 'mean'
        }).reset_index()
        fig_category = px.bar(category_kpis, x='category', y=['on_time_delivery', 'invoice_accuracy', 'rejection_rate'],
            title='Performance by Category', barmode='group')
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        if len(invoices_df) > 0:
            fig_payment = px.histogram(invoices_df, x='payment_days', nbins=30, title='Payment Days Distribution')
            st.plotly_chart(fig_payment, use_container_width=True)

with tab4:
    st.subheader("🔍 Supplier Drill-Down")
    selected_supplier_name = st.selectbox("Select Supplier for Details", supplier_kpis['supplier_name'].tolist())
    
    if selected_supplier_name:
        supplier_detail = supplier_kpis[supplier_kpis['supplier_name'] == selected_supplier_name].iloc[0]
        supplier_id_detail = supplier_detail['supplier_id']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Invoices", supplier_detail['total_invoices'])
        with col2:
            st.metric("Total Amount", f"${supplier_detail['total_amount']:,.2f}")
        with col3:
            st.metric("Category", supplier_detail['category'])
        
        supplier_invoices = invoices_df[invoices_df['supplier_id'] == supplier_id_detail]
        if len(supplier_invoices) > 0:
            st.subheader("Recent Invoices")
            st.dataframe(supplier_invoices[['invoice_id', 'invoice_date', 'invoice_amount', 'payment_days', 'delivery_delay_days', 'is_accurate', 'is_rejected']].head(20), use_container_width=True)

# Export
st.markdown("---")
st.subheader("📥 Export Data")
col1, col2 = st.columns(2)

with col1:
    csv_suppliers = supplier_kpis.to_csv(index=False)
    st.download_button("Download Supplier KPIs (CSV)", csv_suppliers, file_name=f"supplier_kpis_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

with col2:
    csv_invoices = invoices_df.to_csv(index=False)
    st.download_button("Download Invoice Details (CSV)", csv_invoices, file_name=f"invoice_details_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

st.markdown("---")
st.caption("Dashboard built with Streamlit | Data refreshed in real-time")