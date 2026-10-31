from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def test_report_outputs_exist():
 for name in ['executive_summary.md','pricing_recommendations.md','sample_report.pdf','category_performance.csv','monthly_performance.csv','discount_band_performance.csv','pricing_exceptions.csv']:
  assert (ROOT/'reports'/name).exists() and (ROOT/'reports'/name).stat().st_size>0
def test_excel_exists():
 p=ROOT/'excel/pricing_analysis_workbook.xlsx'; assert p.exists() and p.stat().st_size>10000

def test_report_reconciles_to_fact():
 f=pd.read_csv(ROOT/'data/processed/fact_sales_clean.csv'); cat=pd.read_csv(ROOT/'reports/category_performance.csv')
 assert abs(f.SalesRevenue.sum()-cat.Revenue.sum())<.02
 assert abs(f.GrossProfit.sum()-cat.GrossProfit.sum())<.02

def test_workbook_has_live_formulas_and_tables():
 from openpyxl import load_workbook
 p=ROOT/'excel/pricing_analysis_workbook.xlsx'
 wb=load_workbook(p,data_only=False,read_only=False)
 assert 'Cleaned Data' in wb.sheetnames and 'Executive Summary' in wb.sheetnames
 assert wb['Cleaned Data']['M2'].value.startswith('=')
 assert wb['Executive Summary']['B6'].value.startswith('=')
 assert len(wb['Cleaned Data'].tables)>=1
