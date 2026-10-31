from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'data/processed'
def test_schema_and_dimensions():
 f=pd.read_csv(D/'fact_sales_clean.csv'); p=pd.read_csv(D/'dim_product.csv'); r=pd.read_csv(D/'dim_region.csv'); c=pd.read_csv(D/'dim_channel.csv'); s=pd.read_csv(D/'dim_customer_segment.csv')
 required={'SalesLineID','OrderID','OrderDate','ProductID','CustomerSegmentID','RegionID','ChannelID','Quantity','UnitListPrice','DiscountPct','UnitSellingPrice','UnitCost','SalesRevenue','CostOfGoodsSold','GrossProfit','GrossMarginPct'}
 assert required.issubset(f.columns); assert len(f)>=15000; assert f.SalesLineID.is_unique
 assert len(p)>=100 and p.Category.nunique()>=8 and len(r)>=3 and len(c)>=3
 assert f.ProductID.isin(p.ProductID).all() and f.RegionID.isin(r.RegionID).all() and f.ChannelID.isin(c.ChannelID).all() and f.CustomerSegmentID.isin(s.CustomerSegmentID).all()
def test_ranges_and_quarantine():
 f=pd.read_csv(D/'fact_sales_clean.csv'); q=pd.read_csv(D/'quarantined_rows.csv')
 assert (f.Quantity>0).all(); assert f.DiscountPct.between(0,1,inclusive='left').all(); assert (f.UnitCost>=0).all(); assert len(q)>=1; assert q.RejectReason.notna().all()
