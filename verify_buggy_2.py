import pandas as pd

from buggy_2 import summarize


normal = pd.DataFrame({
    "category": ["음료", "음료", "베이커리"],
    "price": ["4500", "5,200", "4200원"],
    "quantity": [2, 2, 3],
})

result = summarize(normal)

expected = {"음료": 19_400, "베이커리": 12_600}

assert result.to_dict() == expected, "정상 데이터의 카테고리별 합계 오류"
assert result.sum() == 32_000, "정상 데이터의 전체 합계 오류"
print("정상 데이터 검증 통과: 32,000원")

missing_category = normal.copy()
missing_category.loc[0, "category"] = pd.NA

result = summarize(missing_category)

assert result.loc["미분류"] == 9_000, "미분류 거래 처리 오류"
assert result.sum() == 32_000, "카테고리 결측으로 매출이 누락됨"
print("카테고리 결측 검증 통과: 누락 없이 32,000원")