def get_category(tags: list[str]) -> list[str]:
    tags = str(tags)
    category = []
    if "카페" in tags:
        category.append("카페")
    elif "술집" in tags:
        category.append("술집")
    elif "맛집" in tags:
        category.append("맛집")
    return category


def split_tag(tags: list[str]) -> list[str]:
    result = []
    for tag in tags:
        if "#" not in tag[1:]:
            result.append(tag)
        else:
            result.extend(map(lambda x: "#" + x, tag[1:].split("#")))
    return result

