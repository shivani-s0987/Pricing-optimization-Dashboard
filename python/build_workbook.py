"""Build a formula-driven Excel analysis workbook with summary tables and charts."""
from pathlib import Path
import pandas as pd, numpy as np
import xlsxwriter
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'data/processed'; OUT=ROOT/'excel/pricing_analysis_workbook.xlsx'; OUT.parent.mkdir(exist_ok=True)
f=pd.read_csv(D/'fact_sales_clean.csv'); p=pd.read_csv(D/'dim_product.csv'); raw=pd.read_csv(ROOT/'data/raw/fact_sales_raw.csv'); q=pd.read_csv(D/'processed'/'quarantined_rows.csv') if (D/'processed'/'quarantined_rows.csv').exists() else pd.read_csv(D/'quarantined_rows.csv')
f=f.merge(p[['ProductID','ProductName','Category','Subcategory','Brand']],on='ProductID',how='left')
f['GrossRevenueBeforeDiscount']=f.Quantity*f.UnitListPrice; f['DiscountAmount']=f.Quantity*(f.UnitListPrice-f.UnitSellingPrice)
f['YearMonth']=pd.to_datetime(f.OrderDate).dt.strftime('%Y-%m')
wb=xlsxwriter.Workbook(OUT); wb.set_properties({'title':'Pricing Optimization Dashboard Analysis','subject':'Synthetic retail pricing analytics','author':'Analytics Portfolio Project','comments':'Synthetic data only; no real company results.'})
navy='#17324D'; teal='#168C8C'; pale='#EAF2F8'; red='#FCE4D6'; green='#E2F0D9'; white='#FFFFFF'
header=wb.add_format({'bold':True,'font_color':white,'bg_color':navy,'border':0,'text_wrap':True,'valign':'vcenter'}); money=wb.add_format({'num_format':'#,##0.00;[Red](#,##0.00)'}); pct=wb.add_format({'num_format':'0.0%'}); integer=wb.add_format({'num_format':'#,##0'}); title=wb.add_format({'bold':True,'font_size':18,'font_color':navy}); sub=wb.add_format({'font_color':'#526575','italic':True}); kpi_label=wb.add_format({'bold':True,'font_color':white,'bg_color':navy,'align':'center','valign':'vcenter'}); kpi_val=wb.add_format({'bold':True,'font_size':15,'font_color':navy,'bg_color':pale,'align':'center','valign':'vcenter','num_format':'#,##0.00'}); note=wb.add_format({'text_wrap':True,'valign':'top'})
def write_df(name,df,table_name=None):
 ws=wb.add_worksheet(name); ws.freeze_panes(1,0); ws.set_row(0,30,header); ws.set_default_row(18)
 for j,col in enumerate(df.columns): ws.write(0,j,col,header)
 for i,row in enumerate(df.itertuples(index=False,name=None),1):
  for j,val in enumerate(row):
   if pd.isna(val): ws.write_blank(i,j,None)
   elif isinstance(val,(np.integer,int)): ws.write_number(i,j,int(val))
   elif isinstance(val,(np.floating,float)): ws.write_number(i,j,float(val))
   else: ws.write(i,j,str(val))
 for j,col in enumerate(df.columns):
  width=min(max(12,len(str(col))+2, max([len(str(x)) for x in df[col].head(100).tolist()]+[10])+1),32)
  ws.set_column(j,j,width)
 if table_name and len(df):
  # existing headers are written, add table formatting to data range
  ws.add_table(0,0,len(df),len(df.columns)-1,{'name':table_name,'style':'Table Style Medium 2','columns':[{'header':str(c)} for c in df.columns]})
 return ws
# Raw / clean and dimensions
rawws=write_df('Raw Data',raw,'RawSales'); clean_df=f.drop(columns=['GrossRevenueBeforeDiscount','DiscountAmount','YearMonth']); cleanws=write_df('Cleaned Data',clean_df,'CleanSales'); prodws=write_df('Product Master',p,'ProductMaster')
# Replace derived financial fields with live Excel formulas (cached values preserve preview in non-calculating viewers).
col_idx={name:i for i,name in enumerate(clean_df.columns)}
for excel_row, (_, rec) in enumerate(clean_df.iterrows(), start=1):
    r=excel_row+1
    for col_name, formula, cached in [
        ('UnitSellingPrice',f'=ROUND(I{r}*(1-J{r}),2)',rec.UnitSellingPrice),
        ('SalesRevenue',f'=ROUND(H{r}*K{r},2)',rec.SalesRevenue),
        ('CostOfGoodsSold',f'=ROUND(H{r}*L{r},2)',rec.CostOfGoodsSold),
        ('GrossProfit',f'=M{r}-N{r}',rec.GrossProfit),
        ('GrossMarginPct',f'=IFERROR(O{r}/M{r},0)',rec.GrossMarginPct)]:
        cleanws.write_formula(excel_row,col_idx[col_name],formula, money if col_name!='GrossMarginPct' else pct,float(cached))
