from pathlib import Path
import pandas as pd

# FIXED: 검토 대상으로 제외할 가격·수량의 상한을 명시한다.
MAX_PRICE = 100_000
MAX_QUANTITY = 1_000


def load(path):
    return pd.read_csv(path, encoding="utf-8")


def summarize(df):
    # FIXED: 함수 밖의 원본 데이터를 변경하지 않도록 복사한다.
    df = df.copy()

    # FIXED: 가격의 쉼표·원 기호·공백을 제거한 뒤 숫자로 변환한다.
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

    # FIXED: 가격 결측과 설정한 가격·수량 범위 밖의 행을 제외한다.
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

    # FIXED: 카테고리 결측으로 매출이 집계에서 빠지지 않도록 처리한다.
    df["category"] = (
        df["category"].astype("string").str.strip()
        .replace("", pd.NA).fillna("미분류")
    )

    # FIXED: 존재하지 않는 단가·수량 대신 실제 열 이름을 사용한다.
    df["매출액"] = df["price"] * df["quantity"]
    result = df.groupby("category")["매출액"].sum()

    # FIXED: 카테고리별 합계가 전체 유효 거래 매출과 같은지 확인한다.
    assert result.sum() == df["매출액"].sum(), "카테고리 집계에서 매출 누락"
    return result


if __name__ == "__main__":
    # FIXED: 실행 위치와 관계없이 스크립트 옆의 CSV를 읽는다.
    input_path = Path(__file__).resolve().parent / "dirty_sales.csv"
    result = summarize(load(input_path))

    print("\n카테고리별 유효 거래 매출:")
    print(result.to_string())
    print(f"\n유효 거래 매출 합계: {result.sum():,}원")