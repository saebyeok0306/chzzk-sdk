# 전방 참조 (Forward Reference)

전방 참조(forward reference)는 프로그램의 한 부분에서 아직 정의되지 않은 것을 참조해야 할 때 사용하는 개념입니다. Python에서는 주로 타입 힌트를 작성할 때 이 개념이 등장합니다.

## 전방 참조의 필요성

타입 힌트를 작성할 때, 어떤 클래스나 데이터 구조가 자기 자신이나 나중에 정의될 클래스를 참조해야 하는 경우가 종종 발생합니다. 하지만 Python은 코드를 위에서 아래로 실행하기 때문에, 참조 대상이 아직 정의되지 않았으면 NameError가 발생합니다.

```py
class Node:
    def __init__(self, value: int, next_node: Node):  # 여기서 Node는 아직 완전히 정의되지 않음
        self.value = value
        self.next_node = next_node
```

## 사용방법

Python 3.7부터 사용할 수 있으며, Python 3.11에서 기본 동작으로 설정되었습니다.

### 1. 문자열 사용

```py
class Node:
    def __init__(self, value: int, next_node: 'Node'):  # 문자열로 Node를 감싸기
        self.value = value
        self.next_node = next_node

```

전방 참조를 문자열로 감싸면 해결됩니다. 이 방식은 Python 3.7 이상에서 작동합니다. 그러나 문자열로 작성하면 IDE의 자동 완성 기능이 제한될 수 있습니다.

### 2. `from __future__ import annotations`

```py
from __future__ import annotations

class Node:
    def __init__(self, value: int, next_node: Node):  # Node를 그대로 사용 가능
        self.value = value
        self.next_node = next_node

```

이 문을 사용하면 전방 참조를 문자열로 감싸지 않아도 사용할 수 있습니다. 이 방식은 Python 3.7 이상에서 사용할 수 있으며, Python 3.11부터는 기본 동작이므로 더 이상 `__future__`를 임포트할 필요가 없습니다.