# CalfTop Host Documentation

!!! warning "Page not yet generated"
    This page is generated automatically by `scripts/generate_host_info.py`.
    It has not been run on CalfTop yet, so no host information is available.

    To populate this page, run the following command **on CalfTop**:

    ```bash
    python scripts/generate_host_info.py
    ```

    Then commit the updated `docs/technical/cameras/admin/calftop.md` and redeploy
    the documentation site.

## About CalfTop

CalfTop is an Ubuntu 24.04 workstation located in the Calf Barn office at UBC DERC.
It serves as the researcher-facing API gateway host for the UniFi Protect camera system
(see [ADR-002](../log/adr-002-gateway-host.md)).

CalfTop is **dual-homed**:

- **Calf Barn LAN (`192.168.1.x`)** — wired directly to `console01` (the UDM Pro)
- **UBC Campus Network (`10.34.173.8`)** — wired directly onto the UBC network;
  same subnet as `console03` (Heifer Barn). Researchers reach the gateway API
  via UBC VPN at this address.

See the [SSH guide](../../../../ssh/index.md) for remote access instructions.
