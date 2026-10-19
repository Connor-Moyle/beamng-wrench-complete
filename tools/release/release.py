"""Build the release zips for every Wrench Works mod, plus one all-in-one bundle.

    python release.py                      build every mod in release.json and the bundle
    python release.py --only a,b           build some mods by id (no bundle)
    python release.py --stage DIR          also lay out a clean BeamNG user folder in DIR for the clean-install test
    python release.py --bundle west_coast  build one named bundle (its mods and the bundle zip), then run the clean-install test on it
    python release.py --selftest           check the exclusion and version logic on a throwaway mod

Every setting (ids, folders, zip names, exclusions, "requires") lives in release.json, so a rename is a config edit.
Each zip gets the shared version check (ww_versions.lua) and its "requires" written into the staged mod_info,
never into the source repo. A mod without a version in its mod_info is refused.
"""
import datetime
import fnmatch
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
STORED = ('.png', '.jpg', '.jpeg', '.ogg', '.zip')  # already compressed
CHECK_LUA = 'lua/ge/extensions/ww_versions.lua'
CHECK_SCRIPT = 'scripts/ww_versions/modScript.lua'
CHECK_SCRIPT_BODY = "extensions.load('ww_versions')\nsetExtensionUnloadMode('ww_versions', 'manual')\n"


def excluded(rel, patterns):
    return any(fnmatch.fnmatch(rel, p) or (p.startswith('**/') and fnmatch.fnmatch(rel, p[3:])) for p in patterns)


def files_of(src, patterns):
    for folder, dirs, files in os.walk(src):
        for f in files:
            full = os.path.join(folder, f)
            rel = os.path.relpath(full, src).replace(os.sep, '/')
            if not excluded(rel, patterns):
                yield full, rel


def export_tag(src, tag, dest):
    """Unpack the folder `src` as it is at git tag `tag` into `dest` (a pinned mod ships the released code, whatever the working tree holds)."""
    top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=src, capture_output=True, text=True, check=True).stdout.strip()
    sub = os.path.relpath(src, top).replace(os.sep, '/')
    zp = os.path.join(dest, 'tag.zip')
    r = subprocess.run(['git', 'archive', '--format=zip', '-o', zp, tag, sub], cwd=top, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"pinned tag {tag} not found in {src}: {r.stderr.strip()}")
    with zipfile.ZipFile(zp) as z:
        z.extractall(dest)
    os.remove(zp)
    return os.path.join(dest, sub)


def build_mod(mod, cfg, out):
    if mod.get('pin'):
        with tempfile.TemporaryDirectory() as tmp:
            return build_mod_from(mod, cfg, out, export_tag(mod['src'], mod['pin'], tmp), True)
    return build_mod_from(mod, cfg, out, mod['src'], False)


def build_mod_from(mod, cfg, out, src, pinned):
    info_path = os.path.join(src, mod['info'])
    if not os.path.isfile(info_path):
        raise SystemExit(f"{mod['id']}: no {mod['info']} in {src} (ask the mod's owner to add one with a version)")
    with open(info_path, encoding='utf-8-sig') as f:
        info = json.load(f)
    if not info.get('version'):
        raise SystemExit(f"{mod['id']}: {mod['info']} has no version")
    dirty = '' if pinned else subprocess.run(['git', 'status', '--porcelain', '--', '.'], cwd=src, capture_output=True, text=True).stdout
    if dirty.strip():
        print(f"WARNING {mod['id']}: uncommitted changes go into the zip:\n{dirty.rstrip()}")
    patterns = cfg['exclude_all'] + mod.get('exclude', [])
    zpath = os.path.join(out, mod['zip'])
    tmp = zpath + '.part'
    count = 0
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for full, rel in files_of(src, patterns):
            if mod.get('versioncheck') and rel == mod['info']:
                continue  # written below with "requires"
            z.write(full, rel, zipfile.ZIP_STORED if rel.lower().endswith(STORED) else zipfile.ZIP_DEFLATED)
            count += 1
        if mod.get('versioncheck'):
            info['requires'] = mod.get('requires', {})
            z.writestr(mod['info'], json.dumps(info, indent=2))
            z.write(os.path.join(HERE, 'ww_versions.lua'), CHECK_LUA)
            z.writestr(CHECK_SCRIPT, CHECK_SCRIPT_BODY)
            count += 3
    os.replace(tmp, zpath)
    if pinned:
        print(f"{mod['id']}: built from tag {mod['pin']}")
    print(f"{mod['zip']}: {info['version']}, {count} files, {os.path.getsize(zpath) / 1e6:.1f} MB")
    return zpath, info['version']


