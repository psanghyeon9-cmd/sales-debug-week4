# buggy_5.py 추가 검토 질문 전문

## ① 맥락

CSV에서 이웃한 두 행의 가격 차이가 큰 구간을 찾는 코드입니다. 인덱스 오류를 수정했지만, 결측 가격과 극단 가격을 처리하는 방식이 탐지 결과에 어떤 영향을 주는지도 검토하고 싶습니다.

## ② 코드

```python
def find_big_jumps(prices, threshold=100_000):
    jumps = []
    for i in range(len(prices) - 1):
        current = prices[i]
        following = prices[i + 1]
        if pd.isna(current) or pd.isna(following):
            continue
        diff = following - current
        if abs(diff) >= threshold:
            jumps.append((i, current, following, diff))
    return jumps
```

원본은 `range(len(prices))`를 사용했고, CSV의 결측 가격은 `fillna(0)`으로 대체했습니다. 수정 후에는 결측 가격과 원래 위치를 유지합니다.

## ③ Traceback

원본 실행 시 저장한 오류 로그 전문입니다.

```text
.\.venv\Scripts\python.exe : Traceback (most recent call las
t):
위치 줄:1 문자:1
+ .\.venv\Scripts\python.exe buggy_5.py 2>&1 | Tee-Object -F
ilePath evi ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (mos 
   t recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
  File "C:\Users\psang\Documents\sales-debug-week4\buggy_5.p
y", line 36, in <module>
    jumps = find_big_jumps(prices)
  File "C:\Users\psang\Documents\sales-debug-week4\buggy_5.p
y", line 29, in find_big_jumps
    diff = prices[i + 1] - prices[i]      # <-- 여기가 문제의 줄
           ~~~~~~^^^^^^^
IndexError: list index out of range
```

## ④ 확인한 것과 검토할 가설

직접 확인한 리스트 길이는 500, 마지막 유효 인덱스는 499, 마지막 반복에서 접근하려던 인덱스는 500입니다. 수정 후에는 가격 결측 2건을 유지하고 249→250, 250→251에서 급변 2건을 찾았습니다. 정상 데이터, 빈 리스트, 가격 1개, 임계값 경계 및 결측 구간 검증도 통과했습니다.

추가 검토할 가설은 '결측을 0으로 채우면 가짜 변화를 만들 수 있고, 결측 행을 삭제하면 원래 이웃하지 않은 가격을 비교할 수 있으므로 해당 비교 쌍만 건너뛰어야 한다'입니다. 이 가설은 AI가 제안한 수정 방식의 근거로, 반례를 통해 더 확인하고 싶습니다.

## ⑤ 요청

반복 범위 변경이 빈 리스트와 가격 1개에서도 안전한 이유를 설명해 주세요. `[100, None, 200000, 4500]`을 예로 들어 0 대체, 결측 행 삭제, 비교 쌍 건너뛰기를 비교해 주세요. 4번과 달리 여기서 극단 가격을 유지하는 이유와, 서로 다른 상품이 섞인 행 순서의 가격 차이를 해석할 때의 한계도 설명해 주세요.
