import textwrap

def clean_docstring(string:str) -> str:
    if not string:
        return ""
    return textwrap.dedent(string).strip()