# Camera Administration

## The Camera Network

The diagram below shows the physical network topology: three barn locations, four UniFi Protect
consoles, and CalfTop — the API gateway host, which is **dual-homed** on both the Calf Barn LAN
and the UBC Campus Network.

```mermaid
architecture-beta
    group calfbarn(mdi:barn)[Calf Barn]
    group calfoffice(mdi:office-building)[Office] in calfbarn
    group calfboiler(mdi:office-building)[Boiler Room] in calfbarn
    group mainbarn(mdi:barn)[Main Barn]
    group barnoffice(mdi:office-building)[Main Office] in mainbarn
    group heiferbarn(mdi:barn)[Heifer Barn]
    group ubcnet(internet)[UBC Campus Network]
    group wireless(internet)[WiFi Networks]
    group apilayer(internet)[Research API Layer]

    service rogers(internet)[Rogers ISP]
    service arc(cloud)[Advanced Computing]
    service vpn(internet)[UBC VPN]

    service dream(server)[console01 UDM Pro] in calfoffice
    service calftop(mdi:laptop)[CalfTop Gateway] in calfoffice
    service switch(typcn:flow-switch)[UniFi Switch] in calfboiler
    service camerabullet(material-symbols:camera-video)[Calf Cameras 4] in calfbarn
    service visitorcalf(material-symbols:wifi)[UBC Visitor] in calfbarn
    service shelly(cbi:shelly-logo)[Shelly Plugs] in calfbarn

    service unvr_robots(disk)[console02 UBCRobots] in barnoffice
    service unvr_main(disk)[console04 UBCMainBarn] in barnoffice
    service camerag4(material-symbols:camera-video)[Robot Cameras 12] in mainbarn
    service cameramain(material-symbols:camera-video)[Main Cameras 3] in mainbarn

    service unvr_heifer(disk)[console03 UBCHeiferBarn] in heiferbarn
    service camerahb(material-symbols:camera-video)[Heifer Cameras 2] in heiferbarn

    service ubccore(internet)[UBC Network Core] in ubcnet

    service visitor(material-symbols:wifi)[UBC Visitor] in wireless
    service eduroam(material-symbols:wifi)[EduRoam] in wireless
    service secure(material-symbols:wifi)[UBCSecure] in wireless

    service uiprotect(mdi:code-braces)[uiprotect library] in apilayer
    service researcher(mdi:account-school)[Researcher Script] in apilayer

    rogers:L -- R:ubccore
    ubccore:R -- L:arc
    dream:B -- T:rogers
    calftop:R -- L:dream
    calftop:T -- B:ubccore
    switch:T -- B:dream
    camerabullet:R --> L:switch
    visitorcalf:T -- B:rogers
    shelly:B -- T:visitorcalf
    visitor:T -- B:ubccore
    eduroam:T -- B:ubccore
    secure:T -- B:ubccore
    unvr_robots:T -- B:ubccore
    unvr_main:T -- B:ubccore
    camerag4:R -- L:unvr_robots
    cameramain:R -- L:unvr_main
    unvr_heifer:T -- B:ubccore
    camerahb:R -- L:unvr_heifer
    vpn:R -- L:ubccore
    uiprotect:B -- T:calftop
    researcher:R -- L:vpn
```

!!! note "CalfTop is dual-homed"
    CalfTop has two network connections:

    - **`net01` (192.168.1.x)** — wired directly to `console01` (the UDM Pro). Used for local Calf
      Barn camera access without touching the UBC network.
    - **`10.34.173.8`** — wired directly onto the UBC Campus Network. This is the same subnet
      (`10.34.173.x`) as `console03` (Heifer Barn, `10.34.173.1`), so that console may be
      reachable without additional routing. `console02` and `console04` (both on `10.34.49.x`)
      are on a different UBC subnet; reachability depends on UBC IT routing between subnets.

    Researchers connect to the gateway API at `10.34.173.8` over UBC VPN — no separate
    VPN or port forwarding is needed.

## Console and Camera Inventory

| Console ID | Label | Model | Location | Network | Cameras |
|---|---|---|---|---|---|
| `console01` | UBC DERC Calf Barn DM1 | UDM Pro | Calf Barn | `net01` 192.168.1.0/24 | 4 × G5 Bullet (wired) |
| `console02` | UBC-Robots | UNVR | Main Barn | `net02` 10.34.49.x | 12 × G4 Bullet (wired) |
| `console03` | UBC-HeiferBarn | UNVR | Heifer Barn | `net03` 10.34.173.x | 2 × G6 Instant (wireless) |
| `console04` | UBC-Main-Barn | UNVR | Main Barn | `net04` 10.34.49.x | 3 × G6 Instant (wireless) |

See the [Camera Inventory](../index.md) for the full per-camera details.

## Troubleshooting

You can find reporting of issues we've encountered on the [Troubleshooting](troubleshooting.md) page.
