# 4주차 디버깅 진단 보고서

아래 줄 번호는 수정 전 원본 커밋 `5f8a273` 기준이다. 수정 내용은 각 파일의 `# FIXED:` 주석과 Git 이력에 남겼다.

## buggy_1.py

- **무엇이:** `ValueError: invalid literal for int() with base 10: '5,200'`가 발생했다. 최초 실행에서는 잘못된 입력 경로로 `FileNotFoundError`도 발생했다.
- **어디서:** 원본 19행 `price = int(row["price"])`에서 숫자 변환에 실패했다. 경로 오류는 25행에서 전달한 `./Week4/dirty_sales.csv`를 16행에서 열 때 발생했다.
- **왜:** `price`에 쉼표가 포함된 문자열이 들어 있었다. 쉼표·원 기호·공백을 제거하고 결측 및 검토 대상 거래를 제외했으며, 입력 경로를 스크립트 위치 기준으로 수정했다.

## buggy_2.py

- **무엇이:** `KeyError: '단가'`가 발생했다.
- **어디서:** 원본 20행 `df["매출액"] = df["단가"] * df["수량"]`에서 존재하지 않는 열을 조회했다.
- **왜:** `df.columns.tolist()`의 실제 열은 `date, product, category, price, quantity, stock`이었다. `price`와 `quantity`로 수정하고 숫자 정제 및 카테고리 결측의 `미분류` 처리를 적용했다.

## buggy_3.py

- **무엇이:** `AttributeError: 'NoneType' object has no attribute 'groupby'`가 발생했다.
- **어디서:** 원본 28행 `df.groupby("category")["revenue"].sum()`에서 발생했으며, `df`를 만든 15행의 `load_and_clean()` 함수를 역추적했다.
- **왜:** 직접 호출한 반환값은 `None`, 자료형은 `NoneType`이었다. 함수에 반환문이 없어 정제한 데이터가 전달되지 않았으므로 마지막에 `return df`를 추가했다.

## buggy_4.py

- **무엇이:** 예외 없이 총매출 151,198,388,824원, 평균 단가 28,342원이 출력됐지만 결측과 극단값을 처리하지 않은 집계였다.
- **어디서:** 원본 31행 `df["revenue"].sum()`과 32행 `df["price"].mean()`에서 문제가 드러났다.
- **왜:** `info()`, 결측치 수, `describe()`로 가격 결측 2건, 가격 -4,500 및 9,999,999, 수량 9,999,999를 확인했다. 결측 매출은 합계에서 제외되는 반면 극단값은 포함되어 결과가 왜곡됐다. 처리 기준과 제외 규모를 보고하고 유효 거래의 합계·평균을 계산했다.

## buggy_5.py

- **무엇이:** `IndexError: list index out of range`가 발생했다.
- **어디서:** 원본 29행 `diff = prices[i + 1] - prices[i]`에서 발생했다.
- **왜:** 리스트 길이 500, 마지막 유효 인덱스 499인데 마지막 반복에서 500에 접근했다. 반복 범위를 `range(len(prices) - 1)`로 수정했다. 결측 가격은 0으로 대체하거나 행을 삭제하지 않고 해당 비교 쌍만 건너뛰어 원래 인덱스를 유지했다. 인덱스 상태는 출력으로 확인했으며 조건부 중단점은 사용하지 않았다.

## 결측·검토 대상 처리 기준

- 원본은 500행이며 가격 결측 2건(0.4%), 카테고리 결측 10건(2%), 재고 결측 15건(3%)이다. 열별 결측 건수는 서로 겹칠 수 있다.
- 1~4번 매출 집계는 가격 결측 2건을 임의로 채우지 않고 제외한다. `0 < 가격 <= 100,000`, `0 < 수량 <= 1,000` 기준 밖의 거래 3건도 제외하여 495건을 집계한다.
- 상한은 이번 분석에서 정한 검토 기준이며, 실제 업무에서 확정된 정상 범위는 아니다. 결과 438,939,400원은 제외된 거래의 실제 매출을 복원한 전체 매출이 아니라 **유효 거래의 합계**다.
- 카테고리 결측은 2~4번에서 `미분류`로 유지한다. 재고는 매출 계산에 쓰이지 않으므로 결측을 이유로 거래를 삭제하지 않는다. 4번 평균 단가는 유효 거래 행의 가격에 대한 단순 평균이다.
- 5번은 급변 탐지가 목적이므로 극단 가격을 유지한다. 차이의 절댓값이 100,000원 이상인 구간을 찾고, 0 이하 또는 100,000원 초과 가격은 별도로 표시한다. 서로 다른 상품도 포함된 행 순서의 비교이므로 동일 상품의 시계열 변화로 해석하지 않는다.

## 검증 증빙

정상 샘플의 기대 매출은 `4,500×2 + 5,200×2 + 4,200×3 = 32,000원`으로 계산했다. 표의 결과는 저장된 실행 로그 기준이다.

| 파일 | 수정 후 실행 | 정상 데이터 검증 | 수정 커밋 |
|---|---|---|---|
| buggy_1.py | 495건, 438,939,400원 | 3건 유지, 32,000원 | `5942215` |
| buggy_2.py | 카테고리 합계 438,939,400원 | 32,000원 및 카테고리 결측 시 합계 유지 | `8519399` |
| buggy_3.py | DataFrame 반환, 438,939,400원 | DataFrame·3건·행별 매출·32,000원 확인 | `4d7e12c` |
| buggy_4.py | 495건, 438,939,400원, 평균 단가 8,290.91원 | 32,000원, 평균 단가 4,633.33원 | `ee76169` |
| buggy_5.py | 인덱스 249→250, 250→251에서 급변 2건 | 정상 가격·상승/하락·임계값 경계·빈 목록·1개 값·결측 구간 검증 | `9a66fbb` |

- 1번: [경로 오류](evidence/buggy_1_before_path.txt), [변환 오류](evidence/buggy_1_before_value.txt), [수정 후](evidence/buggy_1_after.txt), [정상 검증](evidence/buggy_1_normal_check.txt)
- 2번: [오류](evidence/buggy_2_before.txt), [열 이름](evidence/buggy_2_columns.txt), [수정 후](evidence/buggy_2_after.txt), [정상 검증](evidence/buggy_2_normal_check.txt)
- 3번: [오류](evidence/buggy_3_before.txt), [반환값](evidence/buggy_3_return_check.txt), [수정 후](evidence/buggy_3_after.txt), [정상 검증](evidence/buggy_3_normal_check.txt)
- 4번: [수정 전](evidence/buggy_4_before.txt), [데이터 진단](evidence/buggy_4_inspect.txt), [수정 후](evidence/buggy_4_after.txt), [정상 검증](evidence/buggy_4_normal_check.txt)
- 5번: [오류](evidence/buggy_5_before.txt), [인덱스](evidence/buggy_5_index_check.txt), [수정 후](evidence/buggy_5_after.txt), [정상 검증](evidence/buggy_5_normal_check.txt)

원본 데이터는 수정하지 않았다. 검증용 코드는 `verify_buggy_1.py`부터 `verify_buggy_5.py`에 있으며, 4번 데이터 진단 코드는 `inspect_buggy_4.py`에 있다.
