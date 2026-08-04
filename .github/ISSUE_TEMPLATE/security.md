---
name: Security issue
about: Please do not file security issues here.
title: "Do not file security issues on GitHub — see instructions below"
labels: []
assignees: []
---

# Please do not report security issues through public GitHub issues.

PAL Pod is a $95k box that sits in someone's home. Public disclosure of a
security vulnerability without a fix in hand puts real customers at real risk.
We take coordinated disclosure seriously, and so should you.

## How to report a vulnerability

Email **security@palpod.com** with:

- A description of the vulnerability.
- Steps to reproduce (or a proof-of-concept).
- The version of PALPod OS you observed it on
  (`git -C /opt/palpod-os describe --tags --always --dirty`).
- Your name / handle for the SECURITY.md hall of thanks, or a note that you
  want to remain anonymous.

The full disclosure policy — response times, safe-harbor language, scope, and
the PGP key for encrypted reports — lives in
[SECURITY.md](../SECURITY.md).

## What is in scope

- `pal-web` (the FastAPI control app and its endpoints).
- `pal-voice` (the wake-word / STT / LLM / TTS orchestrator).
- The install / update scripts and systemd units in this repo.

## What is out of scope

- Attacks that require physical access to the Pod or the same LAN as the Pod
  are **explicitly out of scope**. The whole product thesis is
  "nothing leaves the house" — every capability listens on the LAN, and a
  LAN-adjacent attacker is inside the trust boundary by design. If you find
  a bug that only fires under LAN-local access with physical proximity, it
  is a bug (file it as a normal issue) but it is not a vulnerability.

Please close this template without submitting and email us instead.
