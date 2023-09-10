def strToFloat(value: str) -> float:
    return float(value.replace('.', '').replace(',', '.'))


def strToInt(value: str) -> int:
    return int(value.replace('.', ''))
