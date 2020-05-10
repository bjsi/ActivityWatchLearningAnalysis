import html
from BaseFunctions.TextHelpers import wrap
from BaseFunctions.QueryHelpers import apply


def remove_references(x: str):
    idx = x.find("#SuperMemo Reference")
    if idx > -1:
        x = x[:idx]
    return x


def fmt_el_content(content: str):
    return apply([
        remove_references,
        wrap,
        "\n".join,
        html.unescape
    ], content)

