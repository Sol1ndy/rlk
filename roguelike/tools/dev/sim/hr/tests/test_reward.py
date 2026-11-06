#!/usr/bin/env python3
"""test_reward.py: the event after 홍련's clear, stage S3 (scratchpad hr/PLAN.md §7.1-7.3, §7.6; contract §3.7):
F:boss/scarlet/ev/{roll,apply,item,buff,title,record,reset} and the FN-b reward hook F:boss/scarlet/reward, in the sim on
a variant with her enabled (the core's stand-in ending / event coda; SR's sword_hwamu is not registered on this branch,
so rlk:items/give and rlk:items/drop are recording stubs: give appends to rlk:pinv order, drop puts one ground item
tagged rlk_daura at the executor).

    python3 test_reward.py <datapack root> [section ...]

  flow    the kill -> death_start (the roll) -> the ending 1042 t -> seq/event at H -> the grant at E56 (title) ->
          death_finish at H + 122 = registry death 1164 without a poof -> won -> the return title words -> one level +
          pkPending + 1 -> the hook once as the player -> one box; both branches (tests 91 / 92)
  roll    10 000 seeded rolls 50 +- 1.5 %; item_pm 0 / 1000 (dry builds) -> all buff / all item; forced branches (the
          sword held -> buff, hrMoon -> item, ev.force item / buff first); ev.force and the scores cleared after use
  inv     room -> items/give once, order + 1, the star 1 (rlk:pinv enh.sword_hwamu 1 = ★☆☆); full at invCap 9 and 18 -> no
          give, #hrEvDrop 1, one ground item at the player's body (rlk_body, rlk_daura), one notice; never lost, never
          doubled
  reload  /reload at every tick E0-E120 of the coda and in CS4 -> the outcome exactly once (coda or hook), no rlk_hr_ev
          entity left, the event scores 0 after the hook
  words   every on-screen string of 7.3.3 verbatim (item title / notice, buff title / numbers, the chat records, the
          full notice, the return title words); the coda lines = api.LINES 24 / 25 (kit build: fx/hud/line {id}); no
          other title / chat line of the module during the coda. F3 (HR-33): the item title and the chat record carry the
          item's own star colours (rlk:items stars, read at run time: gold ★, grey ☆); F3 (HR-35): the 4x title <= 106
          font px, the subtitles <= 192 font px (26.3 glyph advances), the buff's third number on the actionbar, held
          for the title's time (VF3-1-01: a coda run with the REAL player/hud/tick each tick: ev/title at E56 leaves
          hudHold = its `times` total 54, the HUD draws nothing and no other actionbar comes E57-E110, the HUD after)
  scope   F3 (HR-11): the buff's numbers (title subtitle / actionbar / rift chat) follow load's constants; the rift chat's
          scope words follow api.EVENT['buff_scope'] (dry build 'forever': 「영구히」 with 8 / 4 / 4)
  F-I: the coda's blank actionbar at its start (F2 round 1, seq.HUD_BLANK) is not counted among the buff's actionbars
  F3 (HR-05) in flow: at the reward hook (after cleanup) objective hr holds only the event scores (their values kept) —
          the other owners' leftovers (#sq_* #g_* #r2_* #a9_*) are gone — and storage rlk:hr has no core / seq
  real    (I1, requests s3-4 / sr-4: SR's files are merged) the event branches against SR's REAL files instead of the
          recording stubs: the item with room (the real items/enh_add -> ★☆☆, items/give -> build_display -> give_macro:
          one `give` of sword_hwamu with api.ITEM_MODEL), a full inventory (no give; the real items/drop at the player's
          body in the reward hook: one glowing mythic ground item rlk_ditem + rlk_daura, its rlk:ditems record), the buff
          (ev/buff: hrMoon 1, the subtitle numbers from load's 조절 지점 constants), the duplicate rules of PLAN §7.3.1 on
          SR's scores (hrMoon granted by the real ev/buff -> item; it_sword_hwamu, the inventory scan's score of the
          registered id -> buff). SR's SNBT reader (HR/sr/srsim.py: the item tables use single-quoted strings mcsim's
          reader cannot read) parses `value` compounds in this section only; mcsim's own macro call is kept.
"""
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'lib'))
import hrsim as H  # noqa: E402

ARGS = [a for a in sys.argv[1:] if a != '-v']
VERBOSE = '-v' in sys.argv[1:]
DP = Path(ARGS[0]).resolve()
SECTIONS = ARGS[1:] or ['flow', 'roll', 'inv', 'reload', 'words', 'scope', 'real']
sys.path.insert(0, str(DP / 'tools'))
import mboss_scarlet.api as API  # noqa: E402
check = H.check if VERBOSE else H.ck
T = API.EV_TEXT
ID = API.ITEM_ID
H_END = API.SEQ_LEN['ending']                  # H: the ending's end, the coda starts in the same tick
DEATH = H_END + API.SEQ_LEN['event'] + 2       # registry death (1164)
ITEM, BUFF = API.EV_BRANCH['item'], API.EV_BRANCH['buff']

VARS = {}


def var(name='base'):
    if 'root' not in VARS:
        VARS['root'] = H.variant_hr(DP, H.enable_scarlet, label='reward')
        VARS['build'] = 'base'
    root = VARS['root']
    if VARS['build'] != name:
        import shutil
        d = root / 'data/rlk/function/boss/scarlet'
        if name == 'base':
            shutil.rmtree(d)
            shutil.copytree(DP / 'data/rlk/function/boss/scarlet', d)
        else:
            H.dry_build(root, kit=name == 'kit', patch={'kit': '', 'pm0': "api.EVENT['item_pm'] = 0",
                                                         'pm1000': "api.EVENT['item_pm'] = 1000",
                                                         'forever': "api.EVENT['buff_scope'] = 'forever'"}[name])
        VARS['build'] = name
    return root


