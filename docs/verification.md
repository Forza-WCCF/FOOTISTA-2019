# Verify a download

Use the asset attached to the accepted [GitHub Release](https://github.com/Forza-WCCF/FOOTISTA-2019/releases) or the [website Downloads page](https://wccf.online/misc.php?action=wccf_downloads). **Source code (zip)** is the repository, not the installer.

**0.2.19** is the public beta. The earlier **0.2.18** record remains marked as an unreleased candidate: the fresh test found a missing-card-library issue, which was fixed before publication.

## Check SHA-256 in PowerShell

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath "$env:USERPROFILE\Downloads\installer.zip"
```

Compare the full hash with the accepted release's `SHA256SUMS.txt` and its version record under [`releases/`](../releases). The file's size must match too. A matching hash detects altered or incomplete bytes; the client additionally verifies its signed release against its pinned publisher key.

## Check with the repository tool

If you have downloaded this repository, Python 3.13 can check size and SHA-256 without installing packages:

```powershell
py -3.13 tools/verify_download.py "$env:USERPROFILE\Downloads\installer.zip" --version 0.2.19
```

If the browser renamed the download, specify its original asset name:

```powershell
py -3.13 tools/verify_download.py "$env:USERPROFILE\Downloads\installer (1).zip" --version 0.2.19 --artifact installer.zip
```

The tool reads a local file. It makes no network request, extracts nothing and never launches the installer. An unreleased record is shown as such even when its bytes match.

## Publisher identity

The public Ed25519 verification key is [`releases/public-key.ed25519`](../releases/public-key.ed25519). Its SHA-256 fingerprint is:

```text
124756359e4e1aec7d8f6690b31310d508e78e84f62236fbe754053c22cf438a
```

This is a **public** key. The private signing key is not part of the repository, installer or website. An established installation pins its publisher locally; never replace that pinned key just to make an unexpected update pass.
