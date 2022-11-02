import re
PASCAL_RE = re.compile(r"([^\-_]+)")

def lowerCase(string: str) -> str:
        return str(string).lower()

def upperCase(string: str) -> str:
    return str(string).upper()    
        
def camelCase(string: str) -> str:
    def _replace_fn(match):
        return match.group(1)[0].upper() + match.group(1)[1:]

    string = PASCAL_RE.sub(_replace_fn, string)
    if not string:
        return string
    return lowerCase(string[0]) + re.sub(r"[\-_\.\s]([a-z])", lambda matched: upperCase(matched.group(1)), string[1:])

def pascalCase(string: str) -> str:
    if string.isupper() or string.isnumeric():
        return string

    def _replace_fn(match):
        """
        :rtype: str
        """
        return match.group(1)[0].upper() + match.group(1)[1:]

    s = camelCase(PASCAL_RE.sub(_replace_fn, string))
    return s[0].upper() + s[1:] if len(s) != 0 else s