def item_stubs(s):
    """SR's item calls as recording stubs (sword_hwamu is not registered on this branch)."""
    s.cache['rlk:items/give'] = ['$data modify storage rlk:hrtest give append value "$(id)"',
                                 '$data modify storage rlk:pinv order append value "$(id)"']
    s.cache['rlk:items/drop'] = ['$data modify storage rlk:hrtest drop append value "$(id)"',
                                 'summon minecraft:item ~ ~ ~ {Tags:["rlk_room","rlk_daura","rlk_ditem"]}']
    s.storage.setdefault('rlk:hrtest', {})
    s.storage['rlk:hrtest']['give'] = []
    s.storage['rlk:hrtest']['drop'] = []
    for k, v in zip(API.BUFF_FP, API.BUFF_VALUES['run']):
        s.setsc(k, 'tmp', v)                    # SR's load (조절 지점) sets these
    # items/register's rarity / star tables (load): the coda title and the chat record read the stars at run time (F3, HR-33)
    reg = (DP / 'data/rlk/function/items/register.mcfunction').read_text(encoding='utf-8').split('\n')
    s.cache['rlk:hrtest/reg_tables'] = [ln for ln in reg[:13] if ln.startswith('data modify storage rlk:items')]
    s.call('rlk:hrtest/reg_tables', H.C0)


def gives(s):
    return list(s.storage.get('rlk:hrtest', {}).get('give', []))


def drops(s):
    return list(s.storage.get('rlk:hrtest', {}).get('drop', []))


def live_render(s):
    """Render every title / tellraw at the moment it runs (its nbt components read storage then: cur.* is gone later); F3:
    also the actionbar, and the coloured runs of the module's ev/* lines (s.rruns: (t, kind, [(text, colour)])."""
    s.rtitles, s.rtells, s.rruns = [], [], []
    orig = s.cmd

    def cmd(t, ctx):
        if t and t[0] == 'title' and len(t) >= 4 and t[2] in ('title', 'subtitle', 'actionbar'):
            s.rtitles.append((s.t, t[2], render(s, ' '.join(t[3:]))))
            if s.stack and s.stack[-1].startswith('rlk:boss/scarlet/ev/'):
                s.rruns.append((s.t, t[2], runs(s, ' '.join(t[3:]))))
        elif t and t[0] == 'tellraw' and len(t) >= 3:
            s.rtells.append((s.t, render(s, ' '.join(t[2:]))))
            if s.stack and s.stack[-1].startswith('rlk:boss/scarlet/ev/'):
                s.rruns.append((s.t, 'tellraw', runs(s, ' '.join(t[2:]))))
        return orig(t, ctx)
    s.cmd = cmd


def world(seed=5, name='base', branch=None, cap=None, held=0):
    s, pl = H.setup_sc(var(name), seed=seed)
    live_render(s)
    item_stubs(s)
    ok = H.fight_sc(s, intro=False)
    assert ok
    H.run_sc(s, 2)
    if branch:
        H.test_id(s, {'item': 91, 'buff': 92}[branch])
    if cap is not None:
        cap_n, used = cap
        s.setsc(('e', pl.id), 'invCap', cap_n)
        s.storage.setdefault('rlk:pinv', {})['order'] = [f'x{i}' for i in range(used)]
    s.setsc(('e', pl.id), API.ITEM_SCORE, held)
    return s, pl


def hr(s, k):
    return s.sc(k, 'hr')


def mb(s, k):
    return s.sc(k, 'mb') or 0


LEFTOVERS = {'#sq_x': 5, '#sq_g': 13, '#g_n': 3, '#g_c': 2, '#r2_a': 1, '#a9_n': 4, '#a6_n': 2}   # other owners' families


def at_hook(s):
    """F3 (HR-05): snapshot objective hr and storage rlk:hr when the reward hook starts (after the module's cleanup)."""
    s.hook_snap = []
    inner = s.call

    def call(fid, ctx, macro=None):
        if fid == 'rlk:boss/scarlet/reward':
            import copy
            s.hook_snap.append(({k[0]: v for k, v in s.scores.items() if k[1] == 'hr'},
                                copy.deepcopy(s.storage.get('rlk:hr', {}))))
        return inner(fid, ctx, macro)
    s.call = call


def kill(s):
    pl = s.player()
    s.watch['rlk:boss/scarlet/reward'] = []
    s.watch['rlk:boss/scarlet/ev/apply'] = []
    s.watch['rlk:mboss/death_finish'] = []
    s.watch['rlk:mboss/sp/lvup'] = []
    s.watch['rlk:mboss/box/drop_all'] = []
    H.kill(s, pl)


def fast_forward(s, to):
    """The stand-in ending has no beat after its music (300): jump its clock and the framework's death clock together."""
    d = to - (hr(s, '#sq') or 0)
    if d > 0:
        s.setsc('#sq', 'hr', to)
        s.setsc('#mbT', 'mb', mb(s, '#mbT') + d)


def finish(s, limit=2500):
    return H.until_sc(s, lambda s: mb(s, '#mbLive') == 0 and (s.sc('#combat', 'room') or 0) == 0, limit, each=H.heal)


def render(s, comp):
    """Plain text of a title / tellraw component as shown: text verbatim, nbt components from storage (interpret:true
    reads the stored component: a compound or a list, F3), score components from the scoreboard."""
    try:
        return ''.join(t for t, _ in runs(s, comp))
    except Exception:  # noqa: BLE001  (a component SR's reader cannot read: the regex reading below)
        pass
    out = []
    pat = r'\{(?:text:"((?:[^"\\]|\\.)*)"|nbt:"([^"]+)",storage:"([^"]+)"(,interpret:true)?|score:\{name:"([^"]+)",objective:"([^"]+)"\})'
    for m in re.finditer(pat, comp):
        txt, path, st, interp, name, obj = m.groups()
        if txt is not None:
            out.append(txt)
        elif path is not None:
            try:
                v = s.path_get(s.storage[st], path)
            except (KeyError, IndexError, TypeError):
                v = ''
            if interp and isinstance(v, dict):
                v = v.get('text', '')
            out.append(str(v))
        else:
            out.append(str(s.sc(name, obj)))
    return ''.join(out)


