"""Clean-install test for a release bundle: unpack it into an empty mods folder layout and check that what the game would mount is whole.

    python clean_install_test.py <bundle.zip>      exit 0 when nothing is wrong; every problem is listed
    python clean_install_test.py --selftest

No game is needed. What it does, in the order the game's loading goes:
  1. the bundle is unpacked into a fresh folder (<tmp>/current/mods) and each inner zip is opened as the game would mount it;
  2. every mod has mod_info/<id>/info.json with a title and a version, and every "requires" of every mod is met by the mods in the bundle
     (the same rule as ww_versions.lua, which each zip carries);
  3. every mod's scripts/*/modScript.lua loads extensions: each one must be a file in the mounted file system (sl_career -> lua/ge/extensions/sl/career.lua);
  4. every Lua file parses (LuaJIT, the game's Lua) and every require('sl/...') / require('slrr/...') / require('ww_...') names a file that is there;
  5. every UI module folder (ui/modModules/<name>/) has its <name>.js, and the files parse (node --check);
  6. nothing that must not be there is there (the bundle's must_not_contain), and the part pictures' manifest and files agree.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

OURS = ('sl/', 'slrr/', 'slrr', 'ww_')          # our own require prefixes; the game's own modules are not checked
EXT_ROOT = 'lua/ge/extensions/'


def parse_version(v):
    return [int(n) for n in re.findall(r'\d+', str(v or ''))]


def older(a, b):
    x, y = parse_version(a), parse_version(b)
    for i in range(max(len(x), len(y))):
        if (x[i] if i < len(x) else 0) != (y[i] if i < len(y) else 0):
            return (x[i] if i < len(x) else 0) < (y[i] if i < len(y) else 0)
    return False


def extension_file(name, have):
    """an extension's name to its file: a_b -> a/b.lua, else a_b.lua (the game's naming)"""
    if '_' in name:
        folder, rest = name.split('_', 1)
        cands = [f'{EXT_ROOT}{folder}/{rest}.lua', f'{EXT_ROOT}{folder}/{rest.replace("_", "/")}.lua', f'{EXT_ROOT}{name}.lua']
    else:
        cands = [f'{EXT_ROOT}{name}.lua']
    return next((c for c in cands if c in have), None)


def check_mounted(zips, must_not_contain=(), lua_parse=True):
    """zips: { name: path }. Returns a list of problems."""
    problems = []
    files = {}              # path in the mounted fs -> (zip name, ZipFile)
    infos = {}
    for zname, zpath in zips.items():
        z = zipfile.ZipFile(zpath)
        bad = z.testzip()
        if bad:
            problems.append(f'{zname}: damaged entry {bad}')
        for n in z.namelist():
            if not n.endswith('/'):
                files[n] = (zname, z)
        for n in z.namelist():
            m = re.match(r'mod_info/([^/]+)/info\.json$', n)
            if m:
                try:
                    infos[m.group(1)] = json.loads(z.read(n).decode('utf-8-sig'))
                except ValueError as e:
                    problems.append(f'{zname}: {n} is not JSON ({e})')
    # 2. versions and requires
    for zname, zpath in zips.items():
        zi = [i for i in infos if any(n == f'mod_info/{i}/info.json' for n in zipfile.ZipFile(zpath).namelist())]
        if not zi:
            problems.append(f'{zname}: no mod_info/<id>/info.json')
    for mid, info in infos.items():
        if not info.get('title') or not info.get('version'):
            problems.append(f'{mid}: info.json needs a title and a version')
        for need, minimum in (info.get('requires') or {}).items():
            have = infos.get(need)
            if not have:
                problems.append(f'{mid} needs {need} {minimum}, which is not in the bundle')
            elif older(have.get('version'), minimum):
                problems.append(f'{mid} needs {need} {minimum} or newer; the bundle has {have.get("version")}')
    # 3. modScript extension lists
    for path, (zname, z) in sorted(files.items()):
        if re.match(r'scripts/[^/]+/modScript\.lua$', path):
            text = z.read(path).decode('utf-8', 'replace')
            names = set(re.findall(r"'([A-Za-z]+_[A-Za-z0-9_]+)'", text)) | set(re.findall(r"extensions\.load\('([A-Za-z0-9_]+)'\)", text))
            for name in sorted(names):
                if not extension_file(name, files):
                    problems.append(f'{path} ({zname}): loads extension {name}, but its file is not in the mods')
    # 4. Lua parses; requires resolve
    runtime = None
    if lua_parse:
        try:
            from lupa.luajit21 import LuaRuntime
            runtime = LuaRuntime().eval('loadstring')
        except ImportError:
            problems.append('lupa is not installed: the Lua parse step was skipped')
    for path, (zname, z) in sorted(files.items()):
        if not path.endswith('.lua'):
            continue
        text = z.read(path).decode('utf-8', 'replace').lstrip('﻿')
        if runtime:
            res = runtime(text)
            if isinstance(res, tuple):
                problems.append(f'{path} ({zname}): does not parse: {res[1]}')
                continue
        for req in re.findall(r"""require\(\s*['"]([^'"]+)['"]\s*\)""", text):
            if req.startswith(OURS):
                if f'{EXT_ROOT}{req}.lua' not in files and f'lua/{req}.lua' not in files:
                    problems.append(f'{path} ({zname}): require("{req}") has no file in the mods')
    # 5. UI modules
    mods = {m.group(1) for p in files for m in [re.match(r'ui/modModules/([^/]+)/', p)] if m}
    for name in sorted(mods):
        if f'ui/modModules/{name}/{name}.js' not in files:
            problems.append(f'ui/modModules/{name}: no {name}.js')
    node = shutil.which('node')
    if node:
        for path, (zname, z) in sorted(files.items()):
            if path.endswith('.js') and path.startswith('ui/modModules/'):
                with tempfile.NamedTemporaryFile('wb', suffix='.js', delete=False) as t:
                    t.write(z.read(path))
                r = subprocess.run([node, '--check', t.name], capture_output=True, text=True)
                os.unlink(t.name)
                if r.returncode != 0:
                    line = (r.stderr.strip().splitlines() or ['?'])[-1]
                    problems.append(f'{path} ({zname}): does not parse: {line}')
    # 6. forbidden files; the part pictures
    for bad in must_not_contain:
        hit = next((p for p in files if p.startswith(bad)), None)
        if hit:
            problems.append(f'{hit} must not be in this bundle (rule: {bad})')
    manifest = 'art/street_legal/parts/manifest.json'
    if manifest in files:
        z = files[manifest][1]
        try:
            listed = json.loads(z.read(manifest).decode('utf-8'))
        except ValueError:
            problems.append(f'{manifest} is not JSON')
            listed = {}
        for part in listed.get('parts', []):
            if f'art/street_legal/parts/{part}.png' not in files:
                problems.append(f'{manifest}: the picture of {part} is missing')
        for part, canon in (listed.get('alias') or {}).items():
            if f'art/street_legal/parts/{canon}.png' not in files:
                problems.append(f'{manifest}: {part} shares the picture of {canon}, which is missing')
    elif any(p.startswith('lua/ge/extensions/sl/') for p in files):
        problems.append('no part pictures manifest (art/street_legal/parts/manifest.json): ship the pictures first')
    return problems


def check_bundle(bundle, must_not_contain=()):
    problems = []
    with tempfile.TemporaryDirectory() as tmp:
        mods = os.path.join(tmp, 'current', 'mods')
        os.makedirs(mods)                       # an empty mods folder, as on a clean machine
        with zipfile.ZipFile(bundle) as z:
            z.extractall(mods)
        info = os.path.join(mods, 'bundle.json')
        manifest = json.load(open(info, encoding='utf-8')) if os.path.isfile(info) else {}
        if not manifest:
            problems.append('bundle.json is missing')
        zips = {}
        for name, entry in (manifest.get('mods') or {}).items():
            path = os.path.join(mods, entry['zip'])
            if not os.path.isfile(path):
                problems.append(f'{entry["zip"]} is listed in bundle.json but not in the bundle')
                continue
            if hashlib.sha256(open(path, 'rb').read()).hexdigest() != entry.get('sha256'):
                problems.append(f'{entry["zip"]}: the checksum does not match bundle.json')
            zips[name] = path
        stray = [f for f in os.listdir(mods) if f.endswith('.zip') and f not in {e['zip'] for e in (manifest.get('mods') or {}).values()}]
        for f in stray:
            problems.append(f'{f} is in the bundle but not in bundle.json')
        for need in ('INSTALL.txt',):
            if not os.path.isfile(os.path.join(mods, need)):
                problems.append(f'{need} is missing')
        problems += check_mounted(zips, must_not_contain)
    return problems


def selftest():
    with tempfile.TemporaryDirectory() as tmp:
        def make(name, files):
            p = os.path.join(tmp, name)
            with zipfile.ZipFile(p, 'w') as z:
                for k, v in files.items():
                    z.writestr(k, v)
            return p
        good = make('a.zip', {'mod_info/a/info.json': json.dumps({'title': 'A', 'version': '1.2.0', 'requires': {'b': '1.0'}}),
                              'scripts/a/modScript.lua': "for _, name in ipairs({ 'a_main' }) do\n  extensions.load(name)\nend\nextensions.load('a_main')",
                              'lua/ge/extensions/a/main.lua': "local x = require('a/helper')\nreturn x", 'lua/ge/extensions/a/helper.lua': 'return 1'})
        b = make('b.zip', {'mod_info/b/info.json': json.dumps({'title': 'B', 'version': '1.1.0'})})
        assert check_mounted({'a': good, 'b': b}, lua_parse=True) == [p for p in check_mounted({'a': good, 'b': b}) if 'part pictures' in p or 'lupa' in p], 'a whole install is clean'
        old = make('old.zip', {'mod_info/b/info.json': json.dumps({'title': 'B', 'version': '0.9.0'})})
        assert any('needs b 1.0 or newer' in p for p in check_mounted({'a': good, 'old': old}))
        assert any('needs b 1.0, which is not in the bundle' in p for p in check_mounted({'a': good}))
        broken = make('x.zip', {'mod_info/x/info.json': json.dumps({'title': 'X', 'version': '1'}), 'lua/ge/extensions/x/y.lua': 'x = = 1',
                                'scripts/x/modScript.lua': "extensions.load('x_missing')", 'ui/modModules/m/other.js': 'x'})
        ps = check_mounted({'x': broken})
        assert any('does not parse' in p for p in ps) or any('lupa' in p for p in ps)
        assert any('x_missing' in p for p in ps) and any('no m.js' in p for p in ps)
        assert any('must not be in this bundle' in p for p in check_mounted({'x': broken}, ['lua/ge/extensions/x/']))
        assert older('1.7.0', '1.10.0') and not older('1.7.0', '1.7') and extension_file('a_b', {EXT_ROOT + 'a/b.lua'}) == EXT_ROOT + 'a/b.lua'
    print('selftest ok')
    return 0


def main():
    if '--selftest' in sys.argv:
        return selftest()
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    if sys.argv[1] == '--single':               # one merged mod zip: python clean_install_test.py --single <mod.zip>
        cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'release.json'), encoding='utf-8'))
        forbidden = next((m.get('must_not_contain', []) for m in cfg.get('merged', []) if os.path.basename(sys.argv[2]) == m['zip']), [])
        problems = check_mounted({'merged': sys.argv[2]}, forbidden)
        print('clean install: %d problem%s' % (len(problems), '' if len(problems) == 1 else 's'))
        for p in problems:
            print('  ' + p)
        return 1 if problems else 0
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'release.json')
    forbidden = []
    if os.path.isfile(cfg_path):
        for b in json.load(open(cfg_path, encoding='utf-8')).get('bundles', []):
            if os.path.basename(sys.argv[1]) == b['zip']:
                forbidden = b.get('must_not_contain', [])
    problems = check_bundle(sys.argv[1], forbidden)
    print('clean install: %d problem%s' % (len(problems), '' if len(problems) == 1 else 's'))
    for p in problems:
        print('  ' + p)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
