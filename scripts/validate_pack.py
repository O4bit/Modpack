#!/usr/bin/env python3
"""Verify all indexed files and download metadata without downloading mods."""
from pathlib import Path
import hashlib
import tomllib
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

def digest(path, algorithm):
    return hashlib.new(algorithm.replace('-', ''), path.read_bytes()).hexdigest()

def validate_download(meta, relative):
    download = meta['download']
    mode = download.get('mode') or 'url'
    if mode == 'metadata:curseforge':
        provider = meta.get('update', {}).get('curseforge', {})
        for key in ('project-id', 'file-id'):
            value = provider.get(key)
            assert type(value) is int and value > 0, f'{relative}: CurseForge {key} must be a positive integer'
    elif mode == 'url':
        url = download.get('url', '')
        assert url, f'{relative}: URL download is missing download.url'
        assert urlsplit(url).scheme == 'https' and urlsplit(url).netloc, f'{relative}: download.url must be an absolute HTTPS URL'
        assert url.isascii() and not any(c.isspace() for c in url), f'{relative}: unescaped download URL'
    else:
        raise ValueError(f'{relative}: unsupported download mode {mode!r}')

def main():
    pack = tomllib.loads((ROOT / 'pack.toml').read_text())
    assert pack['versions'] == {'minecraft': '1.21.1', 'neoforge': '21.1.264'}
    index_path = ROOT / pack['index']['file']
    assert digest(index_path, pack['index']['hash-format']) == pack['index']['hash'], 'Index hash mismatch'
    index = tomllib.loads(index_path.read_text())
    paths = set()
    download_targets = set()
    mods = 0
    for entry in index['files']:
        relative = Path(entry['file'])
        assert not relative.is_absolute() and '..' not in relative.parts
        assert entry['file'] not in paths, f'Duplicate index entry: {relative}'
        paths.add(entry['file'])
        path = ROOT / relative
        assert path.is_file(), f'Missing indexed file: {relative}'
        assert digest(path, entry.get('hash-format', index['hash-format'])) == entry['hash'], relative
        assert relative.parts[0] not in {'saves', 'logs', 'screenshots', 'fancymenu_data', 'xaero', '.bobby'}
        if entry.get('metafile'):
            try:
                meta = tomllib.loads(path.read_text())
            except tomllib.TOMLDecodeError as error:
                raise ValueError(f'{relative}: {error}') from error
            assert meta['side'] in {'client', 'both'}, f'Client pack would skip {relative}'
            validate_download(meta, relative)
            assert '/' not in meta['filename'] and '\\' not in meta['filename']
            destination = relative.parent / meta['filename']
            assert destination not in download_targets, f'Duplicate download target: {destination}'
            download_targets.add(destination)
            if relative.parts[0] == 'mods':
                mods += 1
    assert mods > 0, 'Pack contains no mod descriptors'
    print(f'Validated {len(paths)} indexed files, {mods} mod descriptors, and the pack index hash.')

if __name__ == '__main__':
    main()
