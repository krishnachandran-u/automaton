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

def _getNextLetter(char: str) -> str:
    if char == 'Z':
        return 'A'
    if char == 'z':
        return 'a'
    if char == '9':
        return '0'
    return chr(ord(char) + 1)

def randomDarkColor() -> str:
    from random import randint
    r = randint(50, 150)
    g = randint(50, 150)
    b = randint(50, 150)
    return f'#{r:02x}{g:02x}{b:02x}'  