# Install FOOTISTA 2019

The current **0.2.18** installer is an unreleased candidate. These instructions describe that candidate; a complete fresh installation and native launch still need acceptance before the public download opens.

## Requirements

| Requirement | Details |
| :--- | :--- |
| **Windows** | 64-bit Windows. Use a recent Windows 11 build for direct `.7z` support; otherwise extract the archive yourself and select its folder. |
| **Game** | FOOTISTA 2019 **1.30.01 / 2019 Series 3**, with the matching ICF and extracted OS Update files. |
| **PowerShell** | [PowerShell 7](https://learn.microsoft.com/powershell/scripting/install/installing-powershell-on-windows). Windows PowerShell 5.1 is a different program. |
| **Python** | [Python 3.13, Windows x64](https://www.python.org/downloads/windows/), including the launcher and Tcl/Tk. The installer creates a private Python environment. |
| **Desktop runtime** | [.NET 10 Desktop Runtime, Windows x64](https://dotnet.microsoft.com/download/dotnet/10.0), plus [Microsoft Edge WebView2 Runtime](https://developer.microsoft.com/microsoft-edge/webview2/). |
| **Internet** | Needed for website approval, the community server and downloads. Setup installs pinned Python dependencies from PyPI. |
| **Storage** | Enough for your downloaded archive and extracted game. Setup checks the required free space before extraction. |

There is no published minimum GPU specification yet. Gameplay performance still depends on the PC.

## Game downloads

The game and supporting files are external downloads. They are not stored in this GitHub repository or on the wccf.online web server.

- **[Game archive: MEGA Extracted Files folder](https://mega.nz/folder/9mJilJQI#KdqiR2mkfu2o9LKAVOTdyA/folder/BuoHyBDS)**
- **[Supporting downloads: MEGA SDEB root](https://mega.nz/folder/9mJilJQI#KdqiR2mkfu2o9LKAVOTdyA)**

In the MEGA folder, follow this layout:

```text
SDEB
├── BASE Version 1.30.01 [2019 Season 3]
│   └── Extracted Files
│       └── SDEB_1.30.01_20190603145829_0.7z   ← game archive
└── _Misc
    ├── ICF (1.30.01)                        ← matching ICF download
    └── OS Update → Extracted Files          ← extracted OS Update download
```

The `_Misc` entries above describe what to choose in the browser; your downloaded filenames and wrapper folders can differ. The installer finds the required files by their signed checksums.

Download the game archive and both supporting downloads. Keep them together in a local folder, for example `C:\Games\FOOTISTA-Downloads`. You can also supply the support folder or archive separately when setup asks.

Use **Extracted Files** for the OS Update. The raw **Original PACK**, APP and VHD images are not installer inputs. The ICF and OS Update are separate from the main game archive; the game archive alone is insufficient.

## Install the client

1. When the public release opens, download **`installer.zip`** from [wccf.online](https://wccf.online/misc.php?action=wccf_downloads) or this project's [Releases](https://github.com/Forza-WCCF/FOOTISTA-2019/releases).
2. Extract the whole installer ZIP into a normal folder. Do not run it inside an archive viewer. GitHub's **Source code** downloads are not the installer.
3. Run **`Install-FOOTISTA.cmd`**. Choose your downloaded `SDEB_1.30.01_20190603145829_0.7z`, or an already extracted game folder.
4. If asked for supporting files, choose the folder or archive containing the ICF and extracted OS Update downloads.
5. Let setup verify the files and finish. The default installation is **`%LOCALAPPDATA%\Footista2019`**.
6. Open **`MANAGE-CLUBS.cmd`** in that installation. Choose **Connect**, sign in on the website and approve the code shown by the picker.
7. Select an existing club, or choose **New club on website**. Select **Play Satellite** to play or **Open Terminal** to manage cards and scout.

Only one native game may run on the PC at a time. Close the current game before opening another club or switching modes.

## What setup accepts

| You have | Select |
| :--- | :--- |
| The downloaded MEGA game | The `.7z` file itself. |
| A ZIP containing the game files | The local `.zip`. |
| An extracted wrapper folder | The folder containing `internal_0`. |
| The extracted game root | `internal_0` itself, or its surrounding game folder. |
| Raw APP / PACK / VHD images | Obtain the **Extracted Files** download first. |

If the local Windows archive reader cannot handle a container, extract it with [7-Zip](https://www.7-zip.org/) and select the resulting folder. Pasting a MEGA URL into setup does not download the game.

## Storage and your mobile data

Selecting a complete extracted game folder reuses its existing files. Selecting an archive extracts the required game files into the installation's **`game-source`** folder. Keep that folder: your club profiles use it. Setup does not import saves or credentials from the downloaded game.

When source files and a club profile are on the same NTFS drive, eligible large files are hardlinked. A hardlink is another filename for the same local file contents, so it does not use mobile data or store another full copy. Files on different drives must be copied, which needs extra space; additional club profiles can also require copies in that case. The game is tens of gigabytes, so keeping its source and profiles on the same drive matters.

The installer ZIP is about 50 MB and already contains `client.zip`; a first-time player does not need to download both. Python dependencies and missing runtimes are additional downloads. Normal website and game-server traffic also uses the internet. Setup does not automatically download the MEGA game archive.

If setup reports missing support files, provide them and run setup again at the same destination. Do not make another installation for each retry, or delete an existing club's files. [Troubleshooting](troubleshooting.md) covers the common cases.
