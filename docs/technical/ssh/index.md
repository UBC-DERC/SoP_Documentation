# OpenSSH Server Setup & Troubleshooting

This documentation assumes you have access to UBC's VPN service through Land and Food Systems. If you do not have this access (and are a member of Land and Food Systems at UBC) you can follow the [LFS VPN setup](https://my.landfood.ubc.ca/lfs-intranet/tech-resources/connecting-to-the-lfs-vpn/) instructions.

## Environment

These instructions are written primarily for a user who is using a Linux (Ubuntu) installation. That user is able to connect to the UBC/LFS VPN.

## Network Topology

<TO BO ADDED>

## Steps Taken

### Verify SSH server installed and running on the remote server

These are steps to be taken by the Dairy Data Manager. If you are using the `ssh` service to access a remote computer you can skip this step.

- `openssh-server` package confirmed installed (`dpkg -l`)
- `ssh` service confirmed active via `systemctl status ssh`
- Confirmed listening via `ss -tlnp`:

```bash
LISTEN 0 4096 0.0.0.0:22958  0.0.0.0:*
```

- Confirm via `/etc/ssh/sshd_config`
  - `Port 22958` is set intentionally (non-standard port, common security practice)
- **All subsequent steps must reference port 22958**, not default port 22.

## Remote Connection

A user with a valid VPN should be able to log in to the remote server using:

```bash
ssh -p <PORT> <your-user>@<IPADDRESS>
```

Ensure that you have a user account on the remote server. Use the proper IP address of the remote server and the assigned port.

