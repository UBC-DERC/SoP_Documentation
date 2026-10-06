# SSH Access to UniFi Consoles

This procedure covers enabling SSH on a UniFi Protect console, verifying the connection
works, and diagnosing the most common failure modes. It applies to all four consoles in the
UBC DERC camera system.

---

## Prerequisites

Before starting, confirm:

- You are connected to **UBC VPN** (required to reach consoles on the `10.34.x.x` network)
- You know the **UniFi OS admin password** for the target console (stored in the `.env` file
  in `sop_private`)
- You know the console's **IP address** (see the table below)

| Console | Location | Last Known IP | Network |
|---|---|---|---|
| console01 | Calf Barn | `192.168.1.1` | Calf Barn LAN — reachable from CalfTop only |
| console02 | Main Barn | `10.34.49.6` | UBC Campus Network |
| console03 | Heifer Barn | `10.34.173.7` | UBC Campus Network |
| console04 | Main Barn | `10.34.49.1` | UBC Campus Network |

!!! warning "Console IP addresses may change after a power outage"
    Some consoles are assigned IPs by DHCP rather than using a static configuration.
    After a power outage or reboot, a console may come back on a different address than
    the one listed above. If the address in the table does not respond, check the UDM Pro's
    DHCP lease table for the current address — see
    [Finding a console's current IP](#finding-a-consoles-current-ip) below.

    The permanent fix is to assign a **static IP** to each console (either a fixed IP in
    UniFi OS or a DHCP reservation by MAC address in the UDM Pro). See
    [Setting static IPs on UniFi consoles](static-ip-consoles.md).

!!! warning "console01 is not directly reachable via VPN"
    console01 (`192.168.1.1`) is on the private Calf Barn LAN. You can only reach it
    from CalfTop or from another machine on the `192.168.1.x` network. SSH into CalfTop
    first, then connect to console01 from there.

---

## Step 1 — Enable SSH on the Console

SSH is disabled by default on UniFi OS. It must be enabled through the web dashboard.

1. Open a browser and navigate to `https://<console-ip>` (accept the self-signed certificate
   warning)
2. Log in with the UniFi OS admin credentials
3. Go to **OS Settings** (the gear icon in the left sidebar) → **System** → **Advanced**
4. Find the **SSH** toggle and enable it
5. Set or confirm the SSH password — this is the password you will use to log in as `root`
6. Click **Apply**

UniFi OS starts the SSH daemon immediately. Wait approximately **60 seconds** before testing.

!!! note "SSH credentials"
    UniFi OS uses `root` as the SSH username. The SSH password is whatever you set in the
    Advanced settings panel — it is not necessarily the same as the web UI login password
    unless you set them the same deliberately.

---

## Step 2 — Test Connectivity

Run these checks in order. Each one tells you something different about where a problem is.

### 2a. Confirm the host is reachable at all

```bash
ping -c 4 <console-ip>
```

**Expected:** 4 replies with low latency (~1 ms for console03, which is on the same subnet
as CalfTop).

If ping fails entirely, either VPN is not connected or routing to that subnet is not working.
Stop here and reconnect VPN before continuing.

### 2b. Confirm the SSH port is open

```bash
nc -zv <console-ip> 22
```

**Expected:** `Connection to <ip> 22 port [tcp/ssh] succeeded!`

**If you get `Connection refused`:** The host is reachable but nothing is listening on port 22.
Either the SSH daemon has not started yet (wait another 60 seconds and retry), or the enable
did not save — log back into the dashboard and confirm SSH is still toggled on.

**If you get a timeout (no response):** A network firewall between you and the console is
silently dropping the connection. This is different from the console refusing it — see
[Troubleshooting](#troubleshooting) below.

### 2c. Confirm the web UI is responding (optional sanity check)

```bash
curl -k -s -o /dev/null -w "%{http_code}" https://<console-ip>
```

**Expected:** `200` or `302`. If this works but SSH is refused, the console is healthy and
the SSH daemon is the only issue.

---

## Step 3 — Connect via SSH

```bash
ssh root@<console-ip>
```

Enter the SSH password you set in Step 1 when prompted.

If the connection succeeds, you will see a UniFi OS shell prompt. You are now logged in as
`root` on the console's operating system.

**To disconnect:** type `exit` or press `Ctrl-D`.

### Saving the connection details

Add an entry to `~/.ssh/config` on your laptop so you do not have to remember the IP:

```
Host console03
    HostName 10.34.173.7
    User root

Host calftop
    HostName 10.34.173.8
    Port 22958
    User dercadm
```

Then `ssh console03` connects directly.

---

## Finding a Console's Current IP

If a console's IP address has changed (e.g., after a power outage), locate it through the
UDM Pro management interface before attempting SSH.

### Via the UniFi Network dashboard

1. Open a browser and navigate to the UDM Pro address (`192.168.1.1` from CalfTop, or via
   whatever address the UDM Pro is reachable at on the UBC Campus Network)
2. Log in with your UniFi Network credentials
3. Go to **Clients** → filter by **Wired** and **Active only**
4. Find the console by its hostname (e.g., `UDMP`, `UNVR`) or by the last-known MAC address
5. The current IP address is listed in the client row

Alternatively, look in **Settings → Networks → [the relevant network] → DHCP** for the
active lease table.

### Via the console's hostname (if DNS or mDNS is available)

Some UniFi consoles advertise via mDNS. From CalfTop:

```bash
avahi-browse -r _http._tcp | grep unifi
```

Or try pinging by hostname:

```bash
ping -c 2 UDMP.local
ping -c 2 unifi.local
```

This is not guaranteed to work across subnets, but works reliably on the `192.168.1.x` and
`10.34.173.x` segments from CalfTop.

### After finding the IP

Update the IP table in this document and in `consoles.csv` in `sop_private`. Then follow the
permanent fix procedure in [Setting static IPs on UniFi consoles](static-ip-consoles.md) to
prevent the address from changing again.

---

## Troubleshooting

### "Connection refused" on port 22

The host is reachable but SSH is not listening on that port.

- Wait 60 seconds and retry — the daemon takes time to start after being enabled in the UI
- Log back into the UniFi OS dashboard and confirm SSH is still enabled; re-enable and save
  if needed
- Try port 22222 in case a non-standard port was configured: `nc -zv <console-ip> 22222`

---

### "Connection reset by peer" during handshake

```
kex_exchange_identification: read: Connection reset by peer
```

The TCP connection succeeded, SSH started to respond, but then reset before completing the
handshake. This is almost always a TCP wrapper or firewall rule blocking your source IP.

The SSH daemon on the console accepted the socket, checked the source IP against an allow
list, and reset the connection before sending its banner.

**Check your effective IP:**

```bash
curl -s https://ifconfig.me
```

**On the console or CalfTop**, check TCP wrappers:

```bash
cat /etc/hosts.allow
cat /etc/hosts.deny
```

If `hosts.deny` contains `ALL: ALL` or `sshd: ALL`, add your IP or VPN subnet to
`hosts.allow`:

```bash
echo "sshd: <your-ip>" | sudo tee -a /etc/hosts.allow
# or for a whole subnet:
echo "sshd: 10.0.0.0/8" | sudo tee -a /etc/hosts.allow
```

No restart is needed for TCP wrapper changes — they take effect immediately.

---

### "Connection timed out" (no response at all)

The packet never arrived. Either:

- VPN is not connected — reconnect and retry
- Routing from the VPN to that subnet is not configured — you may need to reach the console
  from CalfTop rather than directly from your laptop
- A network firewall between you and the console is silently dropping packets

For console01 (`192.168.1.1`), a timeout from your laptop is expected — that address is only
reachable from CalfTop. SSH into CalfTop first, then connect to console01 from there.

---

### SSH key not accepted / password prompt loops

- Confirm you are using `root` as the username (not your UniFi web UI username)
- The password is the SSH-specific password set in UniFi OS → System → Advanced → SSH, not
  necessarily the web UI login password
- If you have an SSH key configured in the UniFi OS dashboard, your laptop's key must match
  — check with `ssh-add -l` to see which keys are loaded

---

### Changes to `sshd_config` not taking effect (CalfTop only)

If you edited CalfTop's SSH configuration directly (not via a UI), restart the daemon to
apply changes. **First** verify the config has no syntax errors:

```bash
sudo sshd -t
```

If that passes, restart safely:

```bash
sudo systemctl restart ssh
```

Keep your existing session open while testing the new configuration in a second terminal.
Do not close your working session until you have confirmed the new config lets you back in.

---

## Security Notes

- Delete session cookie files (`~/cookies.txt`) after testing curl-based API access — they
  are active credentials
- Do not leave SSH enabled on consoles permanently unless there is an operational need —
  disable it in the UniFi OS dashboard when you are done
- SSH credentials for each console are stored in `sop_private` — do not record them in any
  public repository or documentation
- CalfTop's SSH is on a non-standard port (`22958`) — this is intentional and should be
  maintained when updating SSH configuration
