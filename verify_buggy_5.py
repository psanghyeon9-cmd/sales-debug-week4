from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
from buggy_5 import load_prices, find_big_jumps


with TemporaryDirectory() as temp_dir:
    sample_path = Path(temp_dir) / "normal_prices.csv"

    pd.DataFrame({
        "price": ["4500", "5,200", "4200원"],
    }).to_csv(sample_path, index=False, encoding="utf-8")

    prices = load_prices(sample_path)

    assert prices == [4500, 5200, 4200], "가격 정제 오류"
    assert find_big_jumps(prices) == [], "정상 가격을 급변으로 잘못 탐지"
    assert find_big_jumps(prices, threshold=1000) == [
        (1, 5200, 4200, -1000)
    ], "변화량 또는 임계값 경계 처리 오류"

    print("정상 데이터 검증 통과")

    assert find_big_jumps([]) == [], "빈 리스트 처리 오류"
    assert find_big_jumps([4500]) == [], "가격 1개 처리 오류"
    assert find_big_jumps([1000, 101000]) == [
        (0, 1000, 101000, 100000)
    ], "상승 변화량 처리 오류"

    print("반복문 경계 검증 통과")

    pd.DataFrame({
        "price": ["100", None, "200000", "4500"],
    }).to_csv(sample_path, index=False, encoding="utf-8")

    prices = load_prices(sample_path)

    assert len(prices) == 4, "원래 행 위치가 변경됨"
    assert pd.isna(prices[1]), "결측 가격이 다른 값으로 대체됨"
    assert find_big_jumps(prices) == [
        (2, 200000, 4500, -195500)
    ], "결측 구간 비교 또는 원래 인덱스 유지 오류"

    print("결측값 및 인덱스 유지 검증 통과")

print("전체 검증 통과")