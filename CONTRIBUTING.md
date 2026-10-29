# Contributing to OCI Core

Thanks for your interest in Open Collective Intelligence (OCI).

## Current scope

OCI Core is an early local-first prototype. Contributions should keep the project small, understandable, and safe by default.

## Before opening a pull request

1. Explain the problem and proposed change.
2. Keep changes focused.
3. Add or update tests for behavior changes.
4. Run `python -m unittest discover -s tests -v`.
5. Update the README when commands or behavior change.
6. Never commit personal data, API keys, private datasets, or the local `oci.db`.

## Design principles

- Local-first by default.
- Explicit provenance for knowledge claims.
- Forecasts must be falsifiable and time-bounded.
- No automatic external actions.
- Security and privacy are requirements, not optional add-ons.

For security issues, follow [SECURITY.md](SECURITY.md). Do not publish sensitive exploit details in a public issue.
