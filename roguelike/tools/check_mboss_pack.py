#!/usr/bin/env python3
"""Static checks for the mid-boss framework and its boss modules (run after the generators).

    python3 tools/check_mboss_pack.py

- every enabled registry entry has a module F:<fn root>/ (mboss_lib.fn_root: mboss/<id>, or boss/<id> for a chapter
  boss with "fn") with every contract hook (mboss_lib.HOOKS + HELP_HOOKS);
  macro hooks are macro functions, the others are not
- every generated dispatcher F:mboss/d/<hook> calls existing module functions
- every literal "function rlk:..." reference in F:mboss/**, the chapter-boss roots F:boss/<id>/** and the test aliases
  F:boss/test/** resolves; $(...) suffixed references
  (hz/p/c|r|b, pj/h) have their whole numeric family present
- '$' lines carry $(...) and $(...) appears only in '$' lines
- registry ids/numbers are unique and the arena constants agree with the generated arena
- chapter mode (AZ-CM, scratchpad az/contract/cm.md 15.4): every enabled chapter boss has the 17 hooks + prep (not a
  macro); the creg / cbyid lines of F:mboss/register match the registry's enabled chapter entries; every arenas{}
  entry has F:mboss/arena/<aid>/ensure with its stamp string ("<aid>@<ver>:<looks[0]>", or the stub "<aid>@0:stub" when
  its theme module is missing) and the full F:mboss/ar/<aid>/* set; no $(var) inside a function path (dynamic
  references only as a numeric suffix family, which must be contiguous); every proxy key file
  F:mboss/px/<id>/k/<clip>/<t> is reached by its clip's dispatch tree (no orphan from an older manifest); every
  function path under F:mboss, the boss/<id> roots, F:boss/test and F:room/cboss is a valid lower-case resource location
- special bosses (Tachy S1, scratchpad tk/PLAN.md §7-8): every enabled special has the 17 hooks + test/help (+
  mboss_lib.SPECIAL_HOOKS), the sreg / sbyid lines of F:mboss/register and #spN / #spRoll match the enabled special entries,
  each one has its F:mboss/sp/pp/<id>, sp/g/<id> and cb/inc/<id> (incoming through the floor) and every dispatcher
  F:mboss/d/<hook> names it; the frozen runtime names of contract §3.1 exist; the rift F:room/rift/** + room/obj/k_rift
  follow the same reference / macro / resource-location rules, and every shared hook line of tools/build_rift.py is in
  its file exactly once, right after the marker comment
- 아를레키노 S1 (scratchpad ar/contract.md 3.1): the FN-1 Bond-of-Life option (mboss_lib.hz_opts / pj_opts take bol; the
  branch lines of mboss/hurt, hz/init, pj/launch, hz/hurt_pm and the hurt_bol / hz/hurt_pm_bol / hz/init_bol /
  pj/init_bol bodies; the objective mbBol; cleanup_fight's reset; no FN-1 name is ever set outright in F:mboss); a px:false
  chapter boss has no F:mboss/px/<id> tree; the arlecchino entry: its arena = api.ARENA_SPEC, no Pyro resistance
  (res {"*": 10}), px false + shield true, a music pool's len = mboss_lib.music_len
- 홍련 S1 (scratchpad hr/contract.md 3.1): an enabled special that sets an optional hook flag
  (mboss_lib.SPECIAL_OPT_HOOKS: rwHook -> reward) has that hook (not a macro), and F:mboss/sp/reward holds exactly those
  entries' literal hook lines (mboss_lib.special_hook_line) between the sp/lvup line and #spPk (FN-b); the guarded 처치 /
  winWord title lines (FN-a), test/swon's winWord line and the new test/swon_msg_w; death_finish's poof only unless
  cur{poof:0b} (FN-c); the records carry winWord / poof:0b exactly where the registry sets them; FN-f: the wrappers
  mboss/bars_off / bars_on are exactly "flag + bars_hide / bars_show", world skips mboss/bars while #mbBarOff is 1,
  fight_vars and cleanup_fight clear it, start_go's closing bars_show is skipped while it is 1 (홍련 F-I, f2-8: a spawn
  hook's bars(0) holds), no other F:mboss file touches it (bars_hide / bars_show stay flag-free), and
  mboss_lib.bars(on) returns the one wrapper line
Exit code 1 on any problem.
"""
import re
import sys
import mboss_lib as L

