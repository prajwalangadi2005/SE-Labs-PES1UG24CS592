"""Lab 6 - Step 5: tests written to reach >= 90% LINE (statement) coverage."""
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


def test_registered_extension_applied():
    # standard 24 + 6 = 30 covered, age 40 -> excess 10, rate 100
    assert out_of_warranty_charge("standard", 40, "defect", True) == 1000


def test_accidental_within_12_months_excess():
    # basic 12 covered, age 17 -> excess 5, rate 200
    assert out_of_warranty_charge("basic", 17, "accidental", False) == 1000


def test_accidental_excess_over_12():
    # excess 18, rate 200 + 50 + 25 = 275
    assert out_of_warranty_charge("basic", 30, "accidental", False) == 18 * 275


# ---------- claim_allowed ----------
def test_claim_allowed():
    assert claim_allowed(60, 1, False) is True


def test_recall_claim():
    assert claim_allowed(5, 3, True) is True


def test_claim_too_soon():
    assert claim_allowed(10, 1, False) is False


# ---------- sla_status ----------
def test_sla_on_track_hardware_priority():
    assert sla_status(100, True, True) == "on_track"


def test_sla_at_risk():
    assert sla_status(60, True, True) == "at_risk"


def test_sla_critical_software():
    assert sla_status(5, False, False) == "critical"