_SR = {}


def sr():
    """SR's SNBT reader (HR/sr/srsim.py; its import patches mcsim.Sim.call: undone at once)."""
    if 'm' not in _SR:
        import mcsim
        orig = mcsim.Sim.call
        sys.path.insert(0, str(HERE.parent / 'sr'))
        import srsim as SR
        mcsim.Sim.call = orig
        _SR['m'] = SR
    return _SR['m']


def runs(s, comp_text, color=None):
    """The coloured text runs [(text, colour)] of a component as the client draws it: children inherit the parent's colour,
    a list's first element is the parent of the rest, nbt components with interpret:true are resolved from storage (a stored
    list / compound is a component), score components from the scoreboard."""
    def walk(c, col):
        if isinstance(c, str):
            return [(c, col)]
        if isinstance(c, list):
            if not c:
                return []
            head = walk(c[0], col)
            pc = c[0].get('color', col) if isinstance(c[0], dict) else col
            return head + [r for x in c[1:] for r in walk(x, pc)]
        col = c.get('color', col)
        out = []
        if 'text' in c:
            out.append((c['text'], col))
        elif 'score' in c:
            out.append((str(s.sc(c['score']['name'], c['score']['objective'])), col))
        elif 'nbt' in c:
            try:
                v = s.path_get(s.storage[c['storage']], c['nbt'])
            except (KeyError, IndexError, TypeError):
                v = None
            if v is not None:
                out += walk(v, col) if c.get('interpret') else [(str(v), col)]
        for x in c.get('extra', []):
            out += walk(x, col)
        return out
    return [(t, c) for t, c in walk(sr().snbt_parse(comp_text), color) if t]


# 26.3 glyph advances (font px; the D3b-C critic / verifier measured them on the 26.3 client jar and asset index 34:
# unifont Hangul 8, ascii.png / nonlatin_european.png bitmaps; bold +1, unihex bold +0.5). An unknown glyph fails the check.
ADV = {' ': 4, '[': 4, ']': 4, 'M': 6, 'Y': 6, 'T': 6, 'H': 6, 'I': 4, 'C': 6, '+': 6, '%': 6, '·': 2, '★': 8, '☆': 8, '—': 9,
       '.': 2, ',': 2, '?': 6, '(': 5, ')': 5, **{d: 6 for d in '0123456789'}}


def font_w(text, bold=False):
    w = 0.0
    for ch in text:
        if 0xAC00 <= ord(ch) <= 0xD7A3:
            w += 8 + (0.5 if bold else 0)
        elif ch in ADV:
            w += ADV[ch] + (1 if bold and ch != ' ' else 0)
        else:
            return None
    return w


def titles_of(s, since=0, kind='title'):
    return [x for t, k, x in s.rtitles if t >= since and k == kind]


def tells_of(s, since=0):
    return [x for t, x in s.rtells if t >= since]


# ================================================================================================= real (I1)
_REAL = {}


def real_cls():
    """An ScSim whose SNBT reader is SR's (srsim imports patch mcsim.Sim.call: undone at once, the framework's macros keep
    mcsim's own argument stringification)."""
    if 'cls' not in _REAL:
        import mcsim
        orig = mcsim.Sim.call
        sys.path.insert(0, str(HERE.parent / 'sr'))
        import srsim as SR
        mcsim.Sim.call = orig

        class RealSim(H.ScSim):
            def snbt(self, txt):
                return SR.snbt_parse(txt)
        _REAL['cls'] = RealSim
    return _REAL['cls']


def real_items(s):
    """What load / items/register give the real item at run time: the rarity / star tables, sword_hwamu's def (registry +
    ids), the tune factors + its ★★★ base values (items/tune/b10) + their capture, load's 조절 지점 #hrMoon* constants."""
    fn_dir = DP / 'data/rlk/function'
    reg = (fn_dir / 'items/register.mcfunction').read_text(encoding='utf-8').split('\n')
    s.cache['rlk:hrtest/reg_tables'] = [ln for ln in reg[:13] if ln.startswith('data modify storage rlk:items')]
    s.call('rlk:hrtest/reg_tables', H.C0)
    s.storage.setdefault('rlk:items', {})['registry'] = {}
    s.storage['rlk:items']['ids'] = []
    s.call('rlk:items/mythic/sword_hwamu/def', H.C0)
    tune = (fn_dir / 'items/tune/register.mcfunction').read_text(encoding='utf-8').split('\n')
    s.cache['rlk:hrtest/tune_fac'] = [ln for ln in tune if ln.startswith('data modify storage rlk:tune fac')]
    s.call('rlk:hrtest/tune_fac', H.C0)
    s.storage.setdefault('rlk:tune', {})['t'] = {}
    s.storage['rlk:tune']['ids'] = []
    s.call('rlk:items/tune/b10', H.C0)
    s.call('rlk:items/tune/capture', H.C0, {'id': ID})
    load = (fn_dir / 'load.mcfunction').read_text(encoding='utf-8').split('\n')
    s.cache['rlk:hrtest/moon_k'] = [ln for ln in load if ln.startswith('scoreboard players set #hrMoon')]
    s.call('rlk:hrtest/moon_k', H.C0)


def real_world(seed, branch, cap=None, held=0):
    s, pl = H.setup_sc(var('base'), seed=seed, cls=real_cls())
    live_render(s)
    real_items(s)
    s.real_give, s.real_summon = [], []
    inner = s.cmd

    def cmd(t, ctx):
        if t and t[0] == 'give':
            s.real_give.append((s.t, ctx.ex.etype if ctx.ex else None, ' '.join(t)))
        elif t and t[0] == 'summon' and len(t) > 1 and t[1] == 'minecraft:item':
            s.real_summon.append((s.t, ' '.join(t)))
        return inner(t, ctx)
    s.cmd = cmd
    ok = H.fight_sc(s, intro=False)
    assert ok
    H.run_sc(s, 2)
    if branch:
        H.test_id(s, {'item': 91, 'buff': 92}[branch])
    if cap is not None:
        s.setsc(('e', pl.id), 'invCap', cap[0])
        s.storage.setdefault('rlk:pinv', {})['order'] = [f'x{i}' for i in range(cap[1])]
    s.setsc(('e', pl.id), API.ITEM_SCORE, held)
    return s, pl