problems = []
REG = L.load_registry()
FN = L.FN
funcs = {p.relative_to(FN).with_suffix('').as_posix() for p in FN.rglob('*.mcfunction')}


def is_macro(rel):
    return any(l.lstrip().startswith('$') for l in (FN / (rel + '.mcfunction')).read_text(encoding='utf-8').split('\n'))


for b in L.enabled_bosses(REG):
    hooks = L.HOOKS + L.HELP_HOOKS + (L.CHAPTER_HOOKS if b.get('kind', 'mid') == 'chapter' else []) \
        + (L.SPECIAL_HOOKS if b.get('kind', 'mid') == 'special' else [])
    # hr FN-b: an optional special hook is required once the entry sets its flag (rwHook -> reward)
    if b.get('kind', 'mid') == 'special':
        hooks = hooks + [h for f, h in L.SPECIAL_OPT_HOOKS.items() if b.get(f)]
    for h in hooks:
        rel = f'{L.fn_root(b)}/{h}'
        if rel not in funcs:
            problems.append(f'{b["id"]}: missing hook {rel}')
            continue
        want_macro = h in L.MACRO_HOOKS
        if want_macro != is_macro(rel):
            problems.append(f'{rel}: should {"" if want_macro else "not "}be a macro function')
for h in L.HOOKS + [h.replace('/', '_') for h in L.HELP_HOOKS]:
    rel = f'mboss/d/{h}'
    if rel not in funcs:
        problems.append(f'missing dispatcher {rel}')
# every tree the framework and its modules generate: F:mboss/**, each module root outside it (boss/<id>), the aliases
ROOTS = ['mboss'] + sorted({L.fn_root(b) for b in REG['boss'] if not L.fn_root(b).startswith('mboss/')}) + ['boss/test']
# the rift (Tachy S1, tools/build_rift.py): its tree and its hover object
ROOTS += ['room/rift']
SCAN = [p for r in ROOTS if (FN / r).exists() for p in sorted((FN / r).rglob('*.mcfunction'))]
SCAN += [FN / 'room/obj/k_rift.mcfunction'] if (FN / 'room/obj/k_rift.mcfunction').exists() else []
for p in SCAN:
    rel = p.relative_to(FN).with_suffix('').as_posix()
    for i, line in enumerate(p.read_text(encoding='utf-8').split('\n'), 1):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        if s.startswith('$') and '$(' not in s:
            problems.append(f'{rel}:{i} $ line without $(...)')
        if not s.startswith('$') and '$(' in s:
            problems.append(f'{rel}:{i} $(...) in a non-macro line')
        for m in re.finditer(r'function (rlk:[a-z0-9_./-]+)(\$\(\w+\))?', s):
            ref = m.group(1)[4:]
            if m.group(2):
                fam = [f for f in funcs if f.startswith(ref) and f[len(ref):].isdigit()]
                if not fam:
                    problems.append(f'{rel}:{i} no functions for dynamic reference {m.group(0)}')
                else:
                    nums = sorted(int(f[len(ref):]) for f in fam)
                    if nums != list(range(nums[0], nums[-1] + 1)):
                        problems.append(f'{rel}:{i} gaps in {ref}<n>: {nums[0]}..{nums[-1]}')
            elif ref not in funcs:
                problems.append(f'{rel}:{i} missing function rlk:{ref}')
# ranges the runtime clamps to
for fam, lo, hi in (('mboss/hz/p/c/', 1, 60), ('mboss/hz/p/r/', 1, 90), ('mboss/hz/p/b/', 1, 40), ('mboss/pj/h/', 1, 40)):
    missing = [n for n in range(lo, hi + 1) if f'{fam}{n}' not in funcs]
    if missing:
        problems.append(f'{fam}: missing {missing[:5]}...')
# chapter mode
reg_txt = (FN / 'mboss/register.mcfunction').read_text(encoding='utf-8') if (FN / 'mboss/register.mcfunction').exists() else ''
chaps = L.chapter_bosses(REG)
m = re.search(r'^data modify storage rlk:mboss creg set value \[(.*)\]$', reg_txt, re.M)
ids = re.findall(r'(?:^|\},)\{id:"([^"]+)"', m.group(1)) if m and m.group(1) else []
if sorted(ids) != sorted(b['id'] for b in chaps):
    problems.append(f'register: creg {ids} != enabled chapter entries {[b["id"] for b in chaps]}')
