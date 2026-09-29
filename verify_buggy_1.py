import csv
from pathlib import Path
from tempfile import TemporaryDirectory

from buggy_1 import calc_total


# 원본 CSV를 건드리지 않고 임시 정상 데이터를 만들어 검증한다.
with TemporaryDirectory() as temp_dir:
    sample_path = Path(temp_dir) / "normal_sales.csv"

    with open(sample_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([
            ["price", "quantity"],
            ["4500", 2],
            ["5,200", 2],
            ["4200원", 3],
        ])

    # 직접 계산: 9,000 + 10,400 + 12,600 = 32,000
    expected = 32_000
    actual = calc_total(sample_path)

    assert actual == expected, (
        f"정상 데이터 검증 실패: 예상 {expected}, 실제 {actual}"
    )

    print(f"정상 데이터 검증 통과: {actual:,}원")