def ditems(s):
    return [e for e in s.ents if e.alive and e.etype == 'item' and 'rlk_ditem' in e.tags]


def sec_real():
    s, pl = real_world(51, 'item', cap=(9, 5))
    reg = s.storage['rlk:items']
    check('X0 SR\'s real def registers sword_hwamu (registry + ids: items/reg_flags_loop makes its it_sword_hwamu score), '
          'model api.ITEM_MODEL, rarity mythic', ID in reg.get('ids', []) and reg['registry'][ID].get('model') == API.ITEM_MODEL
          and reg['registry'][ID].get('rarity') == 'mythic', reg['registry'].get(ID, {}).get('model'))
    kill(s)
    fast_forward(s, H_END - 2)
    finish(s)
    g = s.real_give
    want = (f'minecraft:custom_data={{rlk:{{id:"{ID}"}}}}', f'minecraft:item_model="{API.ITEM_MODEL}"')
    check('X1 item, room: the real items/give -> give_macro runs once, as the player: one `give` of sword_hwamu with '
          'api.ITEM_MODEL, its name at ★☆☆; no ground item, #hrEvDrop 0',
          len(g) == 1 and g[0][1] == 'player' and all(w in g[0][2] for w in want) and "'★'" in g[0][2] and "'☆☆'" in g[0][2]
          and not ditems(s) and hr(s, '#hrEvDrop') == 0, (g[:1], len(ditems(s))))
    check('X2 item, room: the star raised first by the real items/enh_add (rlk:pinv enh.sword_hwamu 1, sword_hwamu enhL 1)',
          s.storage['rlk:pinv'].get('enh', {}).get(ID) == 1 and s.sc(ID, 'enhL') == 1,
          (s.storage['rlk:pinv'].get('enh'), s.sc(ID, 'enhL')))
    for capn in (9, 18):
        s, pl = real_world(52 + capn, 'item', cap=(capn, capn))
        kill(s)
        fast_forward(s, H_END - 2)
        ok = H.until_sc(s, lambda s: hr(s, '#hrEvDone') == 1, 200, each=H.heal)
        flag = hr(s, '#hrEvDrop')
        t0 = s.t
        finish(s)
        it = ditems(s)
        b = pl
        at_body = len(it) == 1 and all(abs(it[0].pos[i] - b.pos[i]) < 1e-6 for i in (0, 2)) and abs(it[0].pos[1] - b.pos[1] - 0.35) < 1e-6
        rec = list(s.storage.get('rlk:ditems', {}).get('records', {}).values())
        sm = [x for _, x in s.real_summon if f'rlk_ditem:{{id:"{ID}"}}' in x and f'"minecraft:item_model":"{API.ITEM_MODEL}"' in x]
        notes = [x for x in tells_of(s, t0) if x == T['chat_full']]
        check(f'X3 item, full at invCap {capn}: no `give`; #hrEvDrop 1 at the grant; the reward hook runs the real items/drop at the '
              'player\'s body: one glowing mythic ground item (rlk_ditem + rlk_daura, +0.35 b) of sword_hwamu with api.ITEM_MODEL, '
              'its rlk:ditems record, the notice once',
              ok and not s.real_give and flag == 1 and at_body and 'rlk_daura' in it[0].tags and len(sm) == 1
              and [r.get('id') for r in rec] == [ID] and len(notes) == 1,
              (len(s.real_give), flag, [(sorted(e.tags), e.pos) for e in it], len(sm), rec[:1], notes))
        check(f'X4 invCap {capn}: never lost, never doubled (real give + real ground item = 1)', len(s.real_give) + len(it) == 1)
    s, pl = real_world(61, 'buff', cap=(9, 2))
    kill(s)
    fast_forward(s, H_END - 2)
    finish(s)
    subs = titles_of(s, 0, 'subtitle')
    check('X5 buff: ev/buff sets SR\'s hrMoon 1 on the player; nothing given or dropped; the subtitle shows load\'s constants '
          f'({[s.sc(k, "tmp") for k in API.BUFF_FP]}) = api.EV_TEXT buff_sub verbatim',
          s.sc(('e', pl.id), API.BUFF_OBJ) == 1 and not s.real_give and not ditems(s) and T['buff_sub'] in subs, (subs[-2:],))
    # the duplicate rules (PLAN §7.3.1) on SR's own scores, after the real grant
    c = roll_n(s, 300)
    check('X6 duplicates: hrMoon 1 granted by the real ev/buff -> every next roll is the item (300 / 300)', c == 300, c)
    s.setsc(('e', pl.id), API.BUFF_OBJ, 0)
    s.setsc(('e', pl.id), API.ITEM_SCORE, 1)      # what items/scan_count writes while the sword is in the inventory
    c = roll_n(s, 300)
    check(f'X7 duplicates: {API.ITEM_SCORE} >= 1 (the sword held) -> every next roll is the buff (0 / 300 item)', c == 0, c)


