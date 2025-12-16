"""
Generates synthetic supplier performance data
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import sqlite3

fake = Faker()
random.seed(42)
np.random.seed(42)

def generate_suppliers(n=20):
    """Generate supplier master data"""
    suppliers = []
    for i in range(n):
        suppliers.append({
            'supplier_id': f'SUP{i+1:03d}',
            'supplier_name': fake.company(),
            'country': random.choice(['USA', 'India', 'China', 'Germany', 'Japan']),
            'category': random.choice(['Raw Materials', 'Electronics', 'Packaging', 'Logistics'])
        })
    return pd.DataFrame(suppliers)

def generate_invoices(suppliers_df, n=500):
    """Generate invoice data with performance metrics"""
    invoices = []
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(n):
        supplier = suppliers_df.sample(1).iloc[0]
        invoice_date = start_date + timedelta(days=random.randint(0, 365))
        due_date = invoice_date + timedelta(days=30)
        payment_date = due_date + timedelta(days=random.randint(-5, 15))
        expected_delivery = invoice_date + timedelta(days=random.randint(5, 15))
        actual_delivery = expected_delivery + timedelta(days=random.randint(-3, 10))
        
        invoice_amount = round(random.uniform(1000, 50000), 2)
        is_accurate = random.random() > 0.15
        is_rejected = random.random() < 0.08
        
        invoices.append({
            'invoice_id': f'INV{i+1:05d}',
            'supplier_id': supplier['supplier_id'],
            'invoice_date': invoice_date.strftime('%Y-%m-%d'),
            'due_date': due_date.strftime('%Y-%m-%d'),
            'payment_date': payment_date.strftime('%Y-%m-%d'),
            'expected_delivery_date': expected_delivery.strftime('%Y-%m-%d'),
            'actual_delivery_date': actual_delivery.strftime('%Y-%m-%d'),
            'invoice_amount': invoice_amount,
            'is_accurate': int(is_accurate),
            'is_rejected': int(is_rejected),
            'payment_days': (payment_date - invoice_date).days,
            'delivery_delay_days': (actual_delivery - expected_delivery).days
        })
    
    return pd.DataFrame(invoices)

def generate_outstanding(suppliers_df, n=50):
    """Generate outstanding payment data"""
    outstanding = []
    for i in range(n):
        supplier = suppliers_df.sample(1).iloc[0]
        outstanding.append({
            'supplier_id': supplier['supplier_id'],
            'outstanding_amount': round(random.uniform(5000, 100000), 2),
            'aging_days': random.randint(0, 120)
        })
    return pd.DataFrame(outstanding)

def save_to_sqlite(suppliers_df, invoices_df, outstanding_df, db_path='data/suppliers.db'):
    """Save all data to SQLite database"""
    import os
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    
    suppliers_df.to_sql('suppliers', conn, if_exists='replace', index=False)
    invoices_df.to_sql('invoices', conn, if_exists='replace', index=False)
    outstanding_df.to_sql('outstanding', conn, if_exists='replace', index=False)
    
    conn.close()
    print(f"✓ Data saved to {db_path}")

if __name__ == "__main__":
    print("Generating synthetic data...")
    suppliers_df = generate_suppliers(20)
    invoices_df = generate_invoices(suppliers_df, 500)
    outstanding_df = generate_outstanding(suppliers_df, 50)
    
    save_to_sqlite(suppliers_df, invoices_df, outstanding_df)
    
    invoices_df.to_csv('data/sample_export.csv', index=False)
    print("✓ Sample CSV exported to data/sample_export.csv")
    
    print("\nData Summary:")
    print(f"Suppliers: {len(suppliers_df)}")
    print(f"Invoices: {len(invoices_df)}")
    print(f"Outstanding records: {len(outstanding_df)}")