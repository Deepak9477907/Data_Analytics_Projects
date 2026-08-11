import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "Superstore.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
df.columns = [c.strip() for c in df.columns]

for c in ["Order Date", "Ship Date"]:
    if c in df:
        df[c] = pd.to_datetime(df[c], errors="coerce")

for c in ["Sales", "Quantity", "Discount", "Profit"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df = df.drop_duplicates().copy()

for c in ["Sales", "Quantity", "Discount", "Profit"]:
    df[c] = df[c].fillna(df[c].median())

df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)
df["Profit Margin %"] = df["Profit"].div(df["Sales"].replace(0, pd.NA)).fillna(0) * 100

df.to_csv(OUT/"superstore_cleaned.csv", index=False)

kpis = pd.DataFrame({
    "Metric": ["Rows","Orders","Customers","Sales","Profit","Quantity","Average Discount","Profit Margin %"],
    "Value": [
        len(df), df["Order ID"].nunique(), df["Customer ID"].nunique(),
        df["Sales"].sum(), df["Profit"].sum(), df["Quantity"].sum(),
        df["Discount"].mean(), df["Profit"].sum()/df["Sales"].sum()*100
    ]
})
kpis.to_csv(OUT/"kpi_summary.csv", index=False)

monthly = df.groupby("Year-Month", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
monthly.to_csv(OUT/"monthly_sales_profit.csv", index=False)

region = df.groupby("Region", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Quantity=("Quantity","sum"))
region["Profit Margin %"] = region["Profit"]/region["Sales"]*100
region.to_csv(OUT/"region_summary.csv", index=False)

category = df.groupby(["Category","Sub-Category"], as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Quantity=("Quantity","sum"))
category.to_csv(OUT/"category_summary.csv", index=False)

print(kpis.to_string(index=False))
