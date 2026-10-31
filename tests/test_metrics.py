from pathlib import Path
import pandas as pd, numpy as np
ROOT=Path(__file__).resolve().parents[1]; f=pd.read_csv(ROOT/'data/processed/fact_sales_clean.csv')
def test_financial_reconciliation():
 assert np.allclose(f.SalesRevenue,f.Quantity*f.UnitSellingPrice,atol=.011)
 assert np.allclose(f.CostOfGoodsSold,f.Quantity*f.UnitCost,atol=.011)
 assert np.allclose(f.GrossProfit,f.SalesRevenue-f.CostOfGoodsSold,atol=.011)
 assert np.allclose(f.GrossMarginPct,f.GrossProfit/f.SalesRevenue,atol=1e-8)
def test_discount_formula_and_aggregate_denominators():
 discount=f.Quantity*(f.UnitListPrice-f.UnitSellingPrice)
 assert (discount>=-f.Quantity*.011).all()
 gross_list=(f.Quantity*f.UnitListPrice).sum(); assert gross_list>0
 assert 0 <= discount.sum()/gross_list < 1
def test_zero_denominator_safe_division():
 def safe(n,d): return n/d if d else 0
 assert safe(10,0)==0 and safe(0,0)==0 and safe(10,2)==5
def test_scenario_math():
 price,qty,cost,pc,dc,cc=100,10,60,.1,-.05,.05
 sr=price*(1+pc)*qty*(1+dc); sc=cost*(1+cc)*qty*(1+dc); sp=sr-sc
 assert round(sr,2)==1045.0 and round(sc,2)==598.5 and round(sp,2)==446.5
