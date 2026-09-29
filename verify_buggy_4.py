from math import isclose
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
from buggy_4 import load_and_clean


sample = pd.DataFrame({
    "category": ["음료", "음료", "베이커리"],
    "price": ["4500", "5,200", "4200원"],
    "quantity": [2, 2, 3],
    "stock": [10, 20, 30],
})

with TemporaryDirectory() as temp_dir:
    sample_path = Path(temp_dir) / "normal_sales.csv"
    sample.to_csv(sample_path, index=False, encoding="utf-8")

    result = load_and_clean(sample_path)

    assert len(result) == 3, "정상 거래가 제외됨"
    assert result["revenue"].tolist() == [9000, 10400, 12600], "행별 매출 오류"
    assert result["revenue"].sum() == 32000, "매출 합계 오류"
    assert isclose(
        float(result["price"].mean()),
        (4500 + 5200 + 4200) / 3,
    ), "평균 단가 오류"

    print("\n정상 데이터 검증 통과")
    print(f"매출 합계: {result['revenue'].sum():,}원")
    print(f"평균 단가: {result['price'].mean():,.2f}원")