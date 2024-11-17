def getAllStrings(alphabets: list, length: int) -> list[str]:
    if length < 0:
        raise Exception(f"Inside get_all_strings: variable length cannot be negative")
    if length == 0:
        return [""]
    strings = []
    for string in getAllStrings(alphabets, length - 1):
        for alphabet in alphabets:
            strings.append(string + alphabet)
    return strings