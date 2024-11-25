# TypedDict

`TypedDict`는 Python에서 사전(dictionary) 구조의 타입을 명확히 정의할 수 있게 해주는 기능입니다. 예를 들어, 특정 키와 값의 타입이 정해져 있는 사전 구조를 정의할 수 있습니다.

```py
from typing import TypedDict

class Person(TypedDict):
    name: str  # 필수 키
    age: int   # 필수 키
```

위의 Person 정의는 다음과 같은 데이터를 나타냅니다.

```py
person: Person = {"name": "Alice", "age": 30}  # 유효
person = {"name": "Alice"}  # 오류: 'age'가 누락됨
```

## 선택적 키 (Optional Keys)

`TypedDict`에서 선택적 키를 정의하려면 `total=False`를 사용할 수 있습니다.

```py
class PartialPerson(TypedDict, total=False):
    name: str  # 선택적 키
    age: int   # 선택적 키
```

그러나 `total=False`는 모든 키를 선택적으로 만듭니다. 만약 일부 키만 선택적으로 만들고 싶다면, Python 3.11부터 추가된 `NotRequired`를 사용합니다.

## `NotRequired`

`NotRequired`를 사용하면 일부 키는 필수로, 일부 키는 선택적으로 설정할 수 있습니다.

```py
from typing import TypedDict
from typing_extensions import NotRequired

class Person(TypedDict):
    name: str  # 필수 키
    age: NotRequired[int]  # 선택적 키
```

이 경우, `name`은 반드시 포함해야 하지만 `age`는 선택 사항입니다.

> `NotRequired` vs `Optional`<br/>
NotRequired와 Optional은 비슷해 보이지만, 사용하는 목적이 다릅니다.<br/><br/>
Optional은 값이 None일 수 있음을 나타냅니다.
NotRequired는 해당 키 자체가 사전에 존재하지 않아도 유효하다는 것을 의미합니다.

> **왜 typing_extensions인가?**<br/><br/>
**NotRequired**는 Python 3.11에서 처음 추가되었습니다.<br/>
이전 버전(Python 3.8~3.10)과 호환되도록 하기 위해 typing_extensions 패키지에서 제공됩니다.<br/>
Python 3.11 이상을 사용할 경우 from typing import NotRequired로 직접 가져올 수 있습니다.