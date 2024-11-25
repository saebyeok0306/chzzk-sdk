import json
from pprint import pprint

if __name__ == "__main__":
    t = json.loads(input("json 데이터 입력 : ").replace("\\", ""))
    pprint(t)