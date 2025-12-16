"""
Unit tests for KPI calculations
Run with: pytest tests/test_kpis.py -v
"""
import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kpi_calculator import (
    calculate_on_time_delivery,
    calculate_invoice_accuracy,
    calculate_rejection_rate,
    calculate_avg_payment_days,
    calculate_avg_outstanding,
    calculate_total_outstanding
)

@pytest.fixture
def sample_invoices():
    return pd.DataFrame({
        'invoice_id': ['INV001', 'INV002', 'INV003', 'INV004', 'INV005'],
        'supplier_id': ['SUP001', 'SUP001', 'SUP002', 'SUP002', 'SUP003'],
        'delivery_delay_days': [-2, 0, 3, -1, 5],
        'is_accurate': [1, 1, 0, 1, 1],
        'is_rejected': [0, 0, 1, 0, 0],
        'payment_days': [28, 32, 35, 30, 40],
        'invoice_amount': [1000, 2000, 1500, 2500, 3000]
    })

@pytest.fixture
def sample_outstanding():
    return pd.DataFrame({
        'supplier_id': ['SUP001', 'SUP002', 'SUP003'],
        'outstanding_amount': [5000, 10000, 7500],
        'aging_days': [30, 60, 45]
    })

def test_on_time_delivery_calculation(sample_invoices):
    result = calculate_on_time_delivery(sample_invoices)
    expected = 60.0
    assert result == expected

def test_on_time_delivery_empty():
    empty_df = pd.DataFrame(columns=['delivery_delay_days'])
    result = calculate_on_time_delivery(empty_df)
    assert result == 0.0

def test_invoice_accuracy_calculation(sample_invoices):
    result = calculate_invoice_accuracy(sample_invoices)
    expected = 80.0
    assert result == expected

def test_invoice_accuracy_empty():
    empty_df = pd.DataFrame(columns=['is_accurate'])
    result = calculate_invoice_accuracy(empty_df)
    assert result == 0.0

def test_rejection_rate_calculation(sample_invoices):
    result = calculate_rejection_rate(sample_invoices)
    expected = 20.0
    assert result == expected

def test_rejection_rate_empty():
    empty_df = pd.DataFrame(columns=['is_rejected'])
    result = calculate_rejection_rate(empty_df)
    assert result == 0.0

def test_avg_payment_days_calculation(sample_invoices):
    result = calculate_avg_payment_days(sample_invoices)
    expected = 33.0
    assert result == expected

def test_avg_payment_days_empty():
    empty_df = pd.DataFrame(columns=['payment_days'])
    result = calculate_avg_payment_days(empty_df)
    assert result == 0.0

def test_avg_outstanding_calculation(sample_outstanding):
    result = calculate_avg_outstanding(sample_outstanding)
    expected = 7500.0
    assert result == expected

def test_avg_outstanding_empty():
    empty_df = pd.DataFrame(columns=['outstanding_amount'])
    result = calculate_avg_outstanding(empty_df)
    assert result == 0.0

def test_total_outstanding_calculation(sample_outstanding):
    result = calculate_total_outstanding(sample_outstanding)
    expected = 22500.0
    assert result == expected

def test_total_outstanding_empty():
    empty_df = pd.DataFrame(columns=['outstanding_amount'])
    result = calculate_total_outstanding(empty_df)
    assert result == 0.0