# ================================================================================================= flow
def sec_flow():
    for branch in ('item', 'buff'):
        s, pl = world(11, branch=branch, cap=(9, 3))
        # F3 (HR-05): what the other owners leave in objective hr / storage rlk:hr during a fight (patterns, the ghost
        # helpers, the sequences: written before read, never reset by the core's list before F3)
        for k, v in LEFTOVERS.items():
            s.setsc(k, 'hr', v)
        s.storage.setdefault('rlk:hr', {})['seq'] = {'g': 'a13'}
        at_hook(s)
        xp0 = s.sc('#XP', 'azs') or 0
        pk0 = s.sc(('e', pl.id), 'pkPending') or 0
        n_part = len(s.particles)
        kill(s)
        t_k = s.t
        check(f'W1 {branch}: the kill -> death_start: the death state, the roll done (#hrEv {API.EV_BRANCH[branch]}), the ending',
              mb(s, '#mbSt') == 2 and hr(s, '#hrEv') == API.EV_BRANCH[branch] and hr(s, '#sqn') == 7 and hr(s, '#hrEvDone') == 0,
              (mb(s, '#mbSt'), hr(s, '#hrEv'), hr(s, '#sqn')))
        ok = H.until_sc(s, lambda s: hr(s, '#sqn') == 8, H_END + 20, each=H.heal)
        t_h = s.t
        check(f'W2 {branch}: seq/event starts at H = {H_END} (the ending\'s end, the same tick)', ok and abs((t_h - t_k) - H_END) <= 1,
              (ok, t_h - t_k))
        ok = H.until_sc(s, lambda s: hr(s, '#hrEvDone') == 1, 200, each=H.heal)
        t_g = s.t
        got = gives(s) if branch == 'item' else s.sc(('e', pl.id), API.BUFF_OBJ)
        check(f'W3 {branch}: the grant at E{API.EV_T["grant"]} (once), the title in that tick',
              ok and abs((t_g - t_h) - API.EV_T['grant']) <= 1 and (got == [ID] if branch == 'item' else got == 1)
              and titles_of(s, t_g - 1), (t_g - t_h, got, titles_of(s, t_g - 1)))
        ok = finish(s)
        df = s.watch['rlk:mboss/death_finish']
        poof = [p for p in s.particles[n_part:] if p[1] == 'poof']
        check(f'W4 {branch}: death_finish at H + 122 = {DEATH} after the kill, no poof (poof:0b)',
              ok and len(df) == 1 and abs((df[0][0] - t_k) - DEATH) <= 2 and not poof, (df, len(poof)))
        tt = titles_of(s, df[0][0] if df else 0)
        sub = titles_of(s, df[0][0] if df else 0, 'subtitle')
        check(f'W5 {branch}: the return title words: "{T["return_title"]}" / "{T["return_sub"]}"',
              T['return_title'] in tt and T['return_sub'] in sub, (tt, sub))
        w = s.watch['rlk:boss/scarlet/reward']
        lv = s.watch['rlk:mboss/sp/lvup']
        bx = s.watch['rlk:mboss/box/drop_all']
        need = (s.sc(('e', pl.id), 'xpNeed') or 0) - (s.sc(('e', pl.id), 'xp') or 0)
        check(f'W6 {branch}: exactly one level (sp/lvup once: #xpAdd = xpNeed - xp through player/level/add_xp, whose '
              f'pkPending + 1 is the sim stub\'s), the hook once as the player after it, then one box (the rift collapse)',
              len(lv) == 1 and len(w) == 1 and w[0][1] == 'player' and lv[0][0] <= w[0][0]
              and (s.sc('#XP', 'azs') or 0) - xp0 == max(1, need)
              and H.until_sc(s, lambda s: len(H.boxes(s)) >= 1, 80) and len(H.boxes(s)) == 1,
              (lv, w, (s.sc('#XP', 'azs') or 0) - xp0, need, len(H.boxes(s))))
        snap = s.hook_snap[0] if s.hook_snap else ({}, {})
        ev_want = {'#hrEv': API.EV_BRANCH[branch], '#hrEvDone': 1, '#hrEvDrop': 0}
        check(f'HR-05 {branch}: at the reward hook (after cleanup) objective hr holds only the event scores, their values kept '
              f'({ev_want}): the patterns\' / ghost helpers\' / sequences\' fake players are gone; storage rlk:hr has no core / seq',
              len(s.hook_snap) == 1 and snap[0] == ev_want and 'seq' not in snap[1] and 'core' not in snap[1],
              (sorted(snap[0].items()), sorted(snap[1])))
        check(f'W7 {branch}: after the hook the event state is reset (#hrEv* 0, ev.force gone), the outcome kept',
              all(hr(s, k) == 0 for k in API.EV_FP) and 'force' not in s.storage.get('rlk:hr', {}).get('ev', {})
              and (gives(s) == [ID] if branch == 'item' else s.sc(('e', pl.id), API.BUFF_OBJ) == 1) and not drops(s),
              ([hr(s, k) for k in API.EV_FP], s.storage.get('rlk:hr'), gives(s), drops(s)))


# ================================================================================================= roll
def roll_n(s, n):
    pl = s.player()
    c = 0
    for _ in range(n):
        s.call('rlk:boss/scarlet/ev/roll', H.C0)
        c += hr(s, '#hrEv') == ITEM
    return c


