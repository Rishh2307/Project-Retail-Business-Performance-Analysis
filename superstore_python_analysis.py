# superstore_python_analysis.py
import os
import pandas as pd
import matplotlib.pyplot as plt

# ---- CHANGE THIS to match your file name if you renamed it ----
DATA_PATH = r"C:\SuperstorePython\Superstore_Sales_Dataset.csv"
# If you kept spaces, use:
# DATA_PATH = r"C:\SuperstorePython\Superstore Sales Dataset.csv"

OUT_DIR = r"C:\SuperstorePython\py_outputs"
os.makedirs(OUT_DIR, exist_ok=True)

# Load CSV
df = pd.read_csv(DATA_PATH, encoding="latin1")

# Clean column names: replace spaces/dashes with underscore
df.columns = df.columns.str.strip().str.replace(r"[^0-9a-zA-Z]+", "_", regex=True)

# Convert types
if "Order_Date" in df.columns:
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

for col in ["Sales", "Profit", "Discount", "Quantity"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Sales", "Profit"])  # require numeric core columns

def save_fig(name):
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, name), dpi=200)
    plt.close()

# Analysis 1: Category summary
cat = df.groupby("Category")[["Sales","Profit"]].sum().reset_index()
cat["profit_margin_pct"] = (cat["Profit"]/cat["Sales"]*100).round(2)
cat.to_csv(os.path.join(OUT_DIR, "category_summary.csv"), index=False)
ax = cat.plot(x="Category", y=["Sales","Profit"], kind="bar")
plt.title("Sales & Profit by Category")
save_fig("category_summary.png")

# Analysis 2: Monthly trend (if Order_Date exists)
if "Order_Date" in df.columns:
    df["YearMonth"] = df["Order_Date"].dt.to_period("M")
    monthly = df.groupby("YearMonth")[["Sales","Profit"]].sum().reset_index()
    monthly["YearMonth"] = monthly["YearMonth"].astype(str)
    monthly.to_csv(os.path.join(OUT_DIR, "monthly_trend.csv"), index=False)
    monthly.plot(x="YearMonth", y=["Sales","Profit"])
    plt.title("Monthly Sales & Profit Trend")
    plt.xticks(rotation=45)
    save_fig("monthly_trend.png")

# Analysis 3: Ship Mode summary (if exists)
if "Ship_Mode" in df.columns:
    ship = df.groupby("Ship_Mode")[["Sales","Profit"]].sum().reset_index()
    ship["profit_margin_pct"] = (ship["Profit"]/ship["Sales"]*100).round(2)
    ship.to_csv(os.path.join(OUT_DIR, "ship_mode_summary.csv"), index=False)
    ship.plot(x="Ship_Mode", y=["Sales","Profit"], kind="bar")
    plt.title("Sales & Profit by Ship Mode")
    save_fig("ship_mode_summary.png")

# Analysis 4: Top 10 loss-making products
loss = df.groupby("Product_Name")[["Sales","Profit"]].sum().sort_values("Profit").head(10).reset_index()
loss.to_csv(os.path.join(OUT_DIR, "top10_loss_products.csv"), index=False)
loss.plot(x="Product_Name", y="Profit", kind="barh", color='red')
plt.title("Top 10 Loss-Making Products")
save_fig("top10_loss_products.png")

print("Done. Outputs in:", OUT_DIR)