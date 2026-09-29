from pathlib import Path
import pandas as pd

input_path = Path(__file__).resolve().parent / "dirty_sales.csv"
df = pd.read_csv(input_path, encoding="utf-8")

print("데이터 구조:")
df.info()

print("\n열별 결측치 수:")
print(df.isna().sum())

price_text = (
    df["price"].astype("string")
    .str.replace(",", "", regex=False)
    .str.replace("원", "", regex=False)
    .str.strip()
)
df["price"] = pd.to_numeric(price_text, errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

print("\n가격·수량 통계:")
print(df[["price", "quantity"]].describe().to_string())

print("\n가격 결측 행:")
print(df.loc[df["price"].isna()].to_string(index=False))

review = (
    (df["price"] <= 0)
    | (df["price"] > 100_000)
    | (df["quantity"] <= 0)
    | (df["quantity"] > 1_000)
).fillna(False)

print("\n앞서 정한 가격·수량 기준의 검토 대상:")
print(df.loc[review].to_string(index=False))

revenue = df["price"] * df["quantity"]
print(f"\n매출액을 계산할 수 없는 행 수: {int(revenue.isna().sum())}")