for b in chaps:
    if f'{b["id"]}:{{id:"{b["id"]}",n:{b["n"]},' not in reg_txt:
        problems.append(f'register: cbyid.{b["id"]} missing or stale')
for b in L.mid_bosses(REG):
    if f'id:"{b["id"]}"' in (m.group(1) if m else ''):
        problems.append(f'register: mid-boss {b["id"]} in creg')
AR_FNS = ['marker', 'oob', 'sweep', 'box_absorb', 'ok', 'clamp', 'clamp_step', 'clampw', 'clampw_step', 'leash',
          'full_rim', 'tp_in', 'fl_on', 'fl_off', 'loaded', 'ensure', 'test']
for aid, a in L.arenas(REG):
    for f in AR_FNS:
        if f'mboss/ar/{aid}/{f}' not in funcs:
            problems.append(f'arena {aid}: missing F:mboss/ar/{aid}/{f}')
    if aid == 'plaza':
        continue
    e = FN / f'mboss/arena/{aid}/ensure.mcfunction'
    want = f'{aid}@{a["ver"]}:{a["looks"][0]}' if L.theme_module(a['theme']) else f'{aid}@0:stub'
    if not e.exists() or want not in e.read_text(encoding='utf-8'):
        problems.append(f'arena {aid}: F:mboss/arena/{aid}/ensure missing or without the stamp {want}')
for p in SCAN + sorted((FN / 'room/cboss').rglob('*.mcfunction')):
    rel = p.relative_to(FN).with_suffix('').as_posix()
    for i, line in enumerate(p.read_text(encoding='utf-8').split('\n'), 1):
        if re.search(r'function rlk:[a-z0-9_./-]*\$\(\w+\)[a-z0-9_./-]', line):
            problems.append(f'{rel}:{i} $(var) inside a function path (use literal dispatch lines)')
for b in chaps:
    if not b.get('px'):
        continue
    base = f'mboss/px/{b["id"]}/'
    keys = {f for f in funcs if f.startswith(base + 'k/')}
    reached = set()
    for f in funcs:
        if f.startswith((base + 't/', base + 'c/')):
            reached |= set(re.findall(r'function rlk:(' + re.escape(base) + r'k/\d+/\d+)\b', (FN / (f + '.mcfunction')).read_text(encoding='utf-8')))
    for k in sorted(keys - reached):
        problems.append(f'{k}: proxy key file not reached by its clip dispatch (stale output?)')
for p in SCAN + sorted((FN / 'room/cboss').rglob('*.mcfunction')):
    rel = p.relative_to(FN).with_suffix('').as_posix()
    if not re.fullmatch(r'[a-z0-9_./-]+', rel):
        problems.append(f'{rel}: not a valid function resource location (lower case a-z 0-9 _ . / - only)')
# special bosses (Tachy S1)
specs = L.special_bosses(REG)
m = re.search(r'^data modify storage rlk:mboss sreg set value \[(.*)\]$', reg_txt, re.M)
ids = re.findall(r'(?:^|\},)\{id:"([^"]+)"', m.group(1)) if m and m.group(1) else []
if sorted(ids) != sorted(b['id'] for b in specs):
    problems.append(f'register: sreg {ids} != enabled special entries {[b["id"] for b in specs]}')
for k, v in (('#spN', len(specs)), ('#spRoll', sum(1 for b in specs if b['w'] >= 1))):
    if specs and f'scoreboard players set {k} mb {v}' not in reg_txt:
        problems.append(f'register: {k} mb {v} missing')
for b in specs:
    if f'{b["id"]}:{{id:"{b["id"]}",n:{b["n"]},' not in reg_txt:
        problems.append(f'register: sbyid.{b["id"]} missing or stale')
    for f in (f'mboss/sp/pp/{b["id"]}', f'mboss/sp/g/{b["id"]}', f'mboss/cb/inc/{b["id"]}'):
        if f not in funcs:
            problems.append(f'special {b["id"]}: missing F:{f}')
    for h in L.HOOKS:
        d = FN / f'mboss/d/{h}.mcfunction'
        if d.exists() and f'matches {b["n"]} run' not in d.read_text(encoding='utf-8') and h not in L.ALL_MODULE_HOOKS:
            problems.append(f'special {b["id"]}: dispatcher mboss/d/{h} does not name n {b["n"]}')
    if L.arena_of(b, REG)['aid'] == 'plaza':
        problems.append(f'special {b["id"]}: fights in the plaza (a special needs its own arena)')
