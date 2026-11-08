# Maintainer release procedure

The client is built and signed in the private development workspace. This public repository holds the guides and public release records. Its CI checks those files; it does not build or sign the client.

## Before making a release public

1. Build once using the established publisher key and a new release sequence. Keep the private key on the signing PC.
2. Verify the signed manifest, complete client inventory, archive hashes and absence of player data. Review the exact bytes to be distributed.
3. Finish the fresh-installer and native acceptance checks for that exact build: website approval, club selection, launch, print/save/reload and clean close. Test normal updating separately. Record any untested capabilities without claiming they passed.
4. Update the public version record, changelog and release notes. Do not mark a candidate accepted merely because source tests passed.
5. Create a **draft** GitHub Release with the matching version tag. Attach the reviewed `installer.zip`, `client.zip`, `release.json` and `SHA256SUMS.txt`. The installer already contains the client archive; players installing for the first time download only `installer.zip`.
6. Check the uploaded asset sizes and SHA-256 digests against the local review. Publish only after the release is accepted and publication is authorized.
7. Configure the website's versioned external links. The website stores signed metadata, checksums and URLs; both ZIPs remain on the external host. Activate the website's latest metadata last, then verify its public download link resolves to the accepted release asset.

For the first upgrade from a private 0.2.17 installation, use the established local signed update/installer path. That older client does not understand the new external archive redirects. Do not tell existing testers that an external automatic upgrade from 0.2.17 has been verified.

## Release assets

| Asset | Purpose |
| :--- | :--- |
| `installer.zip` | Complete setup package for players. |
| `client.zip` | Signed update payload used by the updater; also nested in the installer. |
| `release.json` | Signed release metadata for this exact build. |
| `SHA256SUMS.txt` | Checksums for the three assets above. |

Never attach the original game, a prepared personal installation, player databases, account maps, browser profiles, protected credentials, signing secrets, server administration keys or test-account state.

GitHub Releases and Pixeldrain are alternative external hosts, not two required downloads. A draft without uploaded assets is only a release placeholder. Repo creation, tag creation and a checksum record do not publish an installer or activate the website download.

## Current candidate

**0.2.18 / sequence 22** is built and signature-verified. Small archive-layout tests and source tests passed. Full-size MEGA extraction and the complete fresh-installer/native rehearsal have not passed yet. Neither a public release nor website activation is authorized by the existence of this candidate record. Two-PC PvP testing remains separate.
