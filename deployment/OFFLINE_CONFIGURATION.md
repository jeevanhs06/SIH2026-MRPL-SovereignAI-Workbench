# Offline & Firewall Configuration (Starter)

This scaffold is designed for local-only operation. It **does not claim to prove host firewall enforcement**.

## App-level controls included

- `SOVAI_OFFLINE_MODE=true` toggles offline-first mode in backend status reporting.
- `SOVAI_MODEL_ENDPOINT` defaults to `http://127.0.0.1:11434`.
- `/security/network-status` verifies whether the configured model endpoint is local and whether it is reachable.

## Host/network controls to configure outside app

1. Deny default outbound traffic on host/firewall.
2. Allow loopback (`127.0.0.1`) and required local subnet addresses only.
3. If Docker is used, enforce egress rules for bridge networks.
4. Enable host-level logging for rejected outbound attempts.

## Verification

Use:

```bash
scripts/verify_offline.sh
```

and combine it with host firewall logs for full sovereignty proof in real deployments.
