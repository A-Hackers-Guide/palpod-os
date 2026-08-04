<!-- Thanks for the PR. Fill in the sections that apply and delete the rest. -->

## Summary

<!-- One or two sentences: what does this change do? -->

## Motivation

<!--
Why is this change needed? Link the issue, the design doc, the customer report,
or the reason the founder asked for it. If it addresses one of the non-negotiable
boundaries in `ATLAS.md` §6, say so.
-->

Closes #

## Changes

<!--
Bullet the concrete changes. If this touches more than one component
(pal-web, pal-voice, pal-face, hardware, ops), call each one out.
-->

- [ ] pal-web
- [ ] pal-voice
- [ ] pal-face
- [ ] hardware/ (mechanical, electrical, thermal)
- [ ] docker-compose / install / systemd / configs
- [ ] docs only

## Testing

<!--
How did you verify this works? Copy relevant `pytest` output or hardware
bring-up notes. "CI is green" is not enough for anything user-visible.
-->

- [ ] `pytest` passes locally in every touched component
- [ ] `ruff check .` clean
- [ ] `docker compose config` still parses
- [ ] Manual smoke test on a Jetson (if runtime behavior changed)

## Screenshots

<!-- Required for any UI change (pal-web, pal-face) or new dashboard panel. -->

## Security considerations (required for `pal-web` changes)

<!--
Answer every question. Delete the section only if this PR touches no code
under `pal-web/`.
-->

- Does this add or change any endpoint that accepts input from the LAN? If yes,
  which auth path guards it?
- Does this touch `pal-web/palweb/routers/remote.py` or any AI-initiated remote
  input path? If yes, confirm the `X-Consent-Origin` header check is present
  and covered by a test.
- Does this add any outbound network call? Per `ATLAS.md` §6, the answer must
  be no unless the destination is on the LAN.
- Does this add or change how user secrets, pairing tokens, or session tokens
  are stored?

## Checklist

- [ ] I read `CONTRIBUTING.md` and followed the commit-message convention.
- [ ] I have updated docs (`README.md`, `docs/`, or per-component `README.md`)
      if the user-visible behavior changed.
- [ ] I have added or updated tests for the behavior I changed.
- [ ] I have not added any cloud dependencies, telemetry, or third-party
      analytics (see `ATLAS.md` §6).
- [ ] I have not routed streams or UI to the Sphere face.
