# Changes

## 0.2.19 — first public beta

- Usable printed cards are restored from your saved club on a clean PC, even with an empty local print-image folder.
- Existing local print images take priority; restored cards use website artwork or a named placeholder. Ownership, progress and printer counters are not changed by restoring the library.
- Includes game archive/folder setup, separate ICF / OS Update discovery, website-connected clubs, more English and signed client updates from external hosting.
- The fresh-install check caught the missing library in 0.2.18; 0.2.19 was verified through native card registration, a CPU match save, Terminal readback and clean shutdown. No new physical print was performed in that acceptance run; the unchanged native printer pipeline retains its earlier acceptance evidence.

Two-PC PvP and the full-size MEGA archive container remain unverified. Archive layout tests and the verified extracted game folder were used during acceptance.

## 0.2.18 — superseded before publication

The next website release brings together the changes tested in the private client builds:

- Setup accepts the local FOOTISTA 1.30.01 game `.7z`, a `.zip` or an extracted game folder, and locates the separate ICF / OS Update files.
- The club picker connects a website account and offers separate game profiles for its clubs.
- More English across tutorials, story subtitles and Terminal screens, with clearer captions.
- The Terminal hides the empty expiry display when no scout tickets remain.
- Installer and update downloads can use external hosting while preserving signature, size and checksum checks.

This candidate was **not published**: a clean existing-club profile had an empty card library. The correction is included in 0.2.19. See [the release procedure](docs/releases.md) and [the public candidate record](releases/0.2.18.json).

## Private acceptance leading to this candidate

The basic tutorials, normal match saves, logout, club-title change, 20 scout draws with full-size reveals, and populated Terminal sorting/filtering were accepted during private testing. The empty ticket-expiry display was also checked after the ticket stock reached zero.

Positive-stock expiry presentation, some translated native screens, the full fresh-installer cycle and matches between two real PCs remain to be checked. There is no public 0.2.x release history implied by the private build numbers.
