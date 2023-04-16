import re

PASCAL_RE = re.compile(r"([^\-_]+)")


def lower_case(string: str) -> str:
    return str(string).lower()


def upper_case(string: str) -> str:
    return str(string).upper()


def camel_case(string: str) -> str:
    def _replace_fn(match):
        return match.group(1)[0].upper() + match.group(1)[1:]

    string = PASCAL_RE.sub(_replace_fn, string)
    if not string:
        return string
    return lower_case(string[0]) + re.sub(
        r"[\-_\.\s]([a-z])", lambda matched: upper_case(matched.group(1)), string[1:]
    )


def pascal_case(string: str) -> str:
    if string.isupper() or string.isnumeric():
        return string

    def _replace_fn(match):
        """
        :rtype: str
        """
        return match.group(1)[0].upper() + match.group(1)[1:]

    s = camel_case(PASCAL_RE.sub(_replace_fn, string))
    return s[0].upper() + s[1:] if len(s) != 0 else s
