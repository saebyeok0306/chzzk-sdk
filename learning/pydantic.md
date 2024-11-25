# pydantic BaseModel

## common config

BaseModel을 상속받는 Model을 하나 만들고, 해당 모델 안에 config를 넣어두고 이 모델을 상속시키게 하면 됩니다.

```py
class DefaultModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,  # 필드명을 camelCase로 자동 변환
        populate_by_name=True,
        frozen=True,  # 모델 인스턴스를 불변(immutable)으로 설정
        extra=Extra.allow  # forbid: 정의되지 않은 추가 필드를 허용하지 않음 allow: 추가 필드 허용
    )
```

## alias_generator에서 to_camel 사용시 생성자 명명 불일치

```py
class PersonalData(DefaultModel):
    private_user_block: bool
    following: Optional[Following] = None
```

예를 들어, 위와 같은 모델이 있을 때 `alias_generator`옵션이 `to_camel`로 되어있는 경우 json 역직렬화 과정에서 입력되는 값이 Camel 케이스일 때 Snake 케이스로 변환해줍니다.

이때, 필드 생성자도 Camel 케이스로 입력해야 하는 불편함이 있는데

```py
PersonalData(privateUserBlock=False, following=None)
```

카멜케이스로 넘어오는 데이터는 Snake로 변환하고, 직접 데이터를 생성할 땐 Snake 케이스로 입력받고 싶으면 `populate_by_name`를 `True`로 해주면 됩니다.
