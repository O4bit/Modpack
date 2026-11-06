#!/usr/bin/env python3
"""Publish only pack/index content, excluding tooling and repository internals."""
from pathlib import Path
import shutil
import tomllib
from validate_pack import main as validate

ROOT = Path(__file__).resolve().parents[1]
validate()
target = ROOT / '_site'
if target.exists():
    shutil.rmtree(target)
target.mkdir()
pack = tomllib.loads((ROOT / 'pack.toml').read_text())
index = tomllib.loads((ROOT / pack['index']['file']).read_text())
files = {'pack.toml', pack['index']['file'], 'CNAME'}
files.update(item['file'] for item in index['files'])
for name in sorted(files):
    source = ROOT / name
    if not source.is_file():
        continue
    destination = target / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
(target / '.nojekyll').touch()
print(f'Prepared {len(files)} pack files for GitHub Pages.')
