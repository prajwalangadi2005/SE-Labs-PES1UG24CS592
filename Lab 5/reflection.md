# Reflection

> Your handout PDF does not print the four reflection questions, so these are the standard Lab 5 questions. If your instructor's wording differs, keep the answers and just change the headings.

**1. Which issues were the easiest and hardest to fix?**
Easiest: Flake8 items (unused import/variable, `is None`, trailing newline) and Pylint docstrings — mechanical, no behaviour change. Hardest: `eval()` in `compute_seasonal_rate`. A tool can only say "don't use eval"; I had to redesign the API (string expression → numeric multiplier with validation) and update the caller, deciding what the function should accept.

**2. Did the tools report any false positives?**
Mostly no, but some findings need judgement. Bandit B105 flagged the "password" because of the variable name/string; it was a genuine hardcoded secret here, but in general such hits can be test data. B311 (`random`) is only a real problem if the booking reference is meant to be unguessable; I switched to `secrets` since references identify bookings. Pylint's "unused variable" on `base_price` was a side-effect of `eval` (it was used inside the string), i.e. the tool misread it — it disappeared once `eval` was removed.

**3. How would you integrate static analysis into your workflow?**
Run Flake8 and Pylint in a pre-commit hook and in CI (e.g. GitHub Actions) on every pull request, with Bandit as a required security gate that fails on Medium/High findings. Set a minimum Pylint score (e.g. 9.0), store tool config in `setup.cfg`/`pyproject.toml`, and use `# nosec` / `# pylint: disable` sparingly with a written justification.

**4. What tangible improvements did you see?**
Pylint went from 5.32 to 10.00, Bandit from 6 issues (2 High) to 0, Flake8 from 7 violations to 0. Beyond scores: the code no longer allows command injection or code execution, no secret lives in source, the shared mutable log bug is gone, failed cancellations are now reported instead of hidden, and importing the module no longer runs the program. It is also easier to read and to unit-test.
