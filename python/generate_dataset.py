"""Generate reproducible synthetic retail pricing data and source-quality exceptions."""
from pathlib import Path
import numpy as np, pandas as pd, json
ROOT=Path(__file__).resolve().parents[1]; RNG=np.random.default_rng(20261028)
N=20000
categories={
 'Electronics':['Audio','Computing','Accessories'], 'Home & Kitchen':['Cookware','Storage','Appliances'],
 'Beauty':['Skincare','Haircare','Cosmetics'], 'Sports':['Fitness','Outdoor','Apparel'],
 'Grocery':['Pantry','Beverages','Snacks'], 'Furniture':['Office','Living','Bedroom'],
 'Toys':['Learning','Games','Outdoor Play'], 'Fashion':['Basics','Footwear','Bags'],
 'Pet Supplies':['Food','Care','Accessories'], 'Books':['Fiction','Education','Hobbies']}
brands=['Northstar','UrbanNest','Everwell','Peakline','BrightLeaf','CoreCraft','Bluebird','Oak & Vale']
products=[]
for i in range(1,121):
 cat=list(categories)[(i-1)%len(categories)]; sub=categories[cat][((i-1)//10)%3]
 price=round(float(np.exp(RNG.uniform(np.log(8),np.log(420)))),2)
 cost=round(price*float(RNG.uniform(.38,.82)),2)
 # Deliberate interpretable pricing scenarios in product master
 if i%17==0: cost=round(price*.91,2) # low-margin product
 if i%19==0: cost=round(price*.54,2) # healthy margin
 products.append({'ProductID':f'P{i:03d}','ProductName':f'{cat.split()[0]} {sub} Item {i:03d}','Category':cat,'Subcategory':sub,'Brand':brands[(i-1)%len(brands)],'CurrentListPrice':price,'CurrentUnitCost':cost,'ProductStatus':'Active' if i%23 else 'Review'})
prod=pd.DataFrame(products)
regions=pd.DataFrame([('R01','North','Delhi','Urban'),('R02','South','Karnataka','Urban'),('R03','West','Maharashtra','Urban'),('R04','East','West Bengal','Mixed'),('R05','Central','Madhya Pradesh','Mixed')],columns=['RegionID','RegionName','StateOrTerritory','MarketType'])
channels=pd.DataFrame([('C01','E-commerce'),('C02','Marketplace'),('C03','Retail Store'),('C04','Wholesale')],columns=['ChannelID','ChannelName'])
segments=pd.DataFrame([('S01','Value Seekers'),('S02','Mainstream'),('S03','Premium'),('S04','Small Business')],columns=['CustomerSegmentID','SegmentName'])
# 24-month period, weighted category and seasonal demand
start=pd.Timestamp('2024-01-01'); dates=pd.date_range(start,'2025-12-31',freq='D')
chosen_prod=RNG.integers(0,len(prod),N); date_idx=RNG.integers(0,len(dates),N); order_dates=dates[date_idx]
rows=[]
for n,(pi,dt) in enumerate(zip(chosen_prod,order_dates),1):
 p=prod.iloc[pi]; cat=p.Category
 season=1.0 + (0.28 if dt.month in [11,12] else 0.12 if dt.month in [3,4] else 0) 
 if cat=='Grocery' and dt.month in [5,6]: season+=.18
 if cat=='Sports' and dt.month in [1,2]: season+=.15
 qty=max(1,int(RNG.negative_binomial(2,2/(2+2.2*season))))
 listp=float(p.CurrentListPrice)*(1+0.015*((dt.year-2024)*12+dt.month-1)/24)
 # controlled discount variation; a subset gets deep discounts
 disc=float(np.clip(RNG.beta(1.5,8)*.45,0,.48))
 if pi%13==0: disc=float(RNG.uniform(.25,.42))
 if pi%11==0: disc=float(RNG.uniform(0,.06))
 # high-volume product with falling realized price scenario
 if pi%29==0 and dt.year==2025: disc=min(.48,disc+.10)
 unit_sell=round(listp*(1-disc),2); unit_cost=round(float(p.CurrentUnitCost)*(1+RNG.normal(0,.015)),2)
 # ensure nonnegative economics inputs, but some deep-discount rows may be below cost naturally
 revenue=round(qty*unit_sell,2); gross=round(revenue-qty*unit_cost,2)
 rows.append({'SalesLineID':f'L{n:06d}','OrderID':f'O{(n-1)//1+1:07d}' if False else f'O{n:07d}','OrderDate':dt,'ProductID':p.ProductID,'CustomerSegmentID':segments.iloc[int(RNG.integers(0,len(segments)))].CustomerSegmentID,'RegionID':regions.iloc[int(RNG.integers(0,len(regions)))].RegionID,'ChannelID':channels.iloc[int(RNG.integers(0,len(channels)))].ChannelID,'Quantity':qty,'UnitListPrice':round(listp,2),'DiscountPct':round(disc,4),'UnitSellingPrice':unit_sell,'UnitCost':unit_cost,'SalesRevenue':revenue,'CostOfGoodsSold':round(qty*unit_cost,2),'GrossProfit':gross,'GrossMarginPct':gross/revenue if revenue else np.nan})
sales=pd.DataFrame(rows)
# Data is synthetic. Raw input contains deliberate invalid source records, which ETL quarantines.
raw=sales.copy()
bad=raw.iloc[:6].copy(); bad['SalesLineID']=['BAD0001','BAD0002','BAD0003','BAD0004','BAD0005','BAD0006']
bad.loc[bad.index[0],'Quantity']=0; bad.loc[bad.index[1],'DiscountPct']=1.25; bad.loc[bad.index[2],'UnitSellingPrice']=-3; bad.loc[bad.index[3],'ProductID']='P999'; bad.loc[bad.index[4],'SalesLineID']=raw.iloc[5].SalesLineID; bad.loc[bad.index[5],'UnitCost']=-1
raw=pd.concat([raw,bad],ignore_index=True); raw['OrderDate']=pd.to_datetime(raw['OrderDate']).dt.strftime('%Y-%m-%d')
for name,df in [('fact_sales_raw.csv',raw),('dim_product.csv',prod),('dim_region.csv',regions),('dim_channel.csv',channels),('dim_customer_segment.csv',segments)]: df.to_csv(ROOT/'data/raw'/name,index=False)
# Clean/validate: flag each invalid row, preserve every rejected row and reasons.
df=raw.copy(); df['OrderDate']=pd.to_datetime(df.OrderDate,errors='coerce'); reasons=[]
for _,r in df.iterrows():
 e=[]
 if pd.isna(r.OrderDate): e.append('invalid_order_date')
 if pd.isna(r.Quantity) or r.Quantity<=0: e.append('quantity_not_positive')
 if pd.isna(r.UnitListPrice) or r.UnitListPrice<=0: e.append('list_price_not_positive')
 if pd.isna(r.UnitSellingPrice) or r.UnitSellingPrice<0: e.append('selling_price_negative')
 if pd.isna(r.UnitCost) or r.UnitCost<0: e.append('unit_cost_negative')
 if pd.isna(r.DiscountPct) or not 0<=r.DiscountPct<1: e.append('discount_out_of_range')
 if r.ProductID not in set(prod.ProductID): e.append('unknown_product_fk')
 reasons.append('|'.join(e))
df['RejectReason']=reasons
# Duplicate IDs: keep first valid row only; duplicates are quarantined
seen=set(); duplicate=[]
for sid in df.SalesLineID:
 duplicate.append(sid in seen); seen.add(sid)
df['DuplicateID']=duplicate
df.loc[df.DuplicateID & df.RejectReason.eq(''),'RejectReason']='duplicate_sales_line_id'
valid=df[df.RejectReason.eq('')].drop(columns=['RejectReason','DuplicateID']).copy()
# recompute derived metrics from source primitives, rounding currency to cents
valid['UnitSellingPrice']=np.round(valid.UnitListPrice*(1-valid.DiscountPct),2)
valid['SalesRevenue']=np.round(valid.Quantity*valid.UnitSellingPrice,2)
valid['CostOfGoodsSold']=np.round(valid.Quantity*valid.UnitCost,2)
valid['GrossProfit']=np.round(valid.SalesRevenue-valid.CostOfGoodsSold,2)
valid['GrossMarginPct']=np.where(valid.SalesRevenue!=0,valid.GrossProfit/valid.SalesRevenue,np.nan)
valid['OrderDate']=pd.to_datetime(valid.OrderDate).dt.strftime('%Y-%m-%d')
valid.to_csv(ROOT/'data/processed/fact_sales_clean.csv',index=False)
df.loc[df.RejectReason.ne(''),['SalesLineID','OrderID','OrderDate','ProductID','Quantity','UnitListPrice','DiscountPct','UnitSellingPrice','UnitCost','RejectReason']].to_csv(ROOT/'data/processed/quarantined_rows.csv',index=False)
# Date dimension
cal=pd.DataFrame({'Date':pd.date_range(valid.OrderDate.min(),valid.OrderDate.max(),freq='D')}); cal['Year']=cal.Date.dt.year; cal['Quarter']='Q'+cal.Date.dt.quarter.astype(str); cal['MonthNumber']=cal.Date.dt.month; cal['MonthName']=cal.Date.dt.month_name(); cal['YearMonth']=cal.Date.dt.strftime('%Y-%m'); cal['Week']=cal.Date.dt.isocalendar().week.astype(int); cal['IsWeekend']=cal.Date.dt.dayofweek>=5; cal['Date']=cal.Date.dt.strftime('%Y-%m-%d'); cal.to_csv(ROOT/'data/processed/dim_date.csv',index=False)
for name,dfx in [('dim_product.csv',prod),('dim_region.csv',regions),('dim_channel.csv',channels),('dim_customer_segment.csv',segments)]: dfx.to_csv(ROOT/'data/processed'/name,index=False)
quality={'generated_at_utc':pd.Timestamp.utcnow().isoformat(),'seed':20261028,'raw_rows':int(len(raw)),'clean_rows':int(len(valid)),'quarantined_rows':int((df.RejectReason!='').sum()),'products':int(len(prod)),'categories':int(prod.Category.nunique()),'regions':int(len(regions)),'channels':int(len(channels)),'date_min':str(valid.OrderDate.min()),'date_max':str(valid.OrderDate.max()),'duplicate_ids_raw':int(df.DuplicateID.sum()),'rejection_reasons':df.loc[df.RejectReason.ne(''),'RejectReason'].value_counts().to_dict(),'synthetic':True}
(ROOT/'data/processed/data_quality_report.json').write_text(json.dumps(quality,indent=2))
(ROOT/'data/README.md').write_text('''# Data files\n\nAll records are synthetic, generated with fixed seed `20261028`; no real customers or business results are represented. `raw/` contains source CSVs including six deliberately imperfect transaction records. `processed/` contains validated fact and dimension CSVs plus quarantined rows and a JSON quality report. Rebuild with `python python/generate_dataset.py`.\n\nGrain: one row per order product line. `OrderID` is unique per line in this demonstration dataset, so distinct order count is equivalent to distinct `OrderID`; in real multi-line orders it would not be. Currency is illustrative and not tied to a specified currency.\n''')
print(json.dumps(quality,indent=2))
