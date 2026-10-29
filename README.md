# OCI Core

**A lightweight, decentralized knowledge and forecasting platform for collaborative intelligence.**

OCI (Open Collective Intelligence) explores how people and AI agents can contribute verifiable knowledge, compare hypotheses, and evaluate forecasts while keeping control of their own data.

> **Status:** Early local-first prototype. This repository is not yet a decentralized P2P network and is not production-ready.

## Current features

- Local SQLite knowledge ledger with sources and confidence values.
- Forecast registry with target dates, assumptions, and probabilities.
- Binary outcome recording and Brier-score calculation.
- Command-line interface and unit tests.
- Python standard library only; no API keys or cloud services required.
- GitHub Actions test workflow.

## Quick start

Requires Python 3.10 or newer.

```bash
git clone https://github.com/PabloEmilioEscobarGaviria1/oci-core.git
cd oci-core
python oci.py init
python -m unittest discover -s tests -v
```

Add and list a knowledge item:

```bash
python oci.py add --claim "Electricity demand may rise" --source "https://example.org/source" --kind hypothesis --confidence 0.55
python oci.py list
```

Record a forecast and score it after the outcome is known:

```bash
python oci.py forecast --question "Will the specified event happen by 2030-01-01?" --probability 0.35 --target-date 2030-01-01 --assumptions "Illustrative estimate"
python oci.py forecasts
python oci.py score --id 1 --outcome 1
```

The database is created locally as `oci.db`. Keep it private if it contains non-public information.

## Principles

- **Voluntary participation:** no contribution is required.
- **Local-first privacy:** data stays local unless explicitly exported.
- **Provenance:** claims should reference sources and preserve assumptions.
- **Falsifiable forecasts:** define probabilities and target dates before outcomes are known.
- **Human approval:** the prototype records information and does not take external actions.
- **Small modules:** networking should be added only after permissions and threat models are defined.

## Roadmap

- [x] Local knowledge ledger
- [x] Forecast registry
- [x] Binary outcome scoring
- [x] Unit tests and CI
- [ ] Signed knowledge objects
- [ ] Peer-to-peer transport and discovery
- [ ] Permissioned replication
- [ ] Provenance graph and contradiction tracking
- [ ] Forecast calibration and historical evaluation
- [ ] Optional local LLM adapter
- [ ] Federated learning as a separate, opt-in subsystem

Networking, encryption, identity, trust scoring, and federated learning are future work.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).
