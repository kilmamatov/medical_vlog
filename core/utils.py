import string

ru_to_eng = {
    "a": "a",
    "6": "b",
    "в": "v",
    "r": "g",
    "д": "d",
    "e": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": None,
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "o": "o",
    "п": "p",
    "p": "r",
    "c": "s",
    "т": "t",
    "y": "u",
    "ф": "f",
    "x": "h",
    "ц": "c",
    "ч": "ch",
    "ш": "sh",
    "щ": "sh",
    "ъ": None,
    "ы": None,
    "ь": None,
    "э": None,
    "ю": None,
    "я": "ya",
    "ѐ": "e",
}


def translate_word(title: str):
    new_title = ""
    transformation_title = title.lower().replace(" ", "")
    for char in transformation_title:
        if char in "1234567890" or char in string.ascii_lowercase:
            new_title += "".join(char)
        elif ru_to_eng[char]:
            new_title += "".join(ru_to_eng[char])
        else:
            continue
    return new_title
