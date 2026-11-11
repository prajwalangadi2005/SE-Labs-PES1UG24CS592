import math

from hypothesis import given, strategies as st
from warranty_claims import parse_claim, age_average, payable_charge

# Anything a caller could plausibly (or implausibly) pass in
anything = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.binary(),
    st.lists(st.integers()),
)


# ---------- 1. "Must never crash" tests ----------

@given(anything)
def test_parse_claim_no_crash(s):
    try:
        parse_claim(s)
    except Exception as e:
        assert False, f"parse_claim crashed with: {e!r}"


@given(anything)
def test_age_average_no_crash(s):
    try:
        age_average(s)
    except Exception as e:
        assert False, f"age_average crashed with: {e!r}"


@given(anything)
def test_payable_charge_no_crash(s):
    try:
        payable_charge(s)
    except Exception as e:
        assert False, f"payable_charge crashed with: {e!r}"


# ---------- 2. Property tests on valid input ----------

@given(st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1),
       st.integers(min_value=0, max_value=10_000))
def test_parse_claim_valid(plan, months):
    result = parse_claim(f"{plan}:{months}")
    assert result is not None
    assert result[0] == plan.strip().title()
    assert result[1] == float(months)


@given(st.lists(st.integers(min_value=0, max_value=1000), min_size=1))
def test_age_average_valid(ages):
    result = age_average(",".join(map(str, ages)))
    assert result is not None
    # the average must lie between the smallest and largest age
    assert min(ages) - 0.01 <= result <= max(ages) + 0.01


@given(st.floats(min_value=0, max_value=1e6),
       st.floats(min_value=0, max_value=1e6))
def test_payable_charge_valid(charge, discount):
    result = payable_charge(f"{charge}|{discount}")
    assert result is not None
    assert math.isfinite(result)
    assert result >= 0            # payable amount can never be negative


# ---------- 3. Specific edge cases found by fuzzing ----------

def test_known_bad_inputs_return_none():
    assert parse_claim("standard") is None        # no colon
    assert parse_claim("a:b:c") is None           # too many colons
    assert parse_claim("gold:abc") is None        # non-numeric months
    assert parse_claim("gold:nan") is None        # NaN
    assert parse_claim("gold:-5") is None         # negative months
    assert parse_claim(None) is None
    assert age_average("") is None                # empty string
    assert age_average("1,,3") is None            # empty element
    assert age_average("12,abc") is None
    assert age_average("-4,10") is None
    assert age_average(None) is None
    assert payable_charge("1500") is None         # missing discount
    assert payable_charge("a|b") is None
    assert payable_charge("inf|0") is None
    assert payable_charge("-100|0") is None
    assert payable_charge(None) is None


def test_known_good_inputs():
    assert parse_claim(" standard :30") == ("Standard", 30.0)
    assert age_average("12,24,37") == 24.33      # no floor-division truncation
    assert payable_charge("1500|200") == 1570.0
    assert payable_charge("10|500") == 0         # discount larger than charge