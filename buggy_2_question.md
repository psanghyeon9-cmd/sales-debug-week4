# buggy_2.py 구조화된 질문

## ① 맥락

dirty_sales.csv를 pandas로 읽어 단가 × 수량으로 매출액을 계산하고,
카테고리별 매출 합계를 구하려는 코드입니다.

## ② 코드

```python
def summarize(df):
    # 단가 x 수량으로 매출액 컬럼을 만든 뒤 카테고리별 합계를 낸다
    df["매출액"] = df["단가"] * df["수량"]        # <-- 여기가 문제의 줄
    return df.groupby("category")["매출액"].sum()
```

## ③ Traceback

다음은 원본 실행 시 저장한 오류 로그 전문입니다.
PowerShell이 stderr를 표시하며 추가한 메시지도 포함했습니다.

```text
.\.venv\Scripts\python.exe : Traceback (most recent call last):
위치 줄:1 문자:1
+ .\.venv\Scripts\python.exe buggy_2.py 2>&1 | Tee-Object -FilePath evi ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (most recent call last)::St 
   ring) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
  File "C:\Users\psang\Documents\sales-debug-week4\.venv\Lib\site-packages\pandas\c
ore\indexes\base.py", line 3641, in get_loc
    return self._engine.get_loc(casted_key)
           ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "pandas/_libs/index.pyx", line 168, in pandas._libs.index.IndexEngine.get_lo
c
  File "pandas/_libs/index.pyx", line 197, in pandas._libs.index.IndexEngine.get_lo
c
  File "pandas/_libs/hashtable_class_helper.pxi", line 7668, in pandas._libs.hashta
ble.PyObjectHashTable.get_item
  File "pandas/_libs/hashtable_class_helper.pxi", line 7676, in pandas._libs.hashta
ble.PyObjectHashTable.get_item
KeyError: '단가'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\psang\Documents\sales-debug-week4\buggy_2.py", line 25, in <module
>
    result = summarize(df)
  File "C:\Users\psang\Documents\sales-debug-week4\buggy_2.py", line 20, in summari
ze
    df["매출액"] = df["단가"] * df["수량"]        # <-- 여기가 문제의 줄
                   ~~^^^^^^^^
  File "C:\Users\psang\Documents\sales-debug-week4\.venv\Lib\site-packages\pandas\c
ore\frame.py", line 4378, in __getitem__
    indexer = self.columns.get_loc(key)
  File "C:\Users\psang\Documents\sales-debug-week4\.venv\Lib\site-packages\pandas\c
ore\indexes\base.py", line 3648, in get_loc
    raise KeyError(key) from err
KeyError: '단가'
```

## ④ 내가 확인한 것

pd.read_csv로 데이터를 읽은 뒤 df.columns.tolist()와 첫 3행을 출력했습니다.

```text
실제 열 이름: ['date', 'product', 'category', 'price', 'quantity', 'stock']
      date product category price  quantity  stock
2026-01-29     텀블러       굿즈 15000         7  379.0
2026-03-04    크루아상     베이커리  3800        58   71.0
2026-01-27     에코백       굿즈 12000       174  379.0
```

실제 열 이름에는 price와 quantity가 있고 단가와 수량은 없습니다.
따라서 코드가 실제 데이터에 없는 열 이름을 사용한 것이 오류의 원인이라는 가설입니다.
현재 summarize 함수는 아직 수정하지 않았습니다.

## ⑤ 요청

무엇이·어디서·왜 형식으로 오류 원인을 설명하고,
열 이름 불일치라는 가설을 확인하는 검증 방법을 먼저 제안해주세요.
그 결과를 확인한 뒤 수정 코드를 진행하겠습니다.
수정 시 price의 문자열 형식과 결측치가 후속 계산에 영향을 주는지도 확인해주세요.
