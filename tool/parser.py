import re


def split_tag(tags: list[str]) -> list[str]:
    result = []
    for tag in tags:
        if "#" not in tag[1:]:
            result.append(tag)
        else:
            result.extend(map(lambda x: "#" + x, tag[1:].split("#")))
    return result


def get_category(tags: list[str]) -> list[str]:
    tags = str(tags)
    category = []
    if "카페" in tags:
        category.append("카페")
    elif "술집" in tags:
        category.append("술집")
    elif "맛집" in tags:
        category.append("맛집")

    meat = ["고기", "삼겹살", "한우", "소고기", "구이"]
    if [1 for x in meat if x in tags]:
        category.append("고깃집")

    if "빵집" in tags or "베이글" in tags:
        category.append("베이커리")

    return category


def parse_daejeon_people(text, is_video: bool):
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

    # 가공
    info_tmp = info_match.group(1).split("＊") if info_match else None
    tags = split_tag(tags_matches)

    # 딕셔너리 형태로 저장
    result = {
        "name": name_match.group(1) if name_match else None,
        "location": info_tmp[0] if info_tmp else None,
        "time": info_tmp[1] if info_tmp else None,
        "tags": tags,
        "description": description_match.group(1).strip() if description_match else None,
        "category": get_category(tags),
        "isVideo": is_video
    }
    return result


def parse_matdongyeop(text, is_video):
    # 정규식 패턴 설정
    description_pattern = re.compile(r'.+?(?=▪️)', re.DOTALL)
    name_pattern = re.compile(r"📌\S+")
    info_pattern = re.compile(r'(▪️.*?)(?=#)', re.DOTALL)
    tags_pattern = re.compile(r"#\S+")

    # 각 부분 추출
    description_match = description_pattern.search(text).group()
    name_match = name_pattern.search(text).group()
    info_match = info_pattern.search(text)
    tags_matches = tags_pattern.findall(text)

    # 가공
    tags = split_tag(tags_matches)
    info_tmp = info_match.group().split("▪️") if info_match else None
    location = info_tmp[1] if info_tmp else None
    try:
        if "휴무" in info_tmp[3]:
            time_match = info_tmp[2] + " / " + info_tmp[3]
        else:
            time_match = info_tmp[2]
    except IndexError:
        time_match = None
    except TypeError:
        time_match = None

    description = description_match.replace(name_match, "")

    if "여기는" in name_match:
        name_match = name_match.replace("여기는", "")
    elif "에서" in name_match:
        name_match = name_match.replace("에서", "")

    # 딕셔너리 형태로 저장
    result = {
        "name": name_match[1:] if name_match else None,
        "location": location if location else None,
        "time": time_match if time_match else None,
        "tags": tags,
        "description": description,
        "category": get_category(tags),
        "isVideo": is_video
    }
    return result