def build_merged(m, cfg, out):
    """ONE mod from several: every member is built as usual (pinned tags, exclusions), then their files go into a single zip with its own
    mod_info. A path two members both ship is a collision: refused, unless the bytes are identical (then it is written once).
    The members' own mod_info and the version check files between them are left out (one mod now)."""
    by = {x['id']: x for x in cfg['mods']}
    unknown = [i for i in m['from'] if i not in by]
    if unknown:
        raise SystemExit(f"{m['id']}: unknown members {unknown}")
    skip = {CHECK_LUA, CHECK_SCRIPT} | {by[i]['info'] for i in m['from']}
    icon_path = f"mod_info/{by[m['icon_from']]['id']}/icon.jpg" if m.get('icon_from') else None
    owner, collisions, counts = {}, [], {}
    with tempfile.TemporaryDirectory() as tmp:
        zips = {}
        for i in m['from']:
            zips[i] = zipfile.ZipFile(build_mod(by[i], cfg, tmp)[0])
        for i in m['from']:
            for e in zips[i].infolist():
                f = e.filename
                if e.is_dir() or f in skip:
                    continue
                if f.startswith('mod_info/'):
                    if not (icon_path and f == icon_path and i == m['icon_from']):
                        continue
                if f in owner:
                    o, oe = owner[f]
                    if (oe.CRC, oe.file_size) != (e.CRC, e.file_size):
                        collisions.append(f"{f}: {o} and {i} differ")
                    continue
                owner[f] = (i, e)
                counts[i] = counts.get(i, 0) + 1
        extras = {}                       # the merged mod's own files (its guard script), from m['extra']; mod_info is generated, not copied
        for full, rel in files_of(m['extra'], cfg['exclude_all']) if m.get('extra') else []:
            if rel.startswith('mod_info/'):
                continue
            if rel in owner:
                collisions.append(f"{rel}: the merged mod's own file and {owner[rel][0]} both ship it")
            extras[rel] = full
        if collisions:
            raise SystemExit(f"{m['id']}: path collisions between the mods:" + chr(10) + chr(10).join(collisions))
        zpath = os.path.join(out, m['zip'])
        with zipfile.ZipFile(zpath + '.part', 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            info = dict(m['info'])
            z.writestr(f"mod_info/{info['name']}/info.json", json.dumps(info, indent=2))
            for rel, full in sorted(extras.items()):
                z.write(full, rel)
            for f, (i, e) in sorted(owner.items()):
                z.writestr(f if f != icon_path else f"mod_info/{info['name']}/icon.jpg", zips[i].read(f),
                           zipfile.ZIP_STORED if f.lower().endswith(STORED) else zipfile.ZIP_DEFLATED)
        for z in zips.values():
            z.close()
    os.replace(zpath + '.part', zpath)
    n = len(owner) + len(extras) + 1
    print(f"{m['zip']}: {info['version']}, {n} files from {counts}, {os.path.getsize(zpath) / 1e6:.1f} MB")
    r = subprocess.run([sys.executable, os.path.join(HERE, 'clean_install_test.py'), '--single', zpath], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode:
        raise SystemExit('clean-install test failed')
    return zpath, n


def build_bundle(cfg, built, out):
    lines = ['Wrench Works: all mods in one download', '',
             'Install: unzip this file and copy the .zip files inside into your BeamNG mods folder',
             '(%LOCALAPPDATA%\\BeamNG\\BeamNG.drive\\current\\mods). Do not unzip the inner zips.', '',
             'What is inside:']
    lines += [f"  {os.path.basename(p)}  {m['title']} {v}" for m, (p, v) in built]
    bpath = os.path.join(out, cfg['bundle'])
    with zipfile.ZipFile(bpath + '.part', 'w', zipfile.ZIP_STORED) as z:
        for _, (p, _) in built:
            z.write(p, os.path.basename(p))
        z.writestr('INSTALL.txt', (chr(13) + chr(10)).join(lines) + chr(13) + chr(10))
    os.replace(bpath + '.part', bpath)
    print(f"{cfg['bundle']}: {os.path.getsize(bpath) / 1e6:.1f} MB")


def build_named_bundle(bcfg, built, out):
    """A named bundle (release.json "bundles"): its mods' zips, bundle.json (each mod's version, checksum and requires), INSTALL.txt and the
    players' READMEs, then the clean-install test on the result. """
    by_id = {m['id']: (m, pv) for m, pv in built}
    missing = [i for i in bcfg['mods'] if i not in by_id]
    if missing:
        raise SystemExit(f"bundle {bcfg['id']}: mods not built: {missing}")
    version = by_id[bcfg['version_from']][1][1]
    manifest = {'title': bcfg['title'], 'version': version, 'built': datetime.date.today().isoformat(), 'mods': {}}
    for i in bcfg['mods']:
        m, (p, v) = by_id[i]
        manifest['mods'][i] = {'zip': os.path.basename(p), 'title': m['title'], 'version': v, 'requires': m.get('requires', {}),
                               'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest()}
    lines = [bcfg['title'] + ' ' + version, '',
             'Install: unzip this file and copy the .zip files inside (not the other files) into your BeamNG mods folder,',
             '%LOCALAPPDATA%' + chr(92) + 'BeamNG' + chr(92) + 'BeamNG.drive' + chr(92) + 'current' + chr(92) + 'mods. Do not unzip the inner zips. Start the game, then Play > Street Legal.', '',
             'What is inside:']
    lines += [f"  {e['zip']}  {e['title']} {e['version']}" + (f"  (needs {', '.join(f'{k} {v}' for k, v in e['requires'].items())})" if e['requires'] else '')
              for e in manifest['mods'].values()]
    lines += ['', 'Each mod checks the versions of the others when a level loads and says so if one is too old or missing.',
              'The README files explain each mod; bundle.json lists the exact versions and checksums.']
    bpath = os.path.join(out, bcfg['zip'])
    with zipfile.ZipFile(bpath + '.part', 'w', zipfile.ZIP_STORED) as z:
        for i in bcfg['mods']:
            z.write(by_id[i][1][0], os.path.basename(by_id[i][1][0]))
            readme = bcfg.get('readmes', {}).get(i)
            if readme and os.path.isfile(readme):
                z.write(readme, f'README_{i}.md')
        z.writestr('bundle.json', json.dumps(manifest, indent=2))
        z.writestr('INSTALL.txt', (chr(13) + chr(10)).join(lines) + chr(13) + chr(10))
    os.replace(bpath + '.part', bpath)
    print(f"{bcfg['zip']}: {version}, {os.path.getsize(bpath) / 1e6:.1f} MB")
    import clean_install_test
    problems = clean_install_test.check_bundle(bpath, bcfg.get('must_not_contain', []))
    print('clean-install test: ' + ('passed' if not problems else f'{len(problems)} problem(s)'))
    for p in problems:
        print('  ' + p)
    if problems:
        raise SystemExit(1)


def stage(built, folder):
    # shortcut: assumes BeamNG uses <userpath>/current/mods like the default user folder; confirm on the first game turn
    mods = os.path.join(folder, 'current', 'mods')
    if os.path.isdir(mods) and os.listdir(mods):
        raise SystemExit(f'{mods} is not empty; the clean-install test needs an empty mods folder')
    os.makedirs(mods, exist_ok=True)
    for _, (p, _) in built:
        shutil.copy2(p, mods)
    print(f'staged {len(built)} zips in {mods}')
    print(f'test: BeamNG.drive.x64.exe -userpath "{folder}" -enablemcp, then load the level; check beamng.log for ww_versions and Lua errors')


def selftest():
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, 'mod')
        for rel, body in [('mod_info/a/info.json', '{"title": "A", "version": "1.2.0"}'), ('lua/x.lua', 'x'),
                          ('graphify-out/g.json', '{}'), ('tools/t.py', ''), ('art/s.wav', ''), ('art/keep.ogg', '')]:
            os.makedirs(os.path.dirname(os.path.join(src, rel)), exist_ok=True)
            with open(os.path.join(src, rel), 'w') as f:
                f.write(body)
        cfg = {'exclude_all': json.load(open(os.path.join(HERE, 'release.json')))['exclude_all']}
        mod = {'id': 'a', 'title': 'A', 'src': src, 'zip': 'a.zip', 'info': 'mod_info/a/info.json',
               'versioncheck': True, 'requires': {'b': '2.0'}, 'exclude': ['art/*.wav']}
        p, v = build_mod(mod, cfg, tmp)
        names = set(zipfile.ZipFile(p).namelist())
        assert v == '1.2.0'
        assert names == {'mod_info/a/info.json', 'lua/x.lua', 'art/keep.ogg', CHECK_LUA, CHECK_SCRIPT}, names
        assert json.loads(zipfile.ZipFile(p).read('mod_info/a/info.json'))['requires'] == {'b': '2.0'}
        with open(os.path.join(src, 'mod_info/a/info.json'), encoding='utf-8') as f:
            assert 'requires' not in json.load(f), 'the source mod_info must stay untouched'
    print('selftest ok')


def main():
    args = sys.argv[1:]
    if '--selftest' in args:
        return selftest()
    with open(os.path.join(HERE, 'release.json'), encoding='utf-8') as f:
        cfg = json.load(f)
    only = args[args.index('--only') + 1].split(',') if '--only' in args else []
    wanted = None
    if '--bundle' in args:
        wanted = next(b for b in cfg.get('bundles', []) if b['id'] == args[args.index('--bundle') + 1])
        only = wanted['mods']
    if '--merged' in args:
        mid = args[args.index('--merged') + 1]
        build_merged(next(x for x in cfg['merged'] if x['id'] == mid), cfg, cfg['out'])
        return
    mods = [m for m in cfg['mods'] if not only or m['id'] in only]
    if only and len(mods) != len(only):
        raise SystemExit(f"unknown id in {only}; known: {[m['id'] for m in cfg['mods']]}")
    os.makedirs(cfg['out'], exist_ok=True)
    built = [(m, build_mod(m, cfg, cfg['out'])) for m in mods]
    if wanted:
        build_named_bundle(wanted, built, cfg['out'])
    elif not only:
        build_bundle(cfg, built, cfg['out'])
        for b in cfg.get('bundles', []):
            build_named_bundle(b, built, cfg['out'])
    if '--stage' in args:
        stage(built, args[args.index('--stage') + 1])


if __name__ == '__main__':
    main()
