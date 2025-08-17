# convert price string to float
def convert_price_to_float(price_str: str) -> float | None:
    if not price_str:
        return None
    cleaned = (
        price_str.replace("€", "")
        .replace(".", "")       # remove thousands separator
        .replace(",", ".")      # replace comma with decimal
        .strip()
    )
    try:
        return float(cleaned)
    except ValueError:
        return None
