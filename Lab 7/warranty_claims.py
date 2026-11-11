import math


def parse_claim(text):
    """Parse 'plan:months' (e.g. 'standard:30').

    Returns (Plan Name, months as float), or None if the input is invalid.
    """
    if not isinstance(text, str):
        return None

    parts = text.split(':')
    if len(parts) != 2:            # no colon, or more than one colon
        return None

    plan = parts[0].strip()
    if not plan:                   # empty plan name
        return None

    try:
        months = float(parts[1])
    except (ValueError, OverflowError):
        return None

    if not math.isfinite(months) or months < 0:   # reject nan, inf, negatives
        return None

    return plan.title(), months


def age_average(ages_csv):
    """Average of comma-separated product ages (e.g. '12,24,36').

    Returns the average as a float, or None if the input is invalid.
    """
    if not isinstance(ages_csv, str):
        return None

    items = ages_csv.split(',')
    values = []
    for item in items:
        try:
            age = int(item.strip())
        except (ValueError, OverflowError):   # '', 'abc', '1.5', huge numbers
            return None
        if age < 0:                           # an age cannot be negative
            return None
        values.append(age)

    if not values:
        return None

    return round(sum(values) / len(values), 2)   # true average, not floor division


def payable_charge(text):
    """Compute charge * 1.18 (18% tax) - discount from 'charge|discount'.

    Returns the payable amount (never below 0), or None if the input is invalid.
    """
    if not isinstance(text, str):
        return None

    parts = text.split('|')
    if len(parts) != 2:
        return None

    try:
        charge = float(parts[0])
        discount = float(parts[1])
    except (ValueError, OverflowError):
        return None

    if not (math.isfinite(charge) and math.isfinite(discount)):
        return None
    if charge < 0 or discount < 0:
        return None

    total = charge * 1.18 - discount
    if not math.isfinite(total):               # overflow on very large charges
        return None

    return round(max(total, 0), 2)


def main():
    print("==== Running parse_claim ====")
    user_input = input("Enter plan:age in months (e.g. standard:30): ")
    result = parse_claim(user_input)
    print("Plan and Age:", result if result is not None else "Invalid input")

    print("\n==== Running age_average ====")
    user_input = input("Enter product ages as CSV (e.g. 12,24,36): ")
    result = age_average(user_input)
    print("Average Age:", result if result is not None else "Invalid input")

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 1500|200): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()