for f in ['mboss/sp/' + n for n in ('roll', 'prep', 'gate', 'start_zone', 'start', 'wait', 'ret_rift', 'won', 'won_kill',
                                     'won_cancel', 'clear', 'reward', 'lvup', 'forget', 'run_reset')] \
        + ['mboss/test/' + n for n in ('rift', 'rift_id', 'rift_id_do', 'special', 'special_ch', 'help_special',
                                        'swon_msg_w')] + ['mboss/bars_off', 'mboss/bars_on'] \
        + ['boss/test/' + n for n in ('rift', 'rift_id', 'special', 'special_ch')] \
        + ['room/rift/' + n for n in ('init', 'roll', 'arm', 'show', 'open', 'reopen', 'close', 'tick', 'enter', 'click',
                                       'forget', 'uninstall')] + ['room/obj/k_rift']:
    if f not in funcs:
        problems.append(f'missing frozen runtime name F:{f} (contract 3.1)')
try:
    import build_rift as BR
    for rel, _mode, _anchor, line in BR.HOOKS:
        lines = (FN / (rel + '.mcfunction')).read_text(encoding='utf-8').split('\n')
        at = [i for i, x in enumerate(lines) if x == line]
        if len(at) != 1 or at[0] == 0 or lines[at[0] - 1] != BR.MARK:
            problems.append(f'{rel}: rift hook line missing, doubled or unmarked: {line}')
        for ref in re.findall(r'function (rlk:[a-z0-9_./-]+)', line):
            if ref[4:] not in funcs:
                problems.append(f'{rel}: rift hook line names a missing function {ref}')
except ImportError as e:
    problems.append(f'tools/build_rift.py not importable: {e}')
# 아를레키노 S1: FN-1 (the Bond-of-Life hazard option) and the chapter-4 entry
import inspect  # noqa: E402
for h in ('hz_opts', 'pj_opts'):
    if 'bol' not in inspect.signature(getattr(L, h)).parameters:
        problems.append(f'mboss_lib.{h}: no bol option (FN-1)')
FN1_LINES = {
    'mboss/hurt': 'execute if score @s mbBol matches 1.. run return run function rlk:mboss/hurt_bol',
    'mboss/hz/init': 'execute if score #hzBol mb matches 1.. run function rlk:mboss/hz/init_bol',
    'mboss/pj/launch': 'execute if score #pjBol mb matches 1.. run function rlk:mboss/pj/init_bol',
    'mboss/hz/hurt_pm': 'execute if score @s mbBol matches 1.. run return run function rlk:mboss/hz/hurt_pm_bol',
    'mboss/hurt_bol': 'execute if score #dodged tmp matches 0 run scoreboard players operation #mbHitBol mb = #mbBolIn mb',
    'mboss/hz/hurt_pm_bol': 'scoreboard players operation #mbHitBol mb = #mbBolIn mb',
    'mboss/hz/init_bol': 'scoreboard players reset #hzBol mb',
    'mboss/pj/init_bol': 'scoreboard players reset #pjBol mb',
    'mboss/cleanup_fight': 'execute if score #mbBolRe mb matches -2147483648.. run scoreboard players set #mbBolRe mb 100',
    'mboss/init': 'scoreboard objectives add mbBol dummy',
}
for rel, line in FN1_LINES.items():
    if rel not in funcs or line not in (FN / (rel + '.mcfunction')).read_text(encoding='utf-8').split('\n'):
        problems.append(f'F:{rel}: FN-1 line missing: {line}')
for p in sorted((FN / 'mboss').rglob('*.mcfunction')):
    for i, line in enumerate(p.read_text(encoding='utf-8').split('\n'), 1):
        if re.search(r'scoreboard players (set|add|remove) (#hzBol|#pjBol|#mbBolIn|#mbHitBol) ', line):
            problems.append(f'{p.relative_to(FN).with_suffix("").as_posix()}:{i} sets an FN-1 one-shot name outright (mid-boss fights '
                            'must carry none; only the bol branches copy / reset them)')
