from pathlib import Path
import pandas as pd

MAX_PRICE = 100_000
MAX_QUANTITY = 1_000


def load(path):
    return pd.read_csv(path, encoding="utf-8")


def summarize(df):
    df = df.copy()

    price_text = (
        df["price"].astype("string")
        .str.replace(",", "", regex=False)
        .str.replace("원", "", regex=False)
        .str.strip()
    )
    df["price"] = pd.to_numeric(
        price_text, errors="raise"
    ).astype("Int64")

    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="raise"
    ).astype("Int64")

    missing_price = df["price"].isna()
    valid = (
        df["price"].between(1, MAX_PRICE)
        & df["quantity"].between(1, MAX_QUANTITY)
    ).fillna(False)

    print(f"집계 행 수: {int(valid.sum())}")
    print(f"가격 결측 제외: {int(missing_price.sum())}건")
    print(
        "가격/수량 검토 대상 제외: "
        f"{int((~valid & ~missing_price).sum())}건"
    )
    df = df.loc[valid].copy()

    df["category"] = (
        df["category"].astype("string").str.strip()
        .replace("", pd.NA).fillna("미분류")
    )

    df["매출액"] = df["price"] * df["quantity"]
    result = df.groupby("category")["매출액"].sum()

    assert result.sum() == df["매출액"].sum(), "카테고리 집계에서 매출 누락"
    return result


if __name__ == "__main__":
    input_path = Path(__file__).resolve().parent / "dirty_sales.csv"
    result = summarize(load(input_path))

    print("\n카테고리별 유효 거래 매출:")
    print(result.to_string())
    print(f"\n유효 거래 매출 합계: {result.sum():,}원")