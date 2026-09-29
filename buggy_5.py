from pathlib import Path
import pandas as pd


def load_prices(path):
    df = pd.read_csv(path, encoding="utf-8")

    price_text = (
        df["price"].astype("string")
        .str.replace(",", "", regex=False)
        .str.replace("원", "", regex=False)
        .str.strip()
    )

    # FIXED: 결측을 0으로 바꾸지 않고 원래 행 위치와 함께 유지한다.
    return pd.to_numeric(price_text, errors="raise").tolist()


def find_big_jumps(prices, threshold=100_000):
    jumps = []

    # FIXED: i + 1이 마지막 유효 인덱스를 넘지 않도록 범위를 줄인다.
    for i in range(len(prices) - 1):
        current = prices[i]
        following = prices[i + 1]

        # FIXED: 가격을 알 수 없는 쌍은 비교하지 않는다.
        if pd.isna(current) or pd.isna(following):
            continue

        diff = following - current
        if abs(diff) >= threshold:
            jumps.append((i, current, following, diff))

    return jumps


def main():
    # FIXED: 실행 위치와 관계없이 스크립트 옆의 CSV를 읽는다.
    input_path = Path(__file__).resolve().parent / "dirty_sales.csv"
    prices = load_prices(input_path)

    print(f"가격 데이터 수: {len(prices)}")
    print(f"가격 결측 수: {sum(pd.isna(p) for p in prices)}")

    # FIXED: 급변 기준으로 놓칠 수 있는 음수 가격도 별도로 표시한다.
    print("\n가격 검토 대상 (0 이하 또는 100,000원 초과):")
    for i, price in enumerate(prices):
        if pd.isna(price):
            continue
        if price <= 0 or price > 100_000:
            print(f"인덱스 {i}: {price:,}원")

    jumps = find_big_jumps(prices)

    print(f"\n급변 지점 {len(jumps)}건")
    for i, current, following, diff in jumps:
        print(
            f"인덱스 {i} → {i + 1}: "
            f"{current:,}원 → {following:,}원 "
            f"(변화량 {diff:+,}원)"
        )


if __name__ == "__main__":
    main()