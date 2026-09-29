import csv
from pathlib import Path

# FIXED: 이상치를 제외하기 위한 과제용 검토 기준을 명시한다.
MAX_PRICE = 100_000
MAX_QUANTITY = 1_000


def calc_total(path):
    total = 0
    valid_count = 0
    missing_count = 0
    outlier_count = 0

    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # FIXED: 쉼표, 원 표시, 주변 공백을 제거한다.
            price_text = (
                row["price"]
                .replace(",", "")
                .replace("원", "")
                .strip()
            )

            # FIXED: 가격 결측을 0으로 채우지 않고 제외 건수를 기록한다.
            if price_text == "":
                missing_count += 1
                continue

            price = int(price_text)
            qty = int(row["quantity"])

            # FIXED: 가격과 수량의 이상치가 합계를 왜곡하지 않도록 제외한다.
            if not (
                0 < price <= MAX_PRICE
                and 0 < qty <= MAX_QUANTITY
            ):
                outlier_count += 1
                continue

            total += price * qty
            valid_count += 1

    print(f"집계 행 수: {valid_count}")
    print(f"가격 결측 제외: {missing_count}건")
    print(f"가격/수량 이상치 제외: {outlier_count}건")
    return total


if __name__ == "__main__":
    # FIXED: 실행 위치와 관계없이 스크립트 옆의 CSV를 읽는다.
    input_path = Path(__file__).resolve().parent / "dirty_sales.csv"
    total = calc_total(input_path)
    print(f"유효 거래 매출 합계: {total:,}원")