"""
Database operations for supplier dashboard
"""
import sqlite3
import pandas as pd

class SupplierDatabase:
    def __init__(self, db_path='data/suppliers.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """Create database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_suppliers(self):
        """Get all suppliers"""
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM suppliers", conn)
        conn.close()
        return df
    
    def get_invoices(self, start_date=None, end_date=None, supplier_ids=None):
        """Get invoices with optional filters"""
        conn = self.get_connection()
        query = "SELECT * FROM invoices WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND invoice_date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND invoice_date <= ?"
            params.append(end_date)
        
        if supplier_ids and len(supplier_ids) > 0:
            placeholders = ','.join('?' * len(supplier_ids))
            query += f" AND supplier_id IN ({placeholders})"
            params.extend(supplier_ids)
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def get_outstanding(self, supplier_ids=None):
        """Get outstanding amounts"""
        conn = self.get_connection()
        query = "SELECT * FROM outstanding WHERE 1=1"
        params = []
        
        if supplier_ids and len(supplier_ids) > 0:
            placeholders = ','.join('?' * len(supplier_ids))
            query += f" AND supplier_id IN ({placeholders})"
            params.extend(supplier_ids)
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def get_date_range(self):
        """Get min and max invoice dates"""
        conn = self.get_connection()
        query = "SELECT MIN(invoice_date) as min_date, MAX(invoice_date) as max_date FROM invoices"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.iloc[0]['min_date'], df.iloc[0]['max_date']