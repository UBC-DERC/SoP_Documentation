# Assigning Static IPs to UniFi Consoles

UniFi Protect consoles that are assigned IPs by DHCP will pick up a different address after a
power outage or reboot if their lease has expired or if the DHCP server restarts. This causes
the API gateway (`derc-unifi-api`) to fail at startup, because it tries to connect to each
console at the address stored in its configuration.

This procedure covers the two approaches for making console IPs stable: **DHCP reservations**
(recommended) and **static IP configuration on the console itself**.

---

## Which Approach to Use

**DHCP reservations (recommended)** — configure the UDM Pro (console01) to always assign
the same IP to a device based on its MAC address. The console still uses DHCP, but it always
gets the same address. This is simpler and means the console's network configuration does not
need to be changed.

**Static IP on the console** — set the IP directly in the console's network interface
settings. Slightly more involved, but does not depend on the UDM Pro handing out the right
lease. Use this if the console is not behind the UDM Pro (e.g., console02 and console04 are
on the UBC Campus Network and their addresses are assigned by UBC IT's DHCP infrastructure —
contact UBC IT to request a reservation there).

---

## Method 1 — DHCP Reservation in the UDM Pro (Recommended for console01 and console03)

console01 and console03 are on subnets managed by the UDM Pro (`192.168.1.x` and
`10.34.173.x`). Use this method for those two consoles.

### Prerequisites

- You are on the Calf Barn LAN or SSH'd into CalfTop (`192.168.1.x` access)
- You know the MAC address of the console's LAN interface (see `consoles.csv` in `sop_private`)

### Steps

1. Open a browser and navigate to the UDM Pro: `http://192.168.1.1` (from CalfTop or another
   machine on the Calf Barn LAN)
2. Log in with your UniFi Network credentials
3. Go to **Settings** (the gear icon) → **Networks**
4. Click on the network the console is connected to (`net01` for console01 at `192.168.1.1`,
   or the `10.34.173.x` network for console03)
5. Scroll down to **DHCP** → expand **DHCP Reservations**
6. Click **Add Reservation**
7. Enter:
   - **MAC Address**: the console's MAC address (from `consoles.csv`)
   - **IP Address**: the desired fixed IP (use the address from the table in the SSH guide —
     e.g., `192.168.1.1` for console01, `10.34.173.7` for console03)
   - **Hostname** (optional but helpful): e.g., `console01`, `console03`
8. Click **Apply**

The reservation takes effect immediately. The console will receive the reserved address on its
next DHCP renewal or reboot.

!!! note "Verifying the reservation"
    After saving, go to **Clients** → find the console → confirm its IP matches the reserved
    address. If it still shows the old address, the lease has not renewed yet. You can either
    wait for the lease to expire naturally, or reboot the console to force a renewal.

---

## Method 2 — Static IP on the Console (for console02 and console04, or as a fallback)

console02 and console04 are on the UBC Campus Network (`10.34.49.x`). Their DHCP is managed
by UBC IT, not by the UDM Pro. The reliable option for these is either:

- **Request a DHCP reservation from UBC IT** (IT Service Centre ticket): provide the
  console's MAC address and the desired IP. UBC IT will bind the MAC to that address on their
  DHCP server. This is the cleaner approach — it keeps the consoles managed by DHCP but
  stable.

- **Set a static IP in UniFi OS** (fallback, if a UBC IT reservation is not feasible):

### Steps for setting a static IP in UniFi OS

1. Open a browser and navigate to `https://<current-console-ip>` (accept the certificate
   warning)
2. Log in with the UniFi OS admin credentials
3. Go to **OS Settings** (the gear icon in the left sidebar) → **System** → **Network**
4. Find the primary network interface (usually `eth0`)
5. Change the **IP Configuration** from **DHCP** to **Static**
6. Enter:
   - **IP Address**: the desired fixed IP (e.g., `10.34.49.6` for console02)
   - **Subnet Mask**: `255.255.255.0` (or `/24`)
   - **Gateway**: the default gateway for that subnet (UBC IT can confirm this — it is
     typically the `.1` address, e.g., `10.34.49.1`, but verify this before entering it to
     avoid losing connectivity)
   - **DNS**: UBC IT's DNS servers (ask UBC IT, or use `8.8.8.8` and `8.8.4.4` as
     fallbacks)
7. Click **Apply**

!!! warning "Risk of losing console access"
    Setting the wrong gateway will cut off the console from the network immediately. Confirm
    the correct gateway with UBC IT before making this change. If you lose access, physical
    access to the console's HDMI output may be required to recover it.

---

## After Fixing the IPs

Once each console has a stable address:

1. Update `consoles.csv` in `sop_private` with the confirmed IPs
2. Update the console IP table in `docs/technical/ssh/ssh-console-access.md`
3. Update the `.env` file in `sop_private` with the new console addresses (used by
   `derc-unifi-api`)
4. Confirm the gateway can connect to each console: run the offline inventory checker
   (`scripts/check_inventory.py`) from CalfTop and verify all four consoles are reachable

---

## Checking Whether a Console Is Using DHCP or a Static IP

From a machine that can reach the console, SSH in as `root` and run:

```bash
cat /etc/network/interfaces
# or, on newer UniFi OS versions:
ip addr show eth0
```

If the interface is configured by DHCP, you will see `dynamic` or `dhcp` in the output. If it
is static, you will see the assigned IP, netmask, and gateway directly.

You can also check from the UniFi OS dashboard: **OS Settings → System → Network** — the IP
Configuration field shows **DHCP** or **Static**.