def sec_roll():
    s, pl = world(21)
    n = 10000
    c = roll_n(s, n)
    check(f'O1 {n} seeded rolls: item {c / n:.3f} (50 +- 1.5 %)', abs(c / n - 0.5) <= 0.015, c / n)
    vals = {hr(s, '#hrEv')}
    for _ in range(50):
        s.call('rlk:boss/scarlet/ev/roll', H.C0)
        vals.add(hr(s, '#hrEv'))
    check('O2 the roll gives 1 or 2 only, #hrEvDone / #hrEvDrop 0', vals <= {ITEM, BUFF} and hr(s, '#hrEvDone') == 0
          and hr(s, '#hrEvDrop') == 0, vals)
    for name, want in (('pm0', 0), ('pm1000', 2000)):
        s, pl = world(22, name=name)
        c = roll_n(s, 2000)
        check(f'O3 item_pm {0 if want == 0 else 1000} (dry build): {"all buff" if want == 0 else "all item"}', c == want, c)
    s, pl = world(23)
    s.setsc(('e', pl.id), API.ITEM_SCORE, 1)
    c = roll_n(s, 300)
    check('O4 the sword held (it_sword_hwamu >= 1): always the buff (no duplicate)', c == 0, c)
    s.setsc(('e', pl.id), API.ITEM_SCORE, 0)
    s.setsc(('e', pl.id), API.BUFF_OBJ, 1)
    c = roll_n(s, 300)
    check('O5 the buff already on (hrMoon >= 1): always the item', c == 300, c)
    s.setsc(('e', pl.id), API.BUFF_OBJ, 0)
    for tid, br, want in ((91, 'item', 300), (92, 'buff', 0)):
        H.test_id(s, tid)
        s.setsc(('e', pl.id), API.ITEM_SCORE, 1 if br == 'item' else 0)
        s.setsc(('e', pl.id), API.BUFF_OBJ, 1 if br == 'buff' else 0)
        c = roll_n(s, 300)
        check(f'O6 test {tid} (ev.force "{br}"): always {br}, before the duplicate rules', c == want, c)
    H.test_id(s, 90)
    check('O7 test 90: ev.force removed (random again)', 'ev' not in s.storage.get('rlk:hr', {}) or
          'force' not in s.storage['rlk:hr'].get('ev', {}), s.storage.get('rlk:hr'))
    # cleared after use: test 91, the kill, the reward hook -> ev.force gone
    s, pl = world(24, branch='item', cap=(9, 0))
    kill(s)
    fast_forward(s, H_END - 2)
    finish(s)
    check('O8 ev.force is cleared by the reward hook (the next kill rolls at random again)',
          'force' not in s.storage.get('rlk:hr', {}).get('ev', {}) and gives(s) == [ID], (s.storage.get('rlk:hr'), gives(s)))


# ================================================================================================= inv
def sec_inv():
    s, pl = world(31, branch='item', cap=(9, 5))
    kill(s)
    fast_forward(s, H_END - 2)
    finish(s)
    order = s.storage['rlk:pinv']['order']
    check('V1 room: items/give {id:"sword_hwamu"} once, rlk:pinv order + 1, the star 1 (enh.sword_hwamu 1 = ★☆☆), no drop',
          gives(s) == [ID] and len(order) == 6 and s.storage['rlk:pinv'].get('enh', {}).get(ID) == 1 and not drops(s)
          and hr(s, '#hrEvDrop') == 0, (gives(s), len(order), s.storage['rlk:pinv'].get('enh'), drops(s)))
    for cap in (9, 18):
        s, pl = world(32 + cap, branch='item', cap=(cap, cap))
        kill(s)
        fast_forward(s, H_END - 2)
        ok = H.until_sc(s, lambda s: hr(s, '#hrEvDone') == 1, 200, each=H.heal)
        drop_flag = hr(s, '#hrEvDrop')
        t0 = s.t
        finish(s)
        items = [e for e in s.ents if e.alive and e.etype == 'item' and 'rlk_daura' in e.tags]
        b = pl
        at_body = items and all(abs(items[0].pos[i] - b.pos[i]) < 1e-6 for i in (0, 2))
        notes = [x for x in tells_of(s, t0) if x == T['chat_full']]
        check(f'V2 full at invCap {cap}: no give, #hrEvDrop 1 at the grant, one ground item at the player\'s body (rlk_daura), '
              f'one notice', ok and not gives(s) and drop_flag == 1 and drops(s) == [ID] and len(items) == 1 and at_body
              and len(notes) == 1, (gives(s), drop_flag, drops(s), len(items), notes))
        check(f'V3 invCap {cap}: never lost, never doubled (give + drop = 1), the order unchanged',
              len(gives(s)) + len(drops(s)) == 1 and len(s.storage['rlk:pinv']['order']) == cap)
    s, pl = world(36, branch='buff', cap=(9, 9))
    kill(s)
    fast_forward(s, H_END - 2)
    finish(s)
    check('V4 the buff branch with a full inventory: hrMoon 1, nothing given or dropped',
          s.sc(('e', pl.id), API.BUFF_OBJ) == 1 and not gives(s) and not drops(s), (gives(s), drops(s)))


# ================================================================================================= reload
def outcome(s, pl, branch):
    return (len(gives(s)) + len(drops(s))) if branch == 'item' else (s.sc(('e', pl.id), API.BUFF_OBJ) or 0)


def sec_reload():
    bad = []
    runs = 0
    for e in list(range(0, API.SEQ_LEN['event'] + 1)) + ['cs4_5', 'cs4_300', 'cs4_1041']:
        branch = 'item' if (e if isinstance(e, int) else len(e)) % 2 == 0 else 'buff'
        full = isinstance(e, int) and e % 3 == 0
        s, pl = world(41, branch=branch, cap=(9, 9 if full else 2))
        kill(s)
        if isinstance(e, int):
            fast_forward(s, H_END - 2)
            ok = H.until_sc(s, lambda s: hr(s, '#sqn') == 8 and (hr(s, '#sq') or 0) >= e, 200, each=H.heal)
        else:
            ok = H.until_sc(s, lambda s: (hr(s, '#sq') or 0) >= int(e.split('_')[1]), H_END + 10, each=H.heal)
        s.call('rlk:mboss/init', H.C0)              # /reload: the framework finishes the death at once
        fin = finish(s)
        runs += 1
        ev_left = H.ents_tagged(s, API.TAGS['ev'])
        n = outcome(s, pl, branch)
        hooks = len(s.watch['rlk:boss/scarlet/reward'])
        if not (ok and fin and n == 1 and hooks == 1 and not ev_left and all(hr(s, k) == 0 for k in API.EV_FP)):
            bad.append((e, branch, full, ok, fin, n, hooks, ev_left[:1], [hr(s, k) for k in API.EV_FP]))
    check(f'D1 /reload at every coda tick E0-E{API.SEQ_LEN["event"]} and in CS4 ({runs} runs, both branches, full / room): '
          'the outcome exactly once, the hook once, no rlk_hr_ev left, the event scores 0', not bad, bad[:4])