for b in chaps:
    if not b.get('px') and any(f.startswith(f'mboss/px/{b["id"]}/') for f in funcs):
        problems.append(f'{b["id"]}: px false but a F:mboss/px/{b["id"]}/ tree exists (stale proxy output)')
KN = next((b for b in REG['boss'] if b['id'] == 'arlecchino'), None)
if KN is not None:
    ka = REG.get('arenas', {}).get(KN.get('arena', 'plaza'))
    try:
        import mboss_arlecchino.api as KN_API
        spec = KN_API.ARENA_SPEC
    except ImportError as e:
        spec = None
        problems.append(f'tools/mboss_arlecchino/api.py not importable: {e}')
    if ka is None:
        problems.append(f'arlecchino: arena {KN.get("arena")} missing from arenas{{}}')
    elif spec is not None and any(ka.get(k) != v for k, v in spec.items()):
        problems.append(f'arlecchino: arenas.{KN["arena"]} differs from api.ARENA_SPEC')
    if KN.get('res') != {'*': 10}:
        problems.append('arlecchino: res must be {"*": 10} (no Pyro resistance, user request)')
    if KN.get('px') or not KN.get('shield'):
        problems.append('arlecchino: px false + shield true (one humanoid body, FN-3)')
    for ph, mu in KN.get('music', {}).items():
        if len(L.MUSIC_TRACKS.get(mu['ev'], [])) > 1 and int(mu['len']) != L.music_len(mu['ev']):
            problems.append(f'arlecchino: music {ph} {mu["ev"]} len {mu["len"]} != music_len {L.music_len(mu["ev"])}')
# hr S1 (scratchpad hr/contract.md 3.1): FN-a the reward word, FN-b the optional reward hook, FN-c no poof, FN-f the
# module's bars-off flag
def _fn_lines(rel):
    p = FN / (rel + '.mcfunction')
    return p.read_text(encoding='utf-8').split('\n') if p.exists() else []


def _record(txt, b):
    """The SNBT record of entry b in F:mboss/register (balanced braces from '{id:"<id>",n:<n>,'), or ''."""
    i = txt.find(f'{{id:"{b["id"]}",n:{b["n"]},')
    if i < 0:
        return ''
    depth, q = 0, False
    for j in range(i, len(txt)):
        c = txt[j]
        if q:
            q = not (c == '"' and txt[j - 1] != '\\')
        elif c == '"':
            q = True
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return txt[i:j + 1]
    return ''


HR_FN_LINES = {
    'mboss/sp/reward': [
        'execute unless data storage rlk:mboss cur.winWord run title @a[tag=player] title [{nbt:"cur.title",storage:"rlk:mboss",interpret:true},{text:" 처치",color:"#FFE08A",bold:true}]',
        'execute if data storage rlk:mboss cur.winWord run title @a[tag=player] title [{nbt:"cur.title",storage:"rlk:mboss",interpret:true},{text:" "},{nbt:"cur.winWord",storage:"rlk:mboss",color:"#FFE08A",bold:true}]'],
    'mboss/test/swon': ['execute if score #mbKilled mb matches 1 if data storage rlk:mboss cur.winWord run return run function rlk:mboss/test/swon_msg_w with storage rlk:mboss tlast'],
    'mboss/death_finish': ['execute unless data storage rlk:mboss cur{poof:0b} at @s run particle minecraft:poof ~ ~1 ~ 0.6 1 0.6 0.02 30 force @a[tag=player]', 'kill @s'],
    'mboss/world': ['execute if score #mbSt mb matches 0..1 unless score #mbBarOff mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/bars'],
    'mboss/fight_vars': ['scoreboard players set #mbBarOff mb 0'],
    'mboss/cleanup_fight': ['scoreboard players set #mbBarOff mb 0'],
    'mboss/bars_off': ['scoreboard players set #mbBarOff mb 1', 'function rlk:mboss/bars_hide'],
    'mboss/bars_on': ['scoreboard players set #mbBarOff mb 0', 'function rlk:mboss/bars_show'],
    # 홍련 F-I (f2-8): the framework's start shows the bars only while the spawn hook left them on (her spawn hook's bars(0))
    'mboss/start_go': ['execute unless score #mbBarOff mb matches 1 run function rlk:mboss/bars_show'],
}
for rel, want in HR_FN_LINES.items():
    have = _fn_lines(rel)
    for line in want:
        if have.count(line) != 1:
            problems.append(f'F:{rel}: hr FN line missing or doubled: {line[:110]}')
