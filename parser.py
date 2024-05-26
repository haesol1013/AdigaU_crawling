import re


def parse_text(text):
    # 정규식 패턴 설정
    description_pattern = re.compile(r"^(.*?)(?=◈#)", re.DOTALL)
    name_pattern = re.compile(r"◈#(.*?)◈")
    info_pattern = re.compile(r"＊(.*?)#")
    tags_pattern = re.compile(r"#\S+")

    # 각 부분 추출
    description_match = description_pattern.search(text)
    name_match = name_pattern.search(text)
    info_match = info_pattern.search(text)
    tags_matches = tags_pattern.findall(text)[1:]

    info_tmp = info_match.group(1).split("＊") if info_match else None

    # 딕셔너리 형태로 저장
    result = {
        "name": name_match.group(1) if name_match else None,
        "location": info_tmp[0] if info_tmp else None,
        "time": info_tmp[1] if info_tmp else None,
        "tags": tags_matches,
        "description": description_match.group(1).strip() if description_match else None
    }

    return result

