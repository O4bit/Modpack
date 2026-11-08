#!/usr/bin/env python3
"""Rebuild Stellar's data-only fix from the pinned MIT-licensed upstream JAR."""
from pathlib import Path
import hashlib
import io
import json
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://cdn.modrinth.com/data/LrtCyjyV/versions/t2CeuuGG/too-expensive-removed-v1.2.3.jar'
SHA512 = '62df9ce0f4aba7fb3e09114bb9d26274c12f38100433d92e7d12a1a85e7f1a58a2b85179d8b0f5fd296ab73ad6dbe2673cffd5e69d3ce9dd7b12401d0ba28b0e'
OUTPUT = ROOT / 'mods/too-expensive-removed-stellar-1.2.3.1.jar'

def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')

def main():
    request = urllib.request.Request(URL, headers={'User-Agent': 'O4bit/Stellar-anvil-fix'})
    with urllib.request.urlopen(request, timeout=30) as response:
        original = response.read()
    assert hashlib.sha512(original).hexdigest() == SHA512, 'Upstream JAR checksum mismatch'
    changes = {
        # Replace the equipment whitelist and timing-sensitive inventory event.
        'data/tooexpensiveremoved/advancement/inventory_changed.json': json_bytes({
            'criteria': {'requirement': {'trigger': 'minecraft:impossible'}}
        }),
        'data/minecraft/tags/function/tick.json': json_bytes({
            'values': ['stellar_anvil_fix:tick']
        }),
        'data/stellar_anvil_fix/function/tick.mcfunction': (
            '# Correct only a nonzero repair-cost component on the cursor stack.\n'
            'execute as @a if items entity @s player.cursor *[minecraft:repair_cost] '
            'unless items entity @s player.cursor *[minecraft:repair_cost=0] '
            'run item modify entity @s player.cursor stellar_anvil_fix:clear_prior_work\n'
        ).encode(),
        'data/stellar_anvil_fix/item_modifier/clear_prior_work.json': json_bytes({
            'function': 'minecraft:set_components',
            'components': {'minecraft:repair_cost': 0}
        }),
        'STELLAR-PATCH.md': (
            '# Stellar anvil compatibility patch\n\n'
            'Based on Too Expensive Removed v1.2.3 by Jodek, under the included MIT license.\n'
            'Upstream: https://modrinth.com/datapack/too-expensive-removed\n\n'
            'Replaces its equipment-only advancement with a cursor check covering every item\n'
            'with a nonzero minecraft:repair_cost component, including enchanted books and\n'
            'modded equipment. Only that component is cleared. Enchantments, affixes, names\n'
            'and durability remain unchanged. Normal enchantment charges still apply.\n'
            'No Java classes or anvil calculation methods are changed.\n'
            'Rebuild: python3 scripts/build_anvil_patch.py in O4bit/Modpack.\n'
        ).encode(),
    }
    with zipfile.ZipFile(io.BytesIO(original)) as source:
        assert 'LICENSE.txt' in source.namelist()
        for name in ['META-INF/neoforge.mods.toml', 'META-INF/mods.toml']:
            text = source.read(name).decode()
            assert "version = '1-v1.2.3'" in text
            changes[name] = text.replace("version = '1-v1.2.3'", "version = '1-v1.2.3-stellar.1'").encode()
        with zipfile.ZipFile(OUTPUT, 'w') as target:
            for entry in source.infolist():
                target.writestr(entry, changes.pop(entry.filename, source.read(entry.filename)))
            for name, data in sorted(changes.items()):
                info = zipfile.ZipInfo(name, date_time=(2026, 11, 8, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                target.writestr(info, data)
    with zipfile.ZipFile(OUTPUT) as result:
        assert result.testzip() is None
    print(f'Built {OUTPUT.name}; upstream license and Java classes preserved.')

if __name__ == '__main__':
    main()