for rel in ('mboss/bars_off', 'mboss/bars_on'):
    cmds = [x for x in _fn_lines(rel) if x.strip() and not x.startswith('#')]
    if cmds != HR_FN_LINES[rel]:
        problems.append(f'F:{rel}: must be exactly {HR_FN_LINES[rel]} (hr FN-f)')
# FN-f: only the two wrappers set the flag on / off mid-fight (fight_vars / cleanup_fight clear it; world and start_go read it,
# their pinned lines above); bars_hide / bars_show, which every death / pause / cleanup path calls, never touch it
for p in sorted((FN / 'mboss').rglob('*.mcfunction')):
    rel = p.relative_to(FN).with_suffix('').as_posix()
    for i, line in enumerate(p.read_text(encoding='utf-8').split('\n'), 1):
        if re.search(r'#mbBarOff mb', line) and not line.startswith('#') and rel not in (
                'mboss/bars_off', 'mboss/bars_on', 'mboss/fight_vars', 'mboss/cleanup_fight', 'mboss/world', 'mboss/start_go'):
            problems.append(f'{rel}:{i} touches #mbBarOff (only bars_off / bars_on / fight_vars / cleanup_fight / world / '
                            'start_go may)')
        elif rel == 'mboss/start_go' and re.search(r'#mbBarOff mb', line) and not line.startswith('#') \
                and line != HR_FN_LINES['mboss/start_go'][0]:
            problems.append(f'{rel}:{i} touches #mbBarOff other than its pinned guard line (hr FN-f, F-I f2-8)')
if tuple(L.bars(i) for i in (0, 1)) != ('function rlk:mboss/bars_off', 'function rlk:mboss/bars_on'):
    problems.append('mboss_lib.bars(on) must return the one line function rlk:mboss/bars_off / bars_on (hr FN-f)')
# FN-b: the reward hook lines of mboss/sp/reward = exactly the enabled specials with a flag, after sp/lvup, before #spPk
rl = _fn_lines('mboss/sp/reward')
want = [L.special_hook_line(b, f) for b in specs for f in L.SPECIAL_OPT_HOOKS if b.get(f)]
try:
    i_lv = next(i for i, x in enumerate(rl) if x.endswith(' run function rlk:mboss/sp/lvup'))
    i_c = rl.index('# hr FN-b: per-special reward hooks (registry rwHook)')
    i_pk = next(i for i, x in enumerate(rl) if x.startswith('execute store result score #spPk mb '))
    if not i_lv < i_c < i_pk or rl[i_c + 1:i_pk] != want:
        problems.append(f'F:mboss/sp/reward: the hook lines after sp/lvup and before #spPk are {rl[i_c + 1:i_pk]}, want {want}')
except (ValueError, StopIteration):
    problems.append('F:mboss/sp/reward: sp/lvup line, the "# hr FN-b" comment or the #spPk line missing')
# FN-a / FN-c: the record fields exactly where the registry sets them
for b in L.enabled_bosses(REG):
    rec = _record(reg_txt, b)
    if not rec:
        continue
    ww = b.get('winWord')
    if ('winWord:' in rec) != (ww is not None) or (ww is not None and f'winWord:{L.snbt_str(ww)}' not in rec):
        problems.append(f'register: {b["id"]} record winWord does not match the registry ({ww!r})')
    if ('poof:0b' in rec) != (b.get('poof') is False):
        problems.append(f'register: {b["id"]} record poof:0b does not match the registry (poof {b.get("poof")!r})')
A = REG['arena']
ens = (FN / 'mboss/arena/ensure.mcfunction')
if not ens.exists() or f'{A["theme"]}@{A["ver"]}' not in ens.read_text(encoding='utf-8'):
    problems.append('arena/ensure is missing or stale: run tools/build_mboss_arena.py')
for p in problems:
    print('PROBLEM', p)
print(f'check_mboss_pack: {len(L.mid_bosses(REG))} enabled mid-boss module(s), {len(chaps)} chapter boss module(s), '
      f'{len(specs)} special boss module(s), {len(L.arenas(REG))} arena(s), {len(problems)} problem(s).')
sys.exit(1 if problems else 0)
