"""Lab 6 - Step 7: tests written to reach >= 90% BRANCH coverage
(every if/elif evaluated both True and False, plus boundary values)."""
import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# ---------- out_of_warranty_charge ----------
def test_within_warranty():
    assert out_of_warranty_charge("standard", 20, "defect", False) == 0


def test_unknown_plan_raises():
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("gold", 10, "defect", False)


def test_negative_age_raises():
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_zero_age_is_valid():
    # boundary: age_months == 0 is NOT < 0
    assert out_of_warranty_charge("basic", 0, "defect", False) == 0


@pytest.mark.parametrize("plan,expected_covered", [("basic", 12), ("standard", 24), ("premium", 36)])
def test_exact_boundary_is_free(plan, expected_covered):
    # excess == 0 -> returns 0 (excess <= 0 branch)
    assert out_of_warranty_charge(plan, expected_covered, "defect", False) == 0


def test_registered_extends_basic():
    # basic 12 + 6 = 18 covered; age 18 -> free
    assert out_of_warranty_charge("basic", 18, "defect", True) == 0
    # one month over -> charged at 100
    assert out_of_warranty_charge("basic", 19, "defect", True) == 100


def test_registered_extends_standard():
    assert out_of_warranty_charge("standard", 40, "defect", True) == 1000


def test_registered_premium_gets_no_extension():
    # registered but premium -> stays at 36; age 37 -> excess 1
    assert out_of_warranty_charge("premium", 37, "defect", True) == 100


def test_unregistered_gets_no_extension():
    assert out_of_warranty_charge("basic", 13, "defect", False) == 100


def test_defect_rate_small_excess():
    assert out_of_warranty_charge("basic", 17, "defect", False) == 5 * 100


def test_accidental_rate_small_excess():
    assert out_of_warranty_charge("basic", 17, "accidental", False) == 5 * 200


def test_excess_exactly_12_no_surcharge():
    # excess == 12 -> NOT > 12
    assert out_of_warranty_charge("basic", 24, "defect", False) == 12 * 100
    assert out_of_warranty_charge("basic", 24, "accidental", False) == 12 * 200


def test_defect_excess_over_12_surcharge():
    # excess 13, rate 100 + 50
    assert out_of_warranty_charge("basic", 25, "defect", False) == 13 * 150


def test_accidental_excess_over_12_surcharge():
    # excess 18, rate 200 + 50 + 25
    assert out_of_warranty_charge("basic", 30, "accidental", False) == 18 * 275


# ---------- claim_allowed ----------
def test_recall_within_limit():
    assert claim_allowed(5, 5, True) is True


def test_recall_over_limit():
    assert claim_allowed(60, 6, True) is False


def test_recall_ignores_cooldown():
    assert claim_allowed(0, 1, True) is True


def test_too_soon_after_last_claim():
    assert claim_allowed(29, 1, False) is False


def test_exactly_30_days_allowed():
    assert claim_allowed(30, 1, False) is True


def test_claim_allowed():
    assert claim_allowed(60, 1, False) is True


def test_normal_claim_at_limit():
    assert claim_allowed(60, 2, False) is True


def test_normal_claim_over_limit():
    assert claim_allowed(60, 3, False) is False


# ---------- sla_status ----------
@pytest.mark.parametrize(
    "hours,hardware,priority,expected",
    [
        # software, non-priority: cutoff 24
        (24, False, False, "on_track"),
        (23, False, False, "at_risk"),
        (12, False, False, "at_risk"),
        (11, False, False, "critical"),
        # hardware, non-priority: cutoff 48
        (48, True, False, "on_track"),
        (36, True, False, "at_risk"),
        (35, True, False, "critical"),
        # software, priority: cutoff 48
        (48, False, True, "on_track"),
        (36, False, True, "at_risk"),
        (0, False, True, "critical"),
        # hardware, priority: cutoff 72
        (72, True, True, "on_track"),
        (60, True, True, "at_risk"),
        (59, True, True, "critical"),
    ],
)
def test_sla_status(hours, hardware, priority, expected):
    assert sla_status(hours, hardware, priority) == expected
