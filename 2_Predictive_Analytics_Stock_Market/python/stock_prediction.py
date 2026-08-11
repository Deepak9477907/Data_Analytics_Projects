from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "stock.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
df.columns = [c.strip() for c in df.columns]
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.sort_values("Date").drop_duplicates().reset_index(drop=True)

for c in ["Open","High","Low","Close","Volume"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna(subset=["Close"]).copy()

# Feature engineering
df["Return_1D"] = df["Close"].pct_change()
df["MA_5"] = df["Close"].rolling(5).mean()
df["MA_20"] = df["Close"].rolling(20).mean()
delta = df["Close"].diff()
gain = delta.clip(lower=0).rolling(14).mean()
loss = (-delta.clip(upper=0)).rolling(14).mean()
rs = gain / loss.replace(0, np.nan)
df["RSI_14"] = 100 - (100 / (1 + rs))

# Target: next-day direction (1 = up, 0 = down)
df["Next_Return"] = df["Close"].shift(-1) / df["Close"] - 1
df["Target"] = (df["Next_Return"] > 0).astype(int)

features = ["Return_1D", "MA_5", "MA_20", "RSI_14", "Volume"]
model_df = df.dropna(subset=features + ["Target"]).copy()

# Chronological split — no random shuffle for time series
split = int(len(model_df) * 0.8)
train = model_df.iloc[:split]
test = model_df.iloc[split:]

X_train, X_test = train[features], test[features]
y_train, y_test = train["Target"], test["Target"]

model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)
pred = model.predict(X_test)

metrics = pd.DataFrame({
    "Metric": ["Accuracy","Precision","Recall","F1"],
    "Value": [
        accuracy_score(y_test, pred),
        precision_score(y_test, pred, zero_division=0),
        recall_score(y_test, pred, zero_division=0),
        f1_score(y_test, pred, zero_division=0)
    ]
})
metrics.to_csv(OUT/"model_metrics.csv", index=False)

results = test[["Date","Close","Target"]].copy()
results["Predicted_Direction"] = pred
results.to_csv(OUT/"predictions.csv", index=False)

plt.figure(figsize=(11,5))
plt.plot(results["Date"], results["Close"])
plt.title("Test-Period Stock Closing Price")
plt.xlabel("Date")
plt.ylabel("Close")
plt.tight_layout()
plt.savefig(OUT/"test_period_price.png", dpi=160)
plt.close()

print(metrics.to_string(index=False))
print("\nConfusion matrix:")
print(confusion_matrix(y_test, pred))
