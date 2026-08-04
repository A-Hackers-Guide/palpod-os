# Contributing to PALPod OS

Thanks for wanting to help. This repository is the base operating layer for a
$95k, fully-offline luxury home AI and media server. That framing shapes
everything below — some rules that would be strange on a normal open-source
project (no cloud calls, no telemetry, no subscription hooks) are hard product
constraints here. Please read `ATLAS.md` before you start.

---

## Table of contents

- [Development environment](#development-environment)
- [Code style](#code-style)
- [Commit conventions](#commit-conventions)
- [Pull request process](#pull-request-process)
- [Adding a new KiCad board](#adding-a-new-kicad-board)
- [Non-negotiable boundaries](#non-negotiable-boundaries)

---

## Development environment

You do not need a Jetson to hack on most of this repo. Any Linux or macOS box
with Docker and Python 3.11+ is enough for the software side.

### Bring up the shared services

```bash
# The full compose stack is heavy; you usually only need Postgres for tests.
docker compose up -d postgres
```

Integration tests that touch a real Postgres use
[testcontainers](https://testcontainers-python.readthedocs.io/) and start their
own disposable `postgres:16` container. You do not need to keep a database
running for them; you just need a Docker-compatible runtime on your PATH.
Tests marked `@pytest.mark.integration` auto-skip when Docker is not
available.

### Set up a component

Each of the three Python components is an independent package.

```bash
cd pal-web            # or pal-voice, or pal-face
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

### Run the whole thing (Jetson-shaped)

The full stack is intended to be brought up by `./install.sh` on a Jetson
AGX Orin running Ubuntu 22.04 aarch64. On a laptop, most services will pull
and start, but anything GPU-accelerated (Sunshine, hardware transcoding) will
not work.

---

## Code style

- **Python: `ruff` for lint, `black` for formatting, `isort` for imports.**
  Configuration lives in each component's `pyproject.toml`. Run
  `ruff check .`, `black .`, and `isort .` before you push. CI enforces
  `ruff check`.
- **Shell scripts: `shellcheck`-clean.** Prefer `#!/usr/bin/env bash` with
  `set -euo pipefail`.
- **YAML: `yamllint`-clean.** Two-space indentation, no trailing whitespace,
  document-start marker (`---`) on standalone files.
- **Markdown: `markdownlint-cli2`-clean.** Configuration in `.markdownlint.jsonc`
  (add one if you need to relax a rule; do not disable rules per-file).
- **KiCad: match the vocabulary in `hardware/electrical/kicad/palpod-mic-array/`.**
  That board is the reference design; its custom symbol library, stackup file,
  and net-class conventions carry over to every other board.

---

## Commit conventions

We use [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<optional scope>): <subject>

<optional body>

<optional footer>
```

Types we use:

- `feat` — a new user-facing capability.
- `fix` — a bug fix.
- `docs` — documentation only.
- `chore` — build tooling, CI, dependency bumps, cleanup with no behavior
  change.
- `test` — tests only, no production code change.
- `refactor` — code change that neither adds a feature nor fixes a bug.

Optional scopes: `pal-web`, `pal-voice`, `pal-face`, `hardware`,
`compose`, `install`, `docs`, `ci`. Example:

```text
feat(pal-web): add remote-devices settings page

Renders the paired-devices list from `remote_sessions` and exposes the
"Allow AI control" toggle. Enforces the X-Consent-Origin check on the
POST path.

Closes #142
```

---

## Pull request process

1. Fork the repo (or push a branch, if you have push access).
2. Open a PR against `main` using the pull request template.
3. CI must be green — lint, tests, `docker compose config`, and KiCad
   syntax parse.
4. At least one reviewer must approve. Security-sensitive PRs
   (anything under `pal-web/palweb/routers/`, anything touching
   `configs/rustdesk/`, anything touching auth) require two reviewers.
5. We **squash-merge**. The squash-merge commit message should be a valid
   Conventional Commit.
6. Delete the branch after merge.

Draft PRs are welcome for early feedback; mark them draft explicitly.

---

## Adding a new KiCad board

The `hardware/electrical/kicad/palpod-mic-array/` project is the reference for
"what a well-formed board in this repo looks like." When you add a new one:

1. Create `hardware/electrical/kicad/<board-name>/`.
2. Include, at minimum:
   - `<board-name>.kicad_pro` (project settings)
   - `<board-name>.kicad_sch` (schematic — populated, not empty)
   - `<board-name>.kicad_pcb` (board outline, stackup, net classes — routing
     optional, but the file must parse)
   - A custom symbol library if you introduce new parts.
   - A `stackup.md` or similar note describing layer count and impedance
     targets.
3. Add the board to the matrix in
   `.github/workflows/kicad-render.yml` so CI renders schematic PDF and 3D
   preview on every push.
4. Update `hardware/README.md` and `hardware/electrical/block-diagrams/` so
   the new board appears in the top-down view.

CI runs `sexpdata.load` on every `.kicad_sch` and `.kicad_pcb` file in the
tree — if your board does not parse, CI fails.

---

## Non-negotiable boundaries

Copied verbatim from [`ATLAS.md`](ATLAS.md) §6. These are not preferences.
They are the product. A PR that violates one of these will be rewritten in
review.

- **No AI-initiated remote input without explicit user-tap consent.** The
  remote-desktop endpoints (landing in `pal-web/palweb/routers/remote.py`)
  check an `X-Consent-Origin` header. Any code path that skips or fakes that
  check is a safety bug. The AI can propose an action; the human's actual
  finger on an actual screen approves it. This is the safety property that
  lets a $95k box sit in a customer's home and do real things without
  anyone getting sued.
- **No cloud dependencies added anywhere.** No AWS SDK. No third-party
  analytics. No "helpful" webhook to a status server. No telemetry. No
  update server we host. If a service can't run entirely offline on the
  customer's own hardware, it can't run at all. This is why we are $95k and
  not $9,500 with a subscription.
- **The sphere shows only its face.** Never any UI. Never any game content.
  Never a remote-desktop stream. Never a notification. The face is the
  face. Streams and UI go to TVs and extenders. This is a hard product
  rule. Break it and the product stops being the product.
- **No new subscription revenue models.** The buyer paid $95k. Everything
  they need is included, forever, on their hardware. No SaaS layer, no
  premium tier, no cloud storage upsell, no "PAL Premium." If a Series A
  investor pushes for one, the answer is no. The whole thesis is that we
  sell one thing at a high price and never come back for more.

---

By contributing you agree that your contribution is licensed under Apache 2.0,
matching the rest of the repository (see [LICENSE](LICENSE)), and that you
have read and will follow the [Code of Conduct](CODE_OF_CONDUCT.md).
