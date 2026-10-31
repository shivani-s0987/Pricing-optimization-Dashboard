from pathlib import Path
import pandas as pd, json
ROOT=Path(__file__).resolve().parents[1]; d=ROOT/'data/processed'; f=pd.read_csv(d/'fact_sales_clean.csv'); p=pd.read_csv(d/'dim_product.csv'); r=pd.read_csv(d/'dim_region.csv'); c=pd.read_csv(d/'dim_channel.csv'); s=pd.read_csv(d/'dim_customer_segment.csv')
checks={
 'clean_rows_at_least_15000':len(f)>=15000,
 'unique_sales_line_ids':f.SalesLineID.is_unique,
 'positive_quantity':(f.Quantity>0).all(),
 'discount_in_range':f.DiscountPct.between(0,1,inclusive='left').all(),
 'nonnegative_cost':(f.UnitCost>=0).all(),
 'product_fk_valid':f.ProductID.isin(p.ProductID).all(),
 'region_fk_valid':f.RegionID.isin(r.RegionID).all(),
 'channel_fk_valid':f.ChannelID.isin(c.ChannelID).all(),
 'segment_fk_valid':f.CustomerSegmentID.isin(s.CustomerSegmentID).all(),
 'revenue_reconciles':((f.SalesRevenue-f.Quantity*f.UnitSellingPrice).abs()<.011).all(),
 'cost_reconciles':((f.CostOfGoodsSold-f.Quantity*f.UnitCost).abs()<.011).all(),
 'profit_reconciles':((f.GrossProfit-(f.SalesRevenue-f.CostOfGoodsSold)).abs()<.011).all(),
 'margin_reconciles':((f.GrossMarginPct-f.GrossProfit/f.SalesRevenue).abs()<1e-8).all(),
 'dimensions_meet_minimums':len(p)>=100 and p.Category.nunique()>=8 and len(r)>=3 and len(c)>=3,
 'quarantine_has_rows':len(pd.read_csv(d/'quarantined_rows.csv'))>0,
}
report={'checks':[{'test':k,'expected':'PASS','actual':'PASS' if bool(v) else 'FAIL','status':'PASS' if bool(v) else 'FAIL'} for k,v in checks.items()],'passed':int(sum(bool(v) for v in checks.values())),'failed':int(sum(not bool(v) for v in checks.values())),'rows':len(f)}
(d/'validation_report.json').write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2)); raise SystemExit(1 if report['failed'] else 0)
