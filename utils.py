def validate_amount(amount_str):
    try:
        return float(amount_str)
    except ValueError:
        return None