# ================================================================================================= words
GOLD, GREY = '#FFD24A', '#6B6B6B'      # items/register's star colours (★ / ☆)


def star_runs(rs):
    return [(t, c) for t, c in rs if set(t) <= {'★', '☆'}]


def hud_run(seed=53):
    """F3 (HR-35, VF3-1-01): the buff branch's coda once more, with the REAL player/hud/tick (the regular actionbar HUD, which
    skips its draw and counts hudHold down while hudHold >= 1) run as the player every game tick at its place in rlk:tick:
    in player/tick right after player/elem_tick, so before mboss/main (the coda). Returns s, ev = [(tick, #sq, the
    actionbars it wrote, the `times` it set, the player's hudHold right after)] per ev/title run, hud = [(tick, drew an
    actionbar)] per HUD tick; every actionbar of the run is in s.rtitles."""
    s, pl = world(seed, name='kit', branch='buff', cap=(9, 1))
    ev, hud = [], []
    inner = s.call

    def call(fid, ctx, macro=None):
        if fid == 'rlk:boss/scarlet/ev/title':
            n_t, n_r = len(s.titles), len(s.rtitles)
            r = inner(fid, ctx, macro)
            ev.append((s.t, hr(s, '#sq'), [x for _, k, x in s.rtitles[n_r:] if k == 'actionbar'],
                       [x.split()[2:] for _, x in s.titles[n_t:] if x.startswith('@a[tag=player] times ')],
                       s.sc(('e', pl.id), 'hudHold') or 0))
            return r
        r = inner(fid, ctx, macro)
        if fid == 'rlk:player/elem_tick' and not s.stack:
            n = len(s.rtitles)
            inner('rlk:player/hud/tick', H.Ctx(pl, tuple(pl.pos), tuple(pl.rot)))
            hud.append((s.t, any(k == 'actionbar' for _, k, _ in s.rtitles[n:])))
        return r
    s.call = call
    kill(s)
    fast_forward(s, H_END - 2)
    H.until_sc(s, lambda s: hr(s, '#sqn') == 8, 20, each=H.heal)
    H.until_sc(s, lambda s: (hr(s, '#sq') or 0) >= API.SEQ_LEN['event'] or hr(s, '#sqn') != 8, 200, each=H.heal)
    H.run_sc(s, 20, each=H.heal)          # the HUD back after (merged with F2, its coda holds it a few t past E120)
    return s, ev, hud


