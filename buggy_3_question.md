# buggy_3.py 구조화된 질문

## ① 맥락
CSV를 읽고 가격을 정제한 뒤 카테고리별 매출을 집계하려는 코드입니다.

## ② 코드
```python
def load_and_clean(path):
    df = pd.read_csv(path, encoding="utf-8")
    # price 컬럼을 숫자로 정제
    df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["revenue"] = df["price"] * df["quantity"]
```

호출 직후 오류가 발생한 줄은 다음과 같습니다.
```python
df = load_and_clean("dirty_sales.csv")
result = df.groupby("category")["revenue"].sum()
```

## ③ Traceback
원본 실행 오류 로그 전문입니다. PowerShell의 추가 표시를 포함합니다.
```text
.\.venv\Scripts\python.exe : Traceback (most recent call las
t):
위치 줄:1 문자:1
+ .\.venv\Scripts\python.exe buggy_3.py 2>&1 | Tee-Object -F
ilePath evi ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Traceback (mos 
   t recent call last)::String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
  File "C:\Users\psang\Documents\sales-debug-week4\buggy_3.p
y", line 32, in <module>
    main()
    ~~~~^^
  File "C:\Users\psang\Documents\sales-debug-week4\buggy_3.p
y", line 28, in main
    result = df.groupby("category")["revenue"].sum()   # <--
 여기서 죽는다
             ^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'groupby'
```

## ④ 내가 확인한 것
함수를 직접 호출하고 반환값과 자료형을 출력했습니다.
```text
반환값: None
반환값 자료형: <class 'NoneType'>
```
함수 내부에서는 DataFrame을 만들었지만 반환값은 None입니다.
함수 끝에 return df가 없어서 None이 전달된 것이라는 가설입니다.

## ⑤ 요청
무엇이·어디서·왜 형식으로 설명하고, 반환값을 만든 함수를 역추적해
원인을 확인해주세요. 정제한 DataFrame을 반환하도록 수정하고,
정상 데이터에서도 반환 자료형과 계산 결과가 올바른지 검증해주세요.
