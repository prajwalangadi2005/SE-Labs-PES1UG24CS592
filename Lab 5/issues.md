# Issues Table — hotel_booking_system.py

Reports: `reports/before/` (original) and `reports/after/` (fixed).
Severity order: High → Medium → Low. "Commit" = which of the 3 commits fixed it.

| # | Issue | Type | Tool / Code | Line(s) | Description | Fix Approach | Commit |
|---|-------|------|-------------|---------|-------------|--------------|--------|
| 1 | `os.system` with string concatenation | Security (High) | Bandit B605 | 58 | `filename` is concatenated into a shell command → command injection possible. | Removed the shell call; use `print("Hotel ledger exported to:", filename)`. | 1 – Bandit |
| 2 | Weak MD5 hash | Security (High) | Bandit B324 | 47 | MD5 is broken and unsuitable for identifying guests/personal data. | Switched to `hashlib.sha256`. | 1 – Bandit |
| 3 | `eval()` on caller input | Security (Medium) | Bandit B307, Pylint W0123 | 42 | `compute_seasonal_rate` evaluated an arbitrary string → arbitrary code execution. | Replaced `rate_expr` string with a numeric `rate_multiplier`, validated (`float()`, must be > 0). `main` now calls it with `1.25`. | 1 – Bandit |
| 4 | Hardcoded secret | Security (Low) | Bandit B105 | 62 | Admin token committed in source and printed to console. | Read from env var `HOTEL_ADMIN_TOKEN`; only print whether it is configured. | 1 – Bandit |
| 5 | Weak PRNG for booking ref | Security (Low) | Bandit B311 | 51 | `random` is predictable; booking refs can be guessed. | Used `secrets.randbelow(9000) + 1000` (same 1000–9999 range). | 1 – Bandit |
| 6 | try / except / pass | Security + Bug (Low) | Bandit B110, Pylint W0702, Flake8 E722 | 25-27 | Bare `except` swallowed every error; cancelling an unknown room silently "succeeded". | Explicit `if room_num not in room_inventory: return False`; function now returns True/False. | 1 – Bandit |
| 7 | Mutable default argument | Bug | Pylint W0102 | 15 | `booking_log=[]` is shared across all calls. | Default `None`; falls back to a module-level `BOOKING_LOG`. | 2 – Pylint |
| 8 | Non-snake_case name | Style | Pylint C0103 | 15 | `bookRoom` violates PEP 8. | Renamed to `book_room` (caller in `main` updated). | 2 – Pylint |
| 9 | Missing docstrings (×7) | Documentation | Pylint C0116 | 15,23,30,40,46,50,54,61 | Functions had no docstrings. | Added one-line/short docstrings to every function. | 2 – Pylint |
| 10 | File not closed safely | Bug / Style | Pylint R1732, W1514 | 55-57 | `open()`/`close()` leaks the handle on error; no encoding. | `with open(filename, "w", encoding="utf-8") as ledger:`. | 2 – Pylint |
| 11 | Old-style `%` formatting | Style | Pylint C0209, Flake8 E501 | 19 | Should be an f-string; line was 80 chars. | Converted to f-string (also fixes E501). | 2 – Pylint |
| 12 | Redundant if/else | Refactor | Pylint R1703, R1705 | 34-37 | `if … return True else return False` | `return not room_inventory[room_num]["is_booked"]`. | 2 – Pylint |
| 13 | `main()` runs on import | Design | (found by reading) | 72 | Importing the module executed the demo and wrote a file. | Added `if __name__ == "__main__":` guard. | 2 – Pylint |
| 14 | Unused import `math` | Style | Flake8 F401, Pylint W0611 | 6 | Imported but never used. | Removed. | 3 – Flake8 |
| 15 | Unused variable `cleaning_deposit` | Style | Flake8 F841, Pylint W0612 | 31 | Assigned, never used. | Removed. | 3 – Flake8 |
| 16 | Comparison to `None` with `==` | Style | Flake8 E711, Pylint C0121 | 32 | Should use identity. | `is None`. | 3 – Flake8 |
| 17 | No newline at end of file | Style | Flake8 W292, Pylint C0304 | 72 | PEP 8 requires trailing newline. | Added. | 3 – Flake8 |

## Before / After summary

| Tool | Before | After |
|------|--------|-------|
| Pylint | **5.32 / 10** (23 messages) | **10.00 / 10** |
| Bandit | 6 issues (2 High, 1 Medium, 3 Low) | **0 issues** |
| Flake8 | 7 violations | **0 violations** |

## Bugs not flagged by a tool
- Items 6, 7, 10 and 13 were real logic bugs (silent failure, shared state, side effects on import), not just style.
- Output change to note: the guest hash is now SHA-256, so the value differs from the old MD5 output.
