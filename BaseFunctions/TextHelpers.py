import textwrap
# Read Python for the humanities


def wrap(x: str, width=40):
    return textwrap.wrap(x, width)


def short(x: str, width=15):
    return f"{x[0:width]}..."
