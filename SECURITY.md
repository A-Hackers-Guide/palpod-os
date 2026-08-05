# Security Policy

Hearth is a $95k box that sits in a customer's home. Security issues get
treated with the seriousness that framing implies. If you have found one,
please report it privately so we can fix it before anyone gets hurt.

---

## Supported versions

HearthOS is pre-1.0. Only the current `main` branch is supported for
security fixes; there is no LTS line yet. Once we cut `v1.0`, this section
will list the supported minor releases.

| Version | Supported          |
|---------|--------------------|
| main    | :white_check_mark: |
| < 1.0   | :white_check_mark: (rolling — no LTS yet) |

---

## Reporting a vulnerability

**Email `security@palpod.com`.** Do not open a public GitHub issue.

Please include:

- A description of the vulnerability and its impact.
- Steps to reproduce, or a proof-of-concept.
- The version of HearthOS you observed it on
  (`git -C /opt/palpod-os describe --tags --always --dirty`).
- Your name / handle / affiliation for the hall of thanks below, or a note
  that you would like to remain anonymous.

If you want to encrypt your report, our PGP public key fingerprint is:

```text
<TODO: outside counsel to publish PGP fingerprint here on formation.>
```

We will acknowledge receipt within **3 business days**, provide a preliminary
assessment within **10 business days**, and target a fix or a documented
mitigation within **90 days** of receipt. If a fix will take longer than 90
days we will coordinate a disclosure date with you before that window closes.

---

## Scope

**In scope:**

- The `pal-web` FastAPI service and its endpoints
  (`palpod-os/pal-web/palweb/`), including all authentication, session, and
  remote-device paths.
- The `pal-voice` orchestrator (`palpod-os/pal-voice/palvoice/`), including
  wake-word, STT, LLM, TTS handling, and any bridges into `pal-web`.
- The install / update / uninstall scripts, systemd units, and Docker Compose
  configuration in this repository.
- The RustDesk configuration shipped in `configs/rustdesk/` (self-hosted
  rendezvous + relay).

**Out of scope:**

- **Attacks that require LAN-local access with physical proximity.** The whole
  product thesis is *"nothing leaves the house."* Every capability listens on
  the LAN; a LAN-adjacent attacker who is already inside the customer's home
  network is inside the trust boundary by design. If your finding assumes the
  attacker is already on the same Wi-Fi as the Pod, that is a design
  characteristic, not a vulnerability. (You may still file it as a normal
  bug if you think we can harden it usefully without breaking the model.)
- Attacks that require physical access to the Pod (JTAG, serial console,
  bootloader replacement, chip pull). Same reasoning: the Pod is a physical
  object in a physical home.
- Third-party services running behind the Traefik reverse proxy (Plex,
  Jellyfin, Audiobookshelf, Sunshine, upstream RustDesk / AnyDesk). Please
  report those directly to their upstream projects; if the packaging
  configuration we ship in `configs/` exposes something the upstream did not
  intend, that IS in scope.

---

## Coordinated disclosure

We follow a 90-day coordinated-disclosure timeline. On receipt we work with
the reporter to:

1. Confirm the issue.
2. Assess severity and scope.
3. Develop and test a fix on a private branch.
4. Cut a patched release and notify affected customers.
5. Publish the advisory (typically as a GitHub Security Advisory), crediting
   the reporter unless anonymity was requested.

If a public disclosure is imminent from a third party (e.g. the same
vulnerability is reported to a mailing list) we may move faster. We will
never sue or otherwise pursue researchers acting in good faith under this
policy.

---

## Hall of thanks

We publicly thank researchers who report in good faith. If you'd like to be
listed, tell us how to credit you when you file the report.

<!-- Keep the table alphabetical by reporter name; date is receipt date. -->

| Reporter | Vulnerability | Disclosure date |
|----------|---------------|-----------------|
| _first entry pending_ | — | — |