cleanws.set_column(col_idx['UnitListPrice'],col_idx['UnitCost'],14,money); cleanws.set_column(col_idx['UnitSellingPrice'],col_idx['GrossProfit'],16,money); cleanws.set_column(col_idx['GrossMarginPct'],col_idx['GrossMarginPct'],16,pct)
# Data quality and methodology
qdf=pd.read_csv(D/'quarantined_rows.csv'); qsummary=pd.DataFrame([{'Metric':'Raw source rows','Value':len(raw)},{'Metric':'Cleaned fact rows','Value':len(f)},{'Metric':'Quarantined source rows','Value':len(qdf)},{'Metric':'Duplicate IDs in raw','Value':raw.SalesLineID.duplicated().sum()},{'Metric':'Products','Value':len(p)},{'Metric':'Categories','Value':p.Category.nunique()}]); qws=write_df('Data Quality',qsummary,'DataQualitySummary'); qws.write(len(qsummary)+2,0,'Rejected records are preserved in data/processed/quarantined_rows.csv. Review reasons before any remediation.',note); qws.set_column(0,0,34); qws.set_column(1,1,18)
method=pd.DataFrame([('Net Sales Revenue','Quantity × UnitSellingPrice','Currency; sum line values'),('Gross Revenue Before Discount','Quantity × UnitListPrice','Currency'),('Discount Amount','Quantity × (UnitListPrice − UnitSellingPrice)','Currency'),('COGS','Quantity × UnitCost','Currency'),('Gross Profit','Net Sales Revenue − COGS','Excludes operating expenses'),('Gross Margin %','Gross Profit ÷ Net Sales Revenue','Weighted at aggregate level'),('Weighted Average Discount %','Total Discount Amount ÷ Gross Revenue Before Discount','Not simple average of row discounts'),('Average Selling Price','Net Sales Revenue ÷ Units Sold','Currency/unit'),('Revenue per Order','Net Sales Revenue ÷ distinct OrderID','Generated data uses one line/order'),('Data disclosure','Synthetic data, fixed seed 20261028','No real customers or verified market prices')],columns=['Metric','Definition','Notes']); write_df('Methodology',method,'MetricDefinitions')
# analysis sheets
prod_agg=f.groupby(['ProductID','ProductName','Category']).agg(Revenue=('SalesRevenue','sum'),COGS=('CostOfGoodsSold','sum'),GrossProfit=('GrossProfit','sum'),Units=('Quantity','sum'),DiscountAmount=('DiscountAmount','sum'),ListValue=('GrossRevenueBeforeDiscount','sum')).reset_index(); prod_agg['MarginPct']=prod_agg.GrossProfit/prod_agg.Revenue; prod_agg['WeightedDiscountPct']=prod_agg.DiscountAmount/prod_agg.ListValue
pws=write_df('Pricing Analysis',prod_agg.sort_values('Revenue',ascending=False),'PricingAnalysis'); pws.set_column(4,6,15,money); pws.set_column(8,9,16,pct); pws.conditional_format(1,5,len(prod_agg),5,{'type':'cell','criteria':'<','value':0,'format':wb.add_format({'bg_color':red,'font_color':'#9C0006'})}); pws.conditional_format(1,9,len(prod_agg),9,{'type':'cell','criteria':'<','value':0.15,'format':wb.add_format({'bg_color':red})})
disc=f.groupby(pd.cut(f.DiscountPct,[-.000001,0,.05,.10,.20,.30,1],labels=['0%','>0-5%','>5-10%','>10-20%','>20-30%','>30%'],include_lowest=True),observed=False).agg(Revenue=('SalesRevenue','sum'),GrossProfit=('GrossProfit','sum'),Units=('Quantity','sum'),ListValue=('GrossRevenueBeforeDiscount','sum'),DiscountAmount=('DiscountAmount','sum')).reset_index(names='DiscountBand'); disc['MarginPct']=disc.GrossProfit/disc.Revenue.replace(0,np.nan); disc['WeightedDiscountPct']=disc.DiscountAmount/disc.ListValue.replace(0,np.nan); dws=write_df('Discount Analysis',disc,'DiscountAnalysis'); dws.set_column(1,2,16,money); dws.set_column(5,6,18,pct)
cat=f.groupby('Category').agg(Revenue=('SalesRevenue','sum'),GrossProfit=('GrossProfit','sum'),COGS=('CostOfGoodsSold','sum'),Units=('Quantity','sum'),ListValue=('GrossRevenueBeforeDiscount','sum'),DiscountAmount=('DiscountAmount','sum')).reset_index(); cat['MarginPct']=cat.GrossProfit/cat.Revenue; cat['WeightedDiscountPct']=cat.DiscountAmount/cat.ListValue; cws=write_df('Category Profitability',cat.sort_values('Revenue',ascending=False),'CategoryProfitability'); cws.set_column(1,3,16,money); cws.set_column(6,7,18,pct)
monthly=f.groupby('YearMonth').agg(Revenue=('SalesRevenue','sum'),GrossProfit=('GrossProfit','sum'),Units=('Quantity','sum'),ListValue=('GrossRevenueBeforeDiscount','sum'),DiscountAmount=('DiscountAmount','sum')).reset_index(); monthly['MarginPct']=monthly.GrossProfit/monthly.Revenue; monthly['WeightedDiscountPct']=monthly.DiscountAmount/monthly.ListValue; mws=write_df('Monthly Trends',monthly,'MonthlyTrends'); mws.set_column(1,2,16,money); mws.set_column(5,6,18,pct)
# Executive summary with calculated formula cells and category chart
ws=wb.add_worksheet('Executive Summary'); ws.hide_gridlines(2); ws.set_column('A:A',3); ws.set_column('B:G',20); ws.merge_range('B2:G2','PRICING OPTIMIZATION & PROFITABILITY',title); ws.merge_range('B3:G3','Synthetic retail dataset | 2024–2025 | Excel analysis workbook',sub)
labels=['Net Sales Revenue','Gross Profit','Gross Margin %','Weighted Average Discount %','Units Sold','Average Selling Price']; vals=[f.SalesRevenue.sum(),f.GrossProfit.sum(),f.GrossProfit.sum()/f.SalesRevenue.sum(),f.DiscountAmount.sum()/f.GrossRevenueBeforeDiscount.sum(),f.Quantity.sum(),f.SalesRevenue.sum()/f.Quantity.sum()]
for i,(lab,val) in enumerate(zip(labels,vals)):
 col=1+(i%3)*2; row=4+(i//3)*3
 ws.merge_range(row,col,row,col+1,lab,kpi_label)
 fmt=wb.add_format({'bold':True,'font_size':15,'font_color':navy,'bg_color':pale,'align':'center','valign':'vcenter','num_format':'0.0%' if '%' in lab else '#,##0.00' if lab not in ['Units Sold'] else '#,##0'})
 endrow=len(clean_df)+1
 formulas=[f"=SUM('Cleaned Data'!M2:M{endrow})", f"=SUM('Cleaned Data'!O2:O{endrow})", f"=IFERROR(SUM('Cleaned Data'!O2:O{endrow})/SUM('Cleaned Data'!M2:M{endrow}),0)", f"=IFERROR(SUMPRODUCT('Cleaned Data'!H2:H{endrow},'Cleaned Data'!I2:I{endrow}-'Cleaned Data'!K2:K{endrow})/SUMPRODUCT('Cleaned Data'!H2:H{endrow},'Cleaned Data'!I2:I{endrow}),0)", f"=SUM('Cleaned Data'!H2:H{endrow})", f"=IFERROR(SUM('Cleaned Data'!M2:M{endrow})/SUM('Cleaned Data'!H2:H{endrow}),0)"]
 ws.merge_range(row+1,col,row+1,col+1,'',fmt)
 ws.write_formula(row+1,col,formulas[i],fmt,float(val))
ws.write('B12','Category performance (values are calculated from Cleaned Data)',header); ws.write('B13','Category',header); ws.write('C13','Revenue',header); ws.write('D13','Gross Profit',header); ws.write('E13','Margin %',header)
for i,row in enumerate(cat.sort_values('Revenue',ascending=False).itertuples(index=False),13): ws.write(i,1,row.Category); ws.write_number(i,2,row.Revenue,money); ws.write_number(i,3,row.GrossProfit,money); ws.write_number(i,4,row.MarginPct,pct)
chart=wb.add_chart({'type':'column'}); chart.add_series({'name':'Revenue','categories':['Executive Summary',13,1,12+len(cat),1],'values':['Executive Summary',13,2,12+len(cat),2],'fill':{'color':teal}}); chart.set_title({'name':'Net Sales Revenue by Category'}); chart.set_y_axis({'name':'Revenue','num_format':'#,##0'}); chart.set_legend({'none':True}); chart.set_size({'width':720,'height':360}); ws.insert_chart('G12',chart)
ws.merge_range('B27:G29','Interpretation: gross profit excludes shipping, taxes, returns, payment fees, marketing, and other operating expenses. Discount relationships are observational and do not establish causality. Filter the Excel Tables on the data sheets to explore dimensions.',note)
ws.freeze_panes(4,1)
wb.close(); print(f'Created {OUT} ({OUT.stat().st_size:,} bytes)')
