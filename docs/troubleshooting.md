# Troubleshooting

Start with the exact error message and the client version. Keep the existing installation while diagnosing a problem; repeated fresh installations are usually unnecessary.

| What you see | What to do |
| :--- | :--- |
| **Install PowerShell 7** | Install PowerShell 7, then rerun `Install-FOOTISTA.cmd`. Windows PowerShell 5.1 does not satisfy this requirement. |
| **This release needs Python 3.13 x64** | Install Python 3.13 for Windows x64 with its launcher. Other Python versions and ARM64 builds are not the required runtime. |
| **Tcl/Tk unavailable / club picker cannot open** | Modify the Python 3.13 installation and add Tcl/Tk, then retry. |
| **Missing .NET Desktop Runtime or WebView2** | Install the x64 .NET 10 **Desktop** Runtime and WebView2 Runtime, then retry. The .NET server runtime alone is insufficient. |
| **ICF / printer DLLs missing** | Get the matching ICF and OS Update's **Extracted Files** from `_Misc`; select their folder/archive when prompted. They are not all in the main game archive. |
| **Archive cannot be read** | Extract with 7-Zip and select the resulting game folder. Do not feed a raw APP, PACK or VHD to setup. |
| **File checksum differs** | Confirm the game is 1.30.01 / 2019 Series 3 and the support files match it. Retain an original source rather than combining files from different revisions or modified game folders. |
| **Not enough space** | Free space on the intended destination drive. Keep the game source and club profiles on the same NTFS drive where possible. |
| **Path too long** | Use a short, real folder path such as `C:\Games\Footista2019` for a new installation. Do not manually move an already provisioned profile or substitute a junction. |
| **A game is already running** | Close the existing game normally before switching clubs, opening Terminal or retrying an update. |
| **Website approval / connection error** | Confirm that you can sign in to wccf.online, then reconnect through **Connect** and approve the matching code. Rejected or revoked PC approval needs a new normal approval. |
| **Publisher / signature error** | Keep your existing trust key. Obtain the installer from this project's official download page; report the exact failure. |
| **Update rejected / previous version restored** | Keep the previous working version and report the failed version and error. Do not repeatedly delete and reinstall your club. |
| **No Digital Cards / zero scout tickets** | Printed cards and unprinted digital cards are different lists. Zero tickets after using your stock is expected. |
| **Original card missing after rank-up** | It is retired as Evolved; the new card is its playable replacement. See [Clubs and cards](clubs-and-cards.md). |

For setup details, see [Installation](installation.md). For a repeatable problem, open a [bug report or setup-help request](https://github.com/Forza-WCCF/FOOTISTA-2019/issues/new/choose).

Include your client version, Windows version, the mode you opened, the steps to reproduce and the exact error text. For setup, say whether you selected a `.7z`, `.zip` or extracted folder, and whether you supplied the ICF / OS Update.

Crop personal information out of screenshots. Do not post your whole installation, browser profile, private keys, credentials, approval codes or player databases. See [Support](../SUPPORT.md).
