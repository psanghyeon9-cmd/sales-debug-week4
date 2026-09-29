from pathlib import Path
import pandas as pd

MAX_PRICE = 100_000
MAX_QUANTITY = 1_000


def load_and_clean(path):
    df = pd.read_csv(path, encoding="utf-8")

    # FIXED: 집계 전에 원본 데이터의 결측 규모를 보고한다.
    print(f"원본 행 수: {len(df)}")
    print("\n열별 결측치 수:")
    print(df.isna().sum().to_string())

    # FIXED: 가격 표기를 정리하고 결측을 유지하며 숫자로 변환한다.
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

    # FIXED: 가격 결측과 설정 범위 밖의 거래를 구분하여 제외한다.
    missing_price = df["price"].isna()
    valid = (
        df["price"].between(1, MAX_PRICE)
        & df["quantity"].between(1, MAX_QUANTITY)
    ).fillna(False)
    review = ~valid & ~missing_price

    print(f"\n가격 결측 제외: {int(missing_price.sum())}건")
    print(f"가격/수량 검토 대상 제외: {int(review.sum())}건")

    df = df.loc[valid].copy()

    # FIXED: 카테고리 결측 때문에 유효 거래를 삭제하지 않는다.
    df["category"] = (
        df["category"].astype("string").str.strip()
        .replace("", pd.NA).fillna("미분류")
    )

    # FIXED: 결측·검토 대상 처리 후 남은 거래로 매출을 계산한다.
    df["revenue"] = df["price"] * df["quantity"]
    return df


def main():
    # FIXED: 실행 위치와 관계없이 스크립트 옆의 CSV를 읽는다.
    input_path = Path(__file__).resolve().parent / "dirty_sales.csv"
    df = load_and_clean(input_path)

    # FIXED: 전체 원본 매출로 오해하지 않도록 집계 대상을 명시한다.
    print(f"\n집계 행 수: {len(df)}")
    print(f"유효 거래 매출 합계: {df['revenue'].sum():,}원")

    if df.empty:
        print("유효 거래 평균 단가: 계산할 거래 없음")
    else:
        print(f"유효 거래 평균 단가: {df['price'].mean():,.2f}원")


if __name__ == "__main__":
    main()