"""
KPI calculation functions for supplier performance
"""
import pandas as pd

def calculate_on_time_delivery(invoices_df):
    """Calculate on-time delivery percentage"""
    if len(invoices_df) == 0:
        return 0.0
    on_time_count = (invoices_df['delivery_delay_days'] <= 0).sum()
    total_count = len(invoices_df)
    return round((on_time_count / total_count) * 100, 2)

def calculate_invoice_accuracy(invoices_df):
    """Calculate invoice accuracy percentage"""
    if len(invoices_df) == 0:
        return 0.0
    accurate_count = invoices_df['is_accurate'].sum()
    total_count = len(invoices_df)
    return round((accurate_count / total_count) * 100, 2)

def calculate_rejection_rate(invoices_df):
    """Calculate invoice rejection rate"""
    if len(invoices_df) == 0:
        return 0.0
    rejected_count = invoices_df['is_rejected'].sum()
    total_count = len(invoices_df)
    return round((rejected_count / total_count) * 100, 2)

def calculate_avg_payment_days(invoices_df):
    """Calculate average payment days"""
    if len(invoices_df) == 0:
        return 0.0
    return round(invoices_df['payment_days'].mean(), 2)

def calculate_avg_outstanding(outstanding_df):
    """Calculate average outstanding amount"""
    if len(outstanding_df) == 0:
        return 0.0
    return round(outstanding_df['outstanding_amount'].mean(), 2)

def calculate_total_outstanding(outstanding_df):
    """Calculate total outstanding amount"""
    if len(outstanding_df) == 0:
        return 0.0
    return round(outstanding_df['outstanding_amount'].sum(), 2)

def calculate_supplier_kpis(invoices_df, outstanding_df, suppliers_df):
    """Calculate KPIs per supplier"""
    supplier_kpis = []
    
    for _, supplier in suppliers_df.iterrows():
        supplier_id = supplier['supplier_id']
        supplier_invoices = invoices_df[invoices_df['supplier_id'] == supplier_id]
        supplier_outstanding = outstanding_df[outstanding_df['supplier_id'] == supplier_id]
        
        kpis = {
            'supplier_id': supplier_id,
            'supplier_name': supplier['supplier_name'],
            'country': supplier['country'],
            'category': supplier['category'],
            'on_time_delivery': calculate_on_time_delivery(supplier_invoices),
            'invoice_accuracy': calculate_invoice_accuracy(supplier_invoices),
            'rejection_rate': calculate_rejection_rate(supplier_invoices),
            'avg_payment_days': calculate_avg_payment_days(supplier_invoices),
            'avg_outstanding': calculate_avg_outstanding(supplier_outstanding),
            'total_invoices': len(supplier_invoices),
            'total_amount': round(supplier_invoices['invoice_amount'].sum(), 2) if len(supplier_invoices) > 0 else 0
        }
        supplier_kpis.append(kpis)
    
    return pd.DataFrame(supplier_kpis)

def calculate_overall_kpis(invoices_df, outstanding_df):
    """Calculate overall KPIs across all suppliers"""
    return {
        'on_time_delivery': calculate_on_time_delivery(invoices_df),
        'invoice_accuracy': calculate_invoice_accuracy(invoices_df),
        'rejection_rate': calculate_rejection_rate(invoices_df),
        'avg_payment_days': calculate_avg_payment_days(invoices_df),
        'avg_outstanding': calculate_avg_outstanding(outstanding_df),
        'total_outstanding': calculate_total_outstanding(outstanding_df)
    }