# Redaction & Sensitive Information Policy

This documentation is public and intended to serve as a reusable template for other research groups running similar camera infrastructure.

## What Must Never Appear in This Documentation

- Real API keys, tokens, or console passwords
- Real internal IP addresses or hostnames
- Real MAC addresses of hardware
- Facility-identifying network names (SSIDs, VLAN names that reveal
  location/purpose)
- Any credentials, even expired or rotated ones

## Conventions for Examples

Use the following placeholders consistently across all pages:

| Type              | Placeholder / Convention                          |
|-------------------|----------------------------------------------------|
| IP addresses      | `192.0.2.x`, `198.51.100.x`, or `203.0.113.x` (RFC 5737 reserved documentation ranges) |
| Hostnames         | `console-a.example.com`, `camera-01.example.com` |
| API keys / tokens | `<YOUR_API_KEY>` |
| MAC addresses     | `00:00:00:00:00:00` style placeholder |
| Facility/site names | Generic labels like `Site A`, `Site B`, `North Building` |

## Handling Real Configuration Data

Actual API keys, IP addresses, and hardware inventory details specific to this deployment should be maintained **outside this repository**,
in a private, access-controlled location (e.g., a private wiki page,
password manager, or `.env` file excluded via `.gitignore`).

A suggested pattern:

```
# .env (NOT committed to the public docs repo)
CONSOLE_A_HOST=192.0.2.10
CONSOLE_A_API_KEY=xxxxxxxxxxxxxxxx
CONSOLE_B_HOST=192.0.2.20
CONSOLE_B_API_KEY=xxxxxxxxxxxxxxxx
```

Example code in this documentation should read values from environment variables or a config file, never hardcode them:

```python
import os

console_host = os.environ["CONSOLE_A_HOST"]
api_key = os.environ["CONSOLE_A_API_KEY"]
```

## Review Checklist Before Publishing a Page

- [ ] No real IPs, hostnames, or MACs
- [ ] No real API keys or credentials, even partial or truncated
- [ ] No facility-identifying details in screenshots or diagrams
- [ ] Any screenshots of the UniFi console UI have identifying info
      cropped or blurred (site name, device names, network details)
- [ ] Example code pulls sensitive values from environment/config,
      not inline
