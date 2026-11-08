"""Verify a published installer and the real updater download on an ephemeral CI runner."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from verify_download import ROOT, load_record


def https(url):
    parts = urllib.parse.urlsplit(url)
    if (parts.scheme != 'https' or not parts.hostname or parts.username or parts.password
            or parts.fragment or any(ord(c) <= 32 for c in url)):
        raise ValueError('Expected a public HTTPS download URL')
    return url


class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self, limit=5):
        self.limit, self.count = limit, 0
    def redirect_request(self, request, response, code, message, headers, target):
        self.count += 1
        if self.count > self.limit or request.get_method() != 'GET':
            raise ValueError('Unexpected download redirect')
        return urllib.request.Request(https(urllib.parse.urljoin(request.full_url, target)),
                                      headers={'User-Agent': 'FootistaReleaseCheck/1'})


def response(url, redirects=5):
    request = urllib.request.Request(https(url), headers={'User-Agent': 'FootistaReleaseCheck/1'})
    return urllib.request.build_opener(Redirects(redirects)).open(request, timeout=60)


def small(url, limit=1024 * 1024, redirects=0):
    with response(url, redirects) as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError('Release metadata exceeded its size limit')
    return data


def check_bytes(data, expected):
    if len(data) != expected['bytes'] or hashlib.sha256(data).hexdigest() != expected['sha256']:
        raise ValueError('Published asset differs from the reviewed size or SHA-256')


def download(url, target, expected):
    count, digest = 0, hashlib.sha256()
    with response(url) as source, target.open('xb') as output:
        while chunk := source.read(1024 * 1024):
            count += len(chunk)
            if count > expected['bytes']:
                raise ValueError('Download exceeds the reviewed size')
            digest.update(chunk)
            output.write(chunk)
    if count != expected['bytes'] or digest.hexdigest() != expected['sha256']:
        raise ValueError('Download differs from the reviewed bytes')


def run(version):
    record = load_record(version)
    if record['status'] not in ('prerelease', 'released'):
        raise ValueError('This version is not recorded as a public release')
    public_key = (ROOT / 'releases/public-key.ed25519').read_bytes()
    if len(public_key) != 32 or hashlib.sha256(public_key).hexdigest() != record['public_key_sha256']:
        raise ValueError('Repository publisher fingerprint differs')
    base = 'https://wccf.online/downloads/footista/' + version + '/'
    raw = small(base + 'release.json')
    check_bytes(raw, record['assets']['release.json'])
    check_bytes(small('https://wccf.online/downloads/footista/latest.json'), record['assets']['release.json'])
    envelope = json.loads(raw)
    canonical = json.dumps(envelope['payload'], ensure_ascii=False, sort_keys=True,
                           separators=(',', ':'), allow_nan=False).encode('utf-8')
    Ed25519PublicKey.from_public_bytes(public_key).verify(base64.b64decode(envelope['signature'], validate=True), canonical)
    payload = envelope['payload']
    if payload['version'] != version or payload['sequence'] != record['sequence']:
        raise ValueError('Signed version and public record differ')
    metadata = json.loads(small(base + 'download.json'))
    github = 'https://github.com/Forza-WCCF/FOOTISTA-2019/releases/download/v' + version + '/'
    if (metadata['version'] != version or metadata['url'] != github + 'installer.zip'
            or metadata['archive_url'] != github + 'client.zip'
            or metadata['bytes'] != record['assets']['installer.zip']['bytes']
            or metadata['sha256'] != record['assets']['installer.zip']['sha256']):
        raise ValueError('Website download links differ from this release')
    if payload['archive_url'] != 'https://wccf.online/misc.php?action=wccf_client_archive&version=' + version:
        raise ValueError('Unexpected signed archive broker')
    check_bytes(small(github + 'release.json', redirects=5), record['assets']['release.json'])
    sums = small(github + 'SHA256SUMS.txt', redirects=5).decode('ascii')
    expected_sums = ''.join(record['assets'][name]['sha256'] + '  ' + name + '\n'
                            for name in ('installer.zip', 'client.zip', 'release.json'))
    if sums.splitlines() != expected_sums.splitlines():
        raise ValueError('Published checksum file differs')
    with tempfile.TemporaryDirectory(prefix='footista-release-download-') as temporary:
        root = Path(temporary)
        installer = root / 'installer.zip'
        download(metadata['url'], installer, record['assets']['installer.zip'])
        bootstrap = root / 'bootstrap'
        bootstrap.mkdir()
        inventory = {row['path']: row for row in payload['files']}
        with zipfile.ZipFile(installer) as package:
            names = package.namelist()
            if len(names) != len({n.casefold() for n in names}) or any('/' in n or '\\' in n or ':' in n for n in names):
                raise ValueError('Unexpected installer layout')
            if package.read('trusted-public-key.bin') != public_key or package.read('release.json') != raw:
                raise ValueError('Bootstrap trust or metadata differs')
            with package.open('client.zip') as nested:
                if hashlib.file_digest(nested, 'sha256').hexdigest() != record['assets']['client.zip']['sha256']:
                    raise ValueError('Bundled client differs')
            for name in names:
                if name in ('client.zip', 'release.json', 'trusted-public-key.bin'):
                    continue
                data = package.read(name)
                check_bytes(data, inventory['client/' + name])
                if name.endswith('.py'):
                    (bootstrap / name).write_bytes(data)
        # Use the exact signed production downloader, including its broker,
        # redirect, size and checksum policy. No signup or native launch occurs.
        sys.path.insert(0, str(bootstrap))
        from footista_client import fetch_archive
        from release import extract_archive
        archive = root / 'client.zip'
        fetch_archive(payload['archive_url'], archive, payload)
        extract_archive(archive, root / 'verified-client', payload)
        with zipfile.ZipFile(archive) as package:
            if any(n.endswith('WCCF-WindowsNoEditor.pak') or n.endswith('WCCF-Win64-Shipping.exe') for n in package.namelist()):
                raise ValueError('Original game file in client archive')
    print(json.dumps({'version': version, 'website_latest_verified': True, 'installer_verified': True,
                      'production_update_download_verified': True, 'signed_files_verified': len(payload['files']),
                      'temporary_inputs_removed': not Path(temporary).exists(), 'native_game_downloaded': False,
                      'account_or_gameplay_requests_sent': False}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    run(parser.parse_args().version)
