import re


def get_result(result: str) -> str:
    result = re.sub("[rR]esult(.*):", "", result).strip()
    if "=" in result:
        parts = result.split("=")
        return parts[0]
    return result


def get_qty(result: str) -> int:
    qty = 1
    if "=" in result:
        parts = result.split("=")
        return int(parts[1])
    return qty


class Recipe:
    payload = list[str]
    result = str
    base = str
    qty = int

    def __init__(self, name, payload, base, file):
        self.name = name
        self.payload = payload
        self.base = base
        self.file = file
        self.parse_result()

    def parse_result(self):
        result = list(filter(lambda r: r.strip().startswith("Result"), self.payload))
        if result is not None and len(result) > 0:
            clean_result = " ".join(result[0].split()).replace(",", "")
            self.result = get_result(clean_result)
            self.qty = get_qty(clean_result)
        return None
