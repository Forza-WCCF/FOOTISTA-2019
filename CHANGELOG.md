# Changes

## 0.2.18 — unreleased candidate

The next website release brings together the changes tested in the private client builds:

- Setup accepts the local FOOTISTA 1.30.01 game `.7z`, a `.zip` or an extracted game folder, and locates the separate ICF / OS Update files.
- The club picker connects a website account and offers separate game profiles for its clubs.
- More English across tutorials, story subtitles and Terminal screens, with clearer captions.
- The Terminal hides the empty expiry display when no scout tickets remain.
- Installer and update downloads can use external hosting while preserving signature, size and checksum checks.

This candidate is **not a published download**. Source tests and the private gameplay checks do not replace the final fresh-installer/native acceptance of these exact release bytes. See [the release procedure](docs/releases.md) and [the public candidate record](releases/0.2.18.json).

## Private acceptance leading to this candidate

The basic tutorials, normal match saves, logout, club-title change, 20 scout draws with full-size reveals, and populated Terminal sorting/filtering were accepted during private testing. The empty ticket-expiry display was also checked after the ticket stock reached zero.

Positive-stock expiry presentation, some translated native screens, the full fresh-installer cycle and matches between two real PCs remain to be checked. There is no public 0.2.x release history implied by the private build numbers.
