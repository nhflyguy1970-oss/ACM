# Release Process

1. Milestone complete: tests green, docs updated, DECISION_LOG entries for deviations.
2. Bump version in `pyproject.toml` and `acm/__init__.py`.
3. Update `CHANGELOG.md`.
4. Tag `vX.Y.Z` on the release commit.
5. Publish package when distribution channel is ready (not required for Foundation Build).

## Versioning

Semantic versioning. Pre-1.0: minor bumps may include breaking cognitive API changes if documented; prefer additive public API.
