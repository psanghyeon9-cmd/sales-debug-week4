from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
from buggy_3 import load_and_clean


sample = pd.DataFrame({
    "category": ["음료", "음료", "베이커리"],
    "price": ["4500", "5,200", "4200원"],
    "quantity": [2, 2, 3],
})

with TemporaryDirectory() as temp_dir:
    sample_path = Path(temp_dir) / "normal_sales.csv"
    sample.to_csv(sample_path, index=False, encoding="utf-8")

    result = load_and_clean(sample_path)

    assert isinstance(result, pd.DataFrame), "DataFrame 반환 실패"
    assert len(result) == 3, "정상 거래가 제외됨"
    assert result["revenue"].tolist() == [9000, 10400, 12600], "행별 매출 오류"
    assert result["revenue"].sum() == 32000, "총매출 오류"

    print("정상 데이터 검증 통과")
    print("DataFrame 반환 확인")
    print("정상 거래 3건 유지")
    print(f"매출 합계: {result['revenue'].sum():,}원")