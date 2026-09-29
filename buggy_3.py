from pathlib import Path
import pandas as pd

MAX_PRICE = 100_000
MAX_QUANTITY = 1_000


def load_and_clean(path):
    df = pd.read_csv(path, encoding="utf-8")

    # FIXED: 가격의 쉼표·원 기호·공백을 제거하고 숫자로 변환한다.
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

    # FIXED: 앞선 스크립트와 동일한 기준으로 결측·검토 대상 행을 제외한다.
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

    # FIXED: 카테고리 결측으로 매출이 집계에서 누락되는 것을 막는다.
    df["category"] = (
        df["category"].astype("string").str.strip()
        .replace("", pd.NA).fillna("미분류")
    )
    df["revenue"] = df["price"] * df["quantity"]

    # FIXED: 반환문 누락으로 None이 전달되던 문제를 해결한다.
    return df


def main():
    # FIXED: 실행 위치와 관계없이 스크립트 옆의 CSV를 읽는다.
    input_path = Path(__file__).resolve().parent / "dirty_sales.csv"
    df = load_and_clean(input_path)
    result = df.groupby("category")["revenue"].sum()

    # FIXED: 카테고리 집계 과정에서 매출이 누락되지 않았는지 검증한다.
    assert result.sum() == df["revenue"].sum(), "카테고리 집계에서 매출 누락"

    print("\n반환값 자료형:", type(df))
    print("\n카테고리별 유효 거래 매출:")
    print(result.to_string())
    print(f"\n유효 거래 매출 합계: {result.sum():,}원")


if __name__ == "__main__":
    main()