def sec_words():
    item_name = T.get('item_name', T['item_title'])
    for branch in ('item', 'buff'):
        s, pl = world(51, name='kit', branch=branch, cap=(9, 1))
        kill(s)
        fast_forward(s, H_END - 2)
        ok = H.until_sc(s, lambda s: hr(s, '#sqn') == 8, 20, each=H.heal)
        t_h = s.t
        n_t, n_c = len(s.titles), len(s.tells)
        ok = H.until_sc(s, lambda s: (hr(s, '#sq') or 0) >= API.SEQ_LEN['event'] or hr(s, '#sqn') != 8, 200, each=H.heal)
        tt = titles_of(s, t_h)
        sub = titles_of(s, t_h, 'subtitle')
        lines = [a.get('id') for t, c, a in s.kitl if c == 'hud/line' and t >= t_h]
        # F-I: the coda's own blank at its start (F2 round 1, `seq.HUD_BLANK`: the HUD-off sequences clear the last actionbar
        # once; ev_dry checks it) is not one of the buff's texts
        ab = [x for x in titles_of(s, t_h, 'actionbar') if x != '']
        rr = [(k, r) for t, k, r in s.rruns if t >= t_h]
        if branch == 'item':
            check('G1 item: the title = api.EV_TEXT item_title verbatim (dark_red, the light shadow), the subtitle = item_sub',
                  tt == [T['item_title']] and sub == [T['item_sub']] and any('color:"dark_red",shadow_color:-8730' in x for _, x in s.titles),
                  (tt, sub))
            tr = [r for k, r in rr if k == 'title']
            check('HR-33 item title: the name dark_red, the stars in the item\'s own colours from rlk:items (★ gold, ☆☆ grey)',
                  len(tr) == 1 and (API.ITEM_NAME, 'dark_red') in tr[0] and star_runs(tr[0]) == [('★', GOLD), ('☆☆', GREY)],
                  tr)
            check('HR-35 item: the 4x title <= 106 font px, 「[ MYTHIC ]」 on the subtitle (<= 192 font px)',
                  tt and font_w(tt[0]) is not None and font_w(tt[0]) <= 106 and '[ MYTHIC ]' not in tt[0]
                  and sub and sub[0].startswith('[ MYTHIC ]') and font_w(sub[0]) is not None and font_w(sub[0]) <= 192,
                  [(x, font_w(x)) for x in tt + sub])
            check('G2 the coda line of the item branch = api.LINES 24 (kit fx/hud/line {id:24}) at E4, once', lines == [24]
                  and API.LINES[24] == T['line_item'], lines)
        else:
            check('G1 buff: the title = buff_title, the subtitle renders buff_sub with the numbers (score components)',
                  tt == [T['buff_title']] and sub == [T['buff_sub']], (tt, sub))
            check('HR-35 buff: the subtitle <= 192 font px (the first two numbers), the third number on the actionbar (= buff_ab), '
                  'all three = buff_stats', sub and font_w(sub[0]) is not None and font_w(sub[0]) <= 192
                  and ab == [T.get('buff_ab')] and f'{sub[0]} · {ab[0]}' == T.get('buff_stats')
                  and font_w(tt[0], bold=True) is not None and font_w(tt[0], bold=True) * 4 <= 106 * 4,
                  [(x, font_w(x)) for x in sub + ab])
            # VF3-1-01: the hold as behaviour (a sim run of the coda with the real HUD tick), not a substring of ev/title
            s2, ev, hud = hud_run()
            t1 = ev[0][0] if len(ev) == 1 else None
            tt = sum(int(x) for x in ev[0][3][0]) if t1 is not None and len(ev[0][3]) == 1 else 0
            check('HR-35 buff: ev/title runs once, at E56 (#sq = EV_T grant), writes the third number on the actionbar (= buff_ab) '
                  'and leaves the player\'s hudHold = the title\'s own time (fade-in + stay + fade-out of its `times` = EV_T '
                  'black - grant = 54)', t1 is not None and ev[0][1] == API.EV_T['grant'] and ev[0][2] == [T.get('buff_ab')]
                  and tt == API.EV_T['black'] - API.EV_T['grant'] and ev[0][4] == tt, ev)
            held = [d for t, d in hud if t1 is not None and t1 < t <= t1 + tt]
            abar = [(t, x) for t, k, x in s2.rtitles if k == 'actionbar' and t1 is not None and t1 <= t <= t1 + tt]
            back = [t for t, d in hud if t1 is not None and t > t1 + tt and d]
            check('HR-35 buff: with the REAL player/hud/tick every game tick (before mboss/main), the regular HUD never overwrites '
                  'that actionbar while the title shows (the next 54 HUD ticks, E57-E110, draw nothing), no other actionbar '
                  'reaches the player from E56 to E110 (the buff\'s is the last of E56), and the HUD draws again after',
                  tt > 0 and len(held) == tt and not any(held) and abar and abar[-1] == (t1, T.get('buff_ab'))
                  and all(t == t1 for t, _ in abar) and bool(back),
                  dict(t1=t1, tt=tt, held=f'{len(held)} ticks, {sum(held)} drew', abar=abar[-3:], back=back[:1]))
            check('G2 the coda line of the buff branch = api.LINES 25 (kit fx/hud/line {id:25}) at E4, once', lines == [25]
                  and API.LINES[25] == T['line_buff'], lines)
        other = [x for _, x in s.titles[n_t:] if not x.startswith(('@a[tag=player] title ', '@a[tag=player] subtitle ',
                                                                     '@a[tag=player] times '))
                 and not (branch == 'buff' and x.startswith('@a[tag=player] actionbar '))]   # F3 (HR-35): the third number
        check(f'G3 {branch}: no other title / chat line of the module during the coda', not other and len(s.tells) == n_c,
              (other, s.tells[n_c:]))
        t0 = s.t
        finish(s)
        chat = tells_of(s, t0)
        want = (T['chat_item'] + item_name) if branch == 'item' else T['chat_buff']
        check(f'G4 {branch}: the chat record at the rift = "{want}"', want in chat, chat)
        if branch == 'item':
            cr = [r for t, k, r in s.rruns if t >= t0 and k == 'tellraw']
            check('HR-33 the chat record: the item\'s display name in its own colours (dark_red name, gold ★, grey ☆☆)',
                  len(cr) == 1 and ('[ MYTHIC ] ' + API.ITEM_NAME, 'dark_red') in cr[0]
                  and star_runs(cr[0]) == [('★', GOLD), ('☆☆', GREY)], cr)
    # the full notice (verbatim) and every string of the generated files = api.EV_TEXT
    files = {rel: (DP / 'data/rlk/function/boss/scarlet' / (rel + '.mcfunction')).read_text(encoding='utf-8')
             for rel in ('ev/title', 'ev/record', 'reward')}
    pieces = set(re.findall(r'text:"([^"]*)"', '\n'.join(files.values())))
    bad = sorted(p for p in pieces if p and not any(p in v for v in T.values()))
    check('G5 every text of ev/title, ev/record and the hook is a piece of api.EV_TEXT (around its numbers / stars)', not bad, bad)
    check('G6 the full-inventory notice verbatim', T['chat_full'] in files['reward'])


# ================================================================================================= scope (F3, HR-11)
def buff_texts(name, seed, consts):
    s, pl = world(seed, name=name, branch='buff', cap=(9, 1))
    for k, v in zip(API.BUFF_FP, consts):
        s.setsc(k, 'tmp', v)
    kill(s)
    fast_forward(s, H_END - 2)
    H.until_sc(s, lambda s: hr(s, '#sqn') == 8, 20, each=H.heal)
    t_h = s.t
    finish(s)
    return titles_of(s, t_h, 'subtitle'), [x for x in titles_of(s, t_h, 'actionbar') if x != ''], tells_of(s, t_h)   # F-I: no HUD_BLANK


def sec_scope():
    words = getattr(API, 'BUFF_SCOPE_WORDS', {'run': ('이번 런 동안', '이번 런'), 'forever': ('영구히', '영구')})
    head = '[월하의 선물] 월하대작 — '
    sub, ab, chat = buff_texts('base', 71, (25, 12, 7))
    want = f'{head}{words["run"][0]} 최종 공격력 +25% · 치명타 확률 +12% · 이동 속도 +7%'
    check('HR-11 run scope, constants retuned to 25 / 12 / 7: the subtitle / actionbar / rift chat show them',
          sub[:1] == ['최종 공격력 +25% · 치명타 확률 +12%'] and ab[:1] == ['이동 속도 +7%'] and want in chat, (sub, ab, chat))
    sub, ab, chat = buff_texts('forever', 72, API.BUFF_VALUES['forever'])
    want = f'{head}{words["forever"][0]} 최종 공격력 +8% · 치명타 확률 +4% · 이동 속도 +4%'
    check('HR-11 the forever switch (api.EVENT buff_scope "forever", dry build) + load\'s 8 / 4 / 4: the rift chat says '
          f'「{words["forever"][0]}」 with 8 / 4 / 4, never 「이번 런」', want in chat and not any('이번 런' in x for x in chat),
          chat)
    var('base')


def main():
    try:
        for sec in SECTIONS:
            globals()[f'sec_{sec}']()
    finally:
        if 'root' in VARS:
            H.drop_variant(VARS.pop('root'))
    return H.summary('test_reward')


if __name__ == '__main__':
    sys.exit(main())
