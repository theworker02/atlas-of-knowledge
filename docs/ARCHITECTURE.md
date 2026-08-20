# Architecture

Atlas is intentionally modular and standard-library based:

| Component | Responsibility |
| --- | --- |
| `atlas.policy` | allowlist and license compatibility decisions |
| `atlas.discovery` | declared catalog parsing, discipline classification, scoring |
| `atlas.registry` | SQLite state for course decisions, provenance, incremental fingerprints, and record reports |
| `atlas.quality` | duplicate fingerprints and machine-readable quality reports |
| `scripts.validate_dataset` | record contract and prerequisite graph validation |
| `atlas.build` | deterministic split, subset, graph, and metadata generation |
| `atlas.pipeline` | explicit orchestration only; domain logic stays in modules |

No component crawls the web or accepts arbitrary URLs. Production source adapters should expose a small catalog-feed interface, validate policy before fetching licensed material, persist only required provenance, and provide original record candidates to the quality stage. An external generative model, when used, belongs behind a credentialed adapter and must not be allowed to bypass policy or auto-release its output.
