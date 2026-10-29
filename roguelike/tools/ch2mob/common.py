"""Chapter-2 mob framework (owner: swarm side). Writes data/rlk/function/cm/c2/** and the narrow, repeatable hook lines
into the shared chapter-1 cm files, the room spawner and load/uninstall.

Every ch2 brain carries `rlk_c2` (the elite ids get it in cm/c2/stats_chk at mob_init); the swarm ids also carry
`rlk_c2a`. What the framework gives every ch2 mob:
  * cm/c2/world (once a tick, before the brains): per-tick hit limits, the drum haste tags (`rlk_cm_haste` on every cm
    brain within 10 b of a drumming 북잡이, cleared and set again every tick) and the yellow aura on hasted brains.
  * cm/c2/tick (per brain, not while the player is down): age, haste (+1 extra tick on 3 of every 10 ticks while tagged:
    #c2X tmp = 1 on that tick; swarm mobs also get the movement modifier rlk:cm_haste +30 % and the extra cmCd tick),
    then the swarm mob's own `cm/<id>/tick`. The elite ids are dispatched by the elite module's own hook lines
    (elite_lib.HOOKS → cm/tick · cm/vis · cm/flash · cm/clean, installed by the entry).
  * swarm hit feel (cm/c2/hurt): 0.25 s hit stun, knockback 0.42 b/t away from the player, red flash; death fling + pop
    (cm/c2/die, death_tick); multi-kill cue (cm/c2/kill_note from combat/apply) when 3 ch2 mobs die within 10 ticks.
  * chapter-2 room routing: room/mob_wave asks cm/c2/plan for a list of groups by map order, room/mob_summon spawns
    one group per placement through `$function rlk:cm/spawn/$(id)` (resolved at run time, so the elite ids need no
    file here).
"""
import re
from pathlib import Path

import help_lib

A_IDS = ('ns', 'sl', 'ss', 'sp', 'dr')
B_IDS = ('kr', 'nj', 'cc', 'ci')
GROUPS = ('g_ns', 'g_sp', 'g_sl')
# rlk:cm/test {t:"help"} rows of chapter 2 (cm/c2/test_help, tools/help_lib.py): every spawn id with its Korean name
TEST_ROWS = [('ns', '떠돌이 무사 졸개'), ('sl', '번개 슬라임'), ('ss', '작은 번개 슬라임'), ('sp', '반란군 창병'), ('dr', '오니 북잡이'),
             ('kr', '카이라기·뇌전'), ('nj', '그림자 닌자'), ('cc', '번개 시킨 술사'), ('ci', '번개 시킨 (단독, 혼자 돌진)'),
             ('g_ns', '졸개 무리 4~6'), ('g_sp', '창병 대열 3'), ('g_sl', '슬라임 무리 2~3')]

# raw numbers (1st level; the existing level rules scale them)
TUNE = {
    # damage
    'c2D_ns': 15, 'c2D_sl': 12, 'c2D_ss': 6, 'c2D_sp': 16,
    # wind-up / tell (ticks)
    'c2W_ns': 12, 'c2W_sl': 10, 'c2W_ss': 20, 'c2W_sp': 20,
    # attack interval (ticks, from the tell start)
    'c2Cd_ns': 36, 'c2Cd_sl': 50, 'c2Cd_ss': 40, 'c2Cd_sp': 60,
    # hops (ticks between hops), drum interrupt, hit stun, knockback (b/t x1000), spear turn (0.01 deg/tick)
    'c2Hop_sl': 24, 'c2Hop_ss': 11, 'c2DrI': 40, 'c2Stun': 5, 'c2KB': 420, 'c2Turn': 450, 'c2TurnN': -450,
    # chain discharge: % of the target's max HP (small / large slime)
    'c2ZapS': 100, 'c2ZapL': 20,
    # constants
    'c2c1000': 1000, 'c2c100': 100, 'c2c12': 12, 'c2c2': 2, 'c2c4': 4, 'c2c3': 3, 'c2c24': 24,
}
# 1st-level HP and kill xp, by id (the elite rows follow the shared contract; the elite module may change its own)
STATS = {'ns': (8, 2), 'sl': (14, 4), 'ss': (3, 1), 'sp': (10, 3), 'dr': (20, 5),
         'kr': (70, 12), 'nj': (45, 9), 'cc': (50, 10), 'ci': (2, 0)}

VANILLA_SOUNDS = None   # filled by the entry from tools/ch2mob/sounds.txt if present (lint only)


# ---------------------------------------------------------------- writer
class Writer:
    """w(path, text): one function under data/rlk/function/ (path without .mcfunction)."""

    def __init__(self, dp):
        self.dp = Path(dp)
        self.fn = self.dp / 'data' / 'rlk' / 'function'
        self.files = {}
        self.sounds = {}

    def __call__(self, path, text):
        if not re.fullmatch(r'[a-z0-9_./-]+', path):
            raise ValueError('bad function path ' + path)
        if path in self.files:
            raise ValueError('written twice: ' + path)
        text = '\n'.join(l.rstrip() for l in text.strip('\n').split('\n')) + '\n'
        self.files[path] = text

    def has(self, path):
        return path in self.files or (self.fn / (path + '.mcfunction')).exists()

    # one sound per (key) per tick; the snd objective is cleared at the start of every rlk:tick
    def snd(self, key, sound, vol=1.0, pitch=1.0):
        if key not in self.sounds:
            self.sounds[key] = (sound, vol, pitch)
            self(f'cm/c2/snd/{key}', f'scoreboard players set #c2{key} snd 1\nplaysound {sound} hostile @a ~ ~ ~ {vol} {pitch}')
        elif self.sounds[key] != (sound, vol, pitch):
            raise ValueError('sound key reused: ' + key)
        return f'execute unless score #c2{key} snd matches 1 run function rlk:cm/c2/snd/{key}'

    def owned(self, ids):
        """Function files this entry owns (to delete when stale)."""
        out = set()
        base = self.fn / 'cm'
        for d in list(ids) + ['c2']:
            p = base / d
            if p.is_dir():
                out |= {str(f.relative_to(self.fn))[:-len('.mcfunction')] for f in p.rglob('*.mcfunction')}
        for i in list(ids) + list(GROUPS):
            f = base / 'spawn' / (i + '.mcfunction')
            if f.exists():
                out.add('cm/spawn/' + i)
        return out

    def flush(self, owned_ids):
        stale = self.owned(owned_ids) - set(self.files)
        for s in sorted(stale):
            (self.fn / (s + '.mcfunction')).unlink()
        for d in sorted({(self.fn / s).parent for s in stale}, key=lambda p: -len(str(p))):
            while d != self.fn and d.exists() and not any(d.iterdir()):
                d.rmdir()
                d = d.parent
        changed = 0
        for path, text in sorted(self.files.items()):
            f = self.fn / (path + '.mcfunction')
            if f.exists() and f.read_text(encoding='utf-8') == text:
                continue
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(text, encoding='utf-8')
            changed += 1
        return changed, len(stale)


# ---------------------------------------------------------------- shared-file patches (repeatable, anchored)
class Patcher:
    def __init__(self, fn_root):
        self.root = Path(fn_root)
        self.changed = []

    def _rw(self, rel, edit):
        p = self.root / (rel + '.mcfunction')
        s = p.read_text(encoding='utf-8').replace('\r\n', '\n')
        n = edit(s)
        if n != s:
            p.write_text(n, encoding='utf-8')
            self.changed.append(rel)

    def after(self, rel, anchor, line):
        def e(s):
            if line in s.split('\n'):
                return s
            if anchor not in s.split('\n'):
                raise RuntimeError(f'missing patch anchor in {rel}: {anchor}')
            lines = s.split('\n')
            i = lines.index(anchor)
            return '\n'.join(lines[:i + 1] + [line] + lines[i + 1:])
        self._rw(rel, e)

    def before(self, rel, anchor, line):
        def e(s):
            if line in s.split('\n'):
                return s
            if anchor not in s.split('\n'):
                raise RuntimeError(f'missing patch anchor in {rel}: {anchor}')
            lines = s.split('\n')
            i = lines.index(anchor)
            return '\n'.join(lines[:i] + [line] + lines[i:])
        self._rw(rel, e)

    def prefix(self, rel, line):
        self._rw(rel, lambda s: s if line in s.split('\n') else line + '\n' + s)

    def replace_line(self, rel, startswith, line):
        def e(s):
            lines = s.split('\n')
            for i, l in enumerate(lines):
                if l.startswith(startswith):
                    lines[i] = line
                    return '\n'.join(lines)
            raise RuntimeError(f'missing line in {rel}: {startswith}')
        self._rw(rel, e)


# ---------------------------------------------------------------- framework functions
def build(w):
    T = TUNE
    # ---- load / uninstall
    w('cm/c2/load', '\n'.join(
        ['# 2챕터 몹 점수(tools/build_ch2_mobs.py): 무리 · 대열 번호, 역할, 타이머, 가속 주기, 나이'] +
        [f'scoreboard objectives add {o} dummy' for o in ('c2G', 'c2R', 'c2T', 'c2T2', 'c2H', 'c2Age')] +
        ['# 피해(원피해) · 예고(틱) · 간격(틱) · 뛰기 간격 · 북 중단 · 경직 · 넉백(칸/틱 x1000) · 창병 회전(0.01°/틱) · 연쇄 방전(최대 체력 %)'] +
        [f'scoreboard players set #{k} tmp {v}' for k, v in T.items()] +
        ['scoreboard players add #c2PackC tmp 0',
         'execute unless score #c2K1 tmp matches -2147483648.. run scoreboard players set #c2K1 tmp -1000',
         'execute unless score #c2K2 tmp matches -2147483648.. run scoreboard players set #c2K2 tmp -1000',
         'execute unless score #c2Kq tmp matches -2147483648.. run scoreboard players set #c2Kq tmp -1000']))
    w('cm/c2/uninstall', '\n'.join(f'scoreboard objectives remove {o}' for o in ('c2G', 'c2R', 'c2T', 'c2T2', 'c2H', 'c2Age')))

    # ---- world pass
    w('cm/c2/world', f'''
# 2챕터 몹 공용, 매 틱 두뇌보다 먼저 (cm/world). 한 틱 피격 제한 · 북 가속 표시 · 가속 기운
scoreboard players set #c2NsHit tmp 0
scoreboard players set #c2SpHit tmp 0
execute if entity @e[tag=rlk_c2fresh,limit=1] run tag @e[tag=rlk_c2fresh] remove rlk_c2fresh
scoreboard players add #c2Clk tmp 1
execute if score #c2Clk tmp matches 20.. run scoreboard players set #c2Clk tmp 0
execute unless entity @e[tag=rlk_c2vec,limit=1] at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {{Tags:["rlk_c2vec","rlk_cmglob"]}}
# 북잡이가 북을 치는 동안 10칸 안의 모든 커스텀 몹(북잡이 제외)에 rlk_cm_haste. 매 틱 지우고 다시 붙인다
execute if entity @e[tag=rlk_cm_haste,limit=1] run tag @e[tag=rlk_cm_haste] remove rlk_cm_haste
execute as @e[tag=rlk_dr_drum] at @s run tag @e[tag=rlk_cmb,tag=!rlk_cm_dr,distance=..10] add rlk_cm_haste
scoreboard players operation #c2m tmp = #c2Clk tmp
scoreboard players operation #c2m tmp %= #c2c4 tmp
execute if score #c2m tmp matches 0 as @e[tag=rlk_cm_haste] at @s run particle minecraft:dust{{color:[1.0,0.82,0.18],scale:1.2}} ~ ~0.9 ~ 0.35 0.55 0.35 0 4 normal
execute if score #c2m tmp matches 2 as @e[tag=rlk_cm_haste] at @s run particle minecraft:wax_on ~ ~1.1 ~ 0.3 0.5 0.3 0 1 normal
''')

    # ---- per-brain tick (A and B); dispatch lines are added in finish()
    w('cm/c2/haste_on', '''
# 북 가속 중 (@s = 두뇌): 10틱마다 3틱은 한 틱 더(#c2X 1) = 타이머 x1.3. 무리 몹은 이동 +30%(rlk:cm_haste)와 쿨타임 한 틱 더
scoreboard players add @s c2H 1
execute if score @s c2H matches 10.. run scoreboard players set @s c2H 0
execute if score @s c2H matches 2 run scoreboard players set #c2X tmp 1
execute if score @s c2H matches 5 run scoreboard players set #c2X tmp 1
execute if score @s c2H matches 8 run scoreboard players set #c2X tmp 1
execute if entity @s[tag=rlk_c2a,tag=!rlk_c2hm] run function rlk:cm/c2/haste_add
execute if score #c2X tmp matches 1 if entity @s[tag=rlk_c2a] if score @s cmCd matches 1.. run scoreboard players remove @s cmCd 1
''')
    w('cm/c2/haste_add', '''
attribute @s minecraft:movement_speed modifier add rlk:cm_haste 0.3 add_multiplied_base
tag @s add rlk_c2hm
''')
    w('cm/c2/haste_off', '''
attribute @s minecraft:movement_speed modifier remove rlk:cm_haste
tag @s remove rlk_c2hm
scoreboard players set @s c2H 0
''')
    w('cm/c2/first', '''
# 처음 한 번(@s = 무리 몹 두뇌, mob/setup 뒤): 넉백 저항 0
attribute @s minecraft:knockback_resistance base set 0
''')

    # ---- swarm hit feel
    w('cm/c2/hurt', f'''
# 무리 몹이 맞음 (@s = 두뇌, at @s, combat/apply 의 cm/flash 에서): 0.25초 경직 · 멀리 밀림 · 붉게 번쩍
scoreboard players set @s cmAH 5
execute if score @s stunT matches 1.. run scoreboard players operation @s stunT = #c2Stun tmp
execute if score #stunHit tmp matches 1 run function rlk:cm/c2/knock
execute unless score #stunHit tmp matches 1 if score #basic itv matches 1 run function rlk:cm/c2/knock
scoreboard players operation #fid tmp = @s cmId
execute as @e[tag=rlk_c2pt,distance=..6] if score @s cmId = #fid tmp run data modify entity @s item.components."minecraft:custom_model_data" set value {{colors:[16737903]}}
execute if entity @s[tag=rlk_cm_dr] run function rlk:cm/dr/interrupt
execute if entity @s[tag=rlk_c2slime] run {w.snd('shurt', 'minecraft:entity.slime.hurt', 0.7, 1.3)}
''')
    w('cm/c2/knock', '''
# 몸에서 멀어지는 쪽으로 #c2KB(칸/틱 x1000) + 땅에 있으면 살짝 띄움
execute unless entity @e[tag=rlk_body,limit=1] run return 0
scoreboard players operation #c2Fw tmp = #c2KB tmp
scoreboard players set #c2Up tmp -1
execute if data entity @s {OnGround:1b} run scoreboard players set #c2Up tmp 220
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 run function rlk:cm/c2/impulse
''')
    w('cm/c2/vec', '''
# 실행 방향의 수평 단위 벡터 x1000 → #c2vx #c2vz (실행 위치 기준, 표식 rlk_c2vec 한 개를 옮겨 잼)
execute unless entity @e[tag=rlk_c2vec,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_c2vec","rlk_cmglob"]}
tp @e[tag=rlk_c2vec,limit=1] ^ ^ ^1
execute store result score #c2vx tmp run data get entity @e[tag=rlk_c2vec,limit=1] Pos[0] 1000
execute store result score #c2vz tmp run data get entity @e[tag=rlk_c2vec,limit=1] Pos[2] 1000
tp @e[tag=rlk_c2vec,limit=1] ~ ~ ~
execute store result score #c2t tmp run data get entity @e[tag=rlk_c2vec,limit=1] Pos[0] 1000
scoreboard players operation #c2vx tmp -= #c2t tmp
execute store result score #c2t tmp run data get entity @e[tag=rlk_c2vec,limit=1] Pos[2] 1000
scoreboard players operation #c2vz tmp -= #c2t tmp
''')
    w('cm/c2/impulse', '''
# @s 의 속도 = 실행 방향 x #c2Fw/1000 칸/틱, 위로 #c2Up/1000 (#c2Up < 0 이면 세로 속도는 그대로). 블록 충돌은 바닐라 물리가 맡음
function rlk:cm/c2/vec
scoreboard players operation #c2vx tmp *= #c2Fw tmp
scoreboard players operation #c2vx tmp /= #c2c1000 tmp
scoreboard players operation #c2vz tmp *= #c2Fw tmp
scoreboard players operation #c2vz tmp /= #c2c1000 tmp
execute store result entity @s Motion[0] double 0.001 run scoreboard players get #c2vx tmp
execute store result entity @s Motion[2] double 0.001 run scoreboard players get #c2vz tmp
execute if score #c2Up tmp matches 0.. store result entity @s Motion[1] double 0.001 run scoreboard players get #c2Up tmp
''')
    w('cm/c2/safe_here', '''
# 몹이 설 수 있는 자리인가(실행 위치 = 발): 발 · 머리 칸이 비고 발밑이 막혀 있음. 2챕터 집 · 가게 안(가문비나무 판자 바닥)은 안 됨
execute unless block ~ ~ ~ #rlk:dash_pass run return 0
execute unless block ~ ~1 ~ #rlk:dash_pass run return 0
execute if block ~ ~-1 ~ #rlk:dash_pass run return 0
execute if score #th room matches 4 if block ~ ~-1 ~ minecraft:spruce_planks run return 0
return 1
''')
    w('cm/c2/hit_el', '''
# 번개 원소 근접 판정 (@s = 두뇌): #cmDmg 설정 후 호출. 플레이어에게 번개가 부착됨
scoreboard players set #cmEl tmp 3
scoreboard players operation #cmLv tmp = @s mlv
function rlk:cm/hit_pl
''')
    w('cm/c2/cancel', '''
# 하던 공격 취소 (@s = 무리 몹 두뇌, cm/cancel 에서): 빛나는 무기 · 바닥 고리 정리
execute as @e[tag=rlk_c2glow,distance=..6] if score @s cmId = #cid tmp run data merge entity @s {Glowing:0b}
execute as @e[tag=rlk_c2ring,distance=..6] if score @s cmId = #cid tmp run kill @s
scoreboard players set @s cmT 0
''')
    w('cm/c2/rig_frozen', '''
# 빙결: 지금 자세 그대로, 피격 번쩍임만 풀림
execute if score @s cmAH matches 1.. run scoreboard players remove @s cmAH 1
tag @e[tag=rlk_c2this] remove rlk_c2this
''')

    # ---- death: fling back + pop
    w('cm/c2/clean', '''
# 2챕터 무리 몹 모습 정리 (cm/clean 맨 앞): 두뇌가 사라진 리그 → 날아가며 터짐. 쓰러지는 리그는 ch1 정리에서 살려 둠
execute as @e[tag=rlk_c2root,tag=!rlk_cmsync,tag=!rlk_c2dying] at @s run function rlk:cm/c2/die
execute as @e[tag=rlk_c2root,tag=rlk_c2dying] at @s run function rlk:cm/c2/death_tick
execute if entity @e[tag=rlk_c2dying,limit=1] run tag @e[tag=rlk_c2dying] add rlk_cmsync
''')
    die = [
        '# 두뇌가 없어진 리그(@s = 뿌리 부품, at @s): 같은 cmId 부품을 쓰러지는 모습으로, 몸 쪽을 보게 돌린 뒤 뒤로 날림',
        'scoreboard players operation #did tmp = @s cmId',
        'execute as @e[tag=rlk_c2pt,tag=!rlk_c2dying,distance=..6] if score @s cmId = #did tmp run tag @s add rlk_c2this',
        'tag @e[tag=rlk_c2this] add rlk_c2dying',
        'execute as @e[tag=rlk_c2this] run data modify entity @s item.components."minecraft:custom_model_data" set value {colors:[16777215]}',
        'execute as @e[tag=rlk_c2this,tag=rlk_c2glow] run data merge entity @s {Glowing:0b}',
        'execute if entity @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 as @e[tag=rlk_c2this] run tp @s ~ ~ ~ ~ 0',
        'scoreboard players set @s cmAD 0',
        'scoreboard players set @s c2T2 0',
    ]
    for i in A_IDS:
        die.append(f'execute if entity @s[tag=rlk_{i}_pt] run function rlk:cm/{i}/rig/die')
    die += [w.snd('kill', 'minecraft:entity.player.attack.strong', 1.0, 0.75),
            'tag @e[tag=rlk_c2this] remove rlk_c2this']
    w('cm/c2/die', '\n'.join(die))
    dt = [
        '# 쓰러지는 리그 한 틱 (@s = 뿌리, at @s). 1~6틱: 뒤로 0.32칸씩(앞이 비었을 때만) · 포물선(올라간 만큼만 내려옴 → 처음 높이 아래로는 안 감), 8틱: 터짐',
        'scoreboard players add @s cmAD 1',
        'scoreboard players operation #did tmp = @s cmId',
        'execute as @e[tag=rlk_c2dying,distance=..6] if score @s cmId = #did tmp run tag @s add rlk_c2this',
        'scoreboard players set #c2ok tmp 0',
        'execute if score @s cmAD matches 1..6 positioned ^ ^ ^-0.32 if block ~ ~0.2 ~ #rlk:cm_pass if block ~ ~1.2 ~ #rlk:cm_pass run scoreboard players set #c2ok tmp 1',
        'execute if score #c2ok tmp matches 1 as @e[tag=rlk_c2this,tag=!rlk_c2still] at @s run tp @s ^ ^ ^-0.32',
    ]
    for t, d in ((1, 26), (2, 16), (3, 6)):
        dt.append(f'execute if score @s cmAD matches {t} if block ~ ~2.4 ~ #rlk:cm_pass as @e[tag=rlk_c2this,tag=!rlk_c2still] at @s run tp @s ~ ~0.{d:02d} ~')
        dt.append(f'execute if score @s cmAD matches {t} if block ~ ~2.4 ~ #rlk:cm_pass run scoreboard players add @s c2T2 {d}')
    for t, d in ((4, 6), (5, 16), (6, 26)):
        dt.append(f'execute if score @s cmAD matches {t} if score @s c2T2 matches {d}.. as @e[tag=rlk_c2this,tag=!rlk_c2still] at @s run tp @s ~ ~-0.{d:02d} ~')
        dt.append(f'execute if score @s cmAD matches {t} if score @s c2T2 matches {d}.. run scoreboard players remove @s c2T2 {d}')
    for i in A_IDS:
        dt.append(f'execute if score @s cmAD matches 3 if entity @s[tag=rlk_{i}_pt] run function rlk:cm/{i}/rig/fling')
    dt += ['execute if score @s cmAD matches 8.. run function rlk:cm/c2/pop',
           'tag @e[tag=rlk_c2this] remove rlk_c2this']
    w('cm/c2/death_tick', '\n'.join(dt))
    w('cm/c2/pop', f'''
# 터짐: 연기 · 번개 불꽃 · 소리, 부품 제거
particle minecraft:poof ~ ~0.8 ~ 0.3 0.4 0.3 0.06 14 normal
particle minecraft:electric_spark ~ ~0.8 ~ 0.35 0.45 0.35 0.35 12 normal
particle minecraft:crit ~ ~0.9 ~ 0.3 0.4 0.3 0.4 10 normal
{w.snd('pop', 'minecraft:entity.firework_rocket.blast', 0.7, 1.5)}
kill @e[tag=rlk_c2this]
''')

    # ---- multi-kill cue (combat/apply → kill_note, @s = dying ch2 brain)
    w('cm/c2/kill_note', '''
# 2챕터 몹 처치 기록 (@s = 죽는 두뇌, combat/apply 에서). 10틱 안에 3마리 → 다중 처치 신호. 큰 슬라임은 분열할 레벨을 리그에 남김
execute store result score #c2Now tmp run time query gametime
execute if entity @s[tag=rlk_cm_sl] run function rlk:cm/sl/keep_lv
scoreboard players operation #c2Dt tmp = #c2Now tmp
scoreboard players operation #c2Dt tmp -= #c2K2 tmp
scoreboard players operation #c2K2 tmp = #c2K1 tmp
scoreboard players operation #c2K1 tmp = #c2Now tmp
execute if score #c2Dt tmp matches ..10 run function rlk:cm/c2/multi
''')
    w('cm/c2/multi', f'''
# 다중 처치: 몸 위치에 묵직한 소리 + 터지는 입자 (한 번 울리면 10틱 동안은 다시 안 울림)
scoreboard players operation #c2Dq tmp = #c2Now tmp
scoreboard players operation #c2Dq tmp -= #c2Kq tmp
execute if score #c2Dq tmp matches ..10 run return 0
scoreboard players operation #c2Kq tmp = #c2Now tmp
scoreboard players add #c2Multi tmp 1
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:item.mace.smash_ground_heavy master @a ~ ~ ~ 1 0.8
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.player.attack.crit master @a ~ ~ ~ 1 0.6
execute at @e[tag=rlk_body,limit=1] run particle minecraft:sweep_attack ~ ~1 ~ 0.9 0.3 0.9 0 6 normal
execute at @e[tag=rlk_body,limit=1] run particle minecraft:crit ~ ~1 ~ 0.8 0.5 0.8 0.6 30 normal
execute at @e[tag=rlk_body,limit=1] run particle minecraft:electric_spark ~ ~1 ~ 0.9 0.5 0.9 0.5 20 normal
''')

    # ---- slime discharge (never the player)
    w('cm/c2/discharge', f'''
# 슬라임이 터짐 (@s = 뿌리, at @s): 2칸 안의 다른 슬라임 두뇌에만 방전(플레이어는 대상이 아님)
particle minecraft:electric_spark ~ ~0.5 ~ 1.0 0.3 1.0 0.25 24 normal
{w.snd('zap', 'minecraft:block.amethyst_cluster.break', 0.9, 1.5)}
execute as @e[tag=rlk_c2slime,tag=rlk_cmb,distance=..2] at @s run function rlk:cm/c2/zap_one
''')
    w('cm/c2/zap_one', '''
# 방전 한 대 (@s = 맞는 슬라임 두뇌): 작은 슬라임 = 최대 체력의 #c2ZapS %, 큰 슬라임 #c2ZapL %. 진짜 피해(원소 · 보정 없음, 면역 없음)
scoreboard players operation #c2zd tmp = @s mhpM
execute if entity @s[tag=rlk_cm_ss] run scoreboard players operation #c2zd tmp *= #c2ZapS tmp
execute unless entity @s[tag=rlk_cm_ss] run scoreboard players operation #c2zd tmp *= #c2ZapL tmp
scoreboard players operation #c2zd tmp /= #c2c100 tmp
execute if score #c2zd tmp matches ..0 run scoreboard players set #c2zd tmp 1
particle minecraft:electric_spark ~ ~0.6 ~ 0.2 0.3 0.2 0.2 8 normal
function rlk:cm/c2/true_hit
''')
    w('cm/c2/true_hit', '''
# @s 에게 진짜 피해 #c2zd (combat/apply 경로: 처치 · 보상 · 숫자). combat/apply 안에서는 부르지 않는다(cm/clean 에서만)
scoreboard players add #hitLanded tmp 0
scoreboard players operation #c2SaveHL tmp = #hitLanded tmp
scoreboard players add #basic itv 0
scoreboard players operation #c2SaveB tmp = #basic itv
function rlk:combat/clear_atkflags
scoreboard players operation #dmg tmp = #c2zd tmp
scoreboard players set #crit tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #basic itv 0
scoreboard players set #bowHit tmp 0
scoreboard players set #elem tmp 3
scoreboard players set #tfm tmp 1
scoreboard players set #trueDmg tmp 1
function rlk:combat/apply
scoreboard players set #trueDmg tmp 0
scoreboard players set #tfm tmp 0
scoreboard players operation #hitLanded tmp = #c2SaveHL tmp
scoreboard players operation #basic itv = #c2SaveB tmp
''')

    # ---- spawning helpers
    w('cm/c2/brain_end', '''
# 새 두뇌 마무리 (@e[tag=rlk_cmnew]): cmId, 실행 방향을 두뇌의 방향으로, cm/init
scoreboard players add #cmIdC tmp 1
scoreboard players operation @e[tag=rlk_cmnew] cmId = #cmIdC tmp
tp @e[tag=rlk_cmnew] ~ ~ ~ ~ 0
execute as @e[tag=rlk_cmnew] at @s run function rlk:cm/init
''')
    w('cm/c2/child_init', '''
# 분열로 생긴 몹 (@s): 방 몹 준비 뒤 부모 레벨(#c2PLv)로 맞춤
function rlk:room/mob_init
execute if score #c2PLv tmp matches 1.. run scoreboard players operation @s mlv = #c2PLv tmp
function rlk:mob/level_apply
''')
    # stats (room/mob_init hook)
    st = ['# 2챕터 몹 1레벨 체력 · 처치 경험치 (@s = 새 두뇌, room/mob_init 에서). 정예 id 도 여기서 rlk_c2 를 받음']
    for i in B_IDS:
        st.append(f'execute if entity @s[tag=rlk_cm_{i}] run tag @s add rlk_c2')
    st.append('execute if entity @s[tag=rlk_c2] run function rlk:cm/c2/stats')
    w('cm/c2/stats_chk', '\n'.join(st))
    st = ['scoreboard players set #mad tmp 0']
    for i, (hp, xp) in STATS.items():
        st.append(f'execute if entity @s[tag=rlk_cm_{i}] run scoreboard players set #mhp tmp {hp}')
        st.append(f'execute if entity @s[tag=rlk_cm_{i}] run scoreboard players set @s xpDrop {xp}')
    w('cm/c2/stats', '\n'.join(st))

    # ---- room plan + slot spawner
    w('cm/c2/plan', '''
# 2챕터 방 구성 (@s = 구역 표식, room/mob_wave 에서). #mobN(방 크기 규칙의 수) → 무리 목록 rlk:c2 plan, #mobN = 무리 수
data modify storage rlk:c2 plan set value []
scoreboard players operation #c2N tmp = #mobN tmp
execute if score #c2N tmp matches ..2 run function rlk:cm/c2/plan_small
execute if score #c2N tmp matches 3.. if score #mapIdx room matches ..1 run function rlk:cm/c2/plan_a
execute if score #c2N tmp matches 3.. if score #mapIdx room matches 2..3 run function rlk:cm/c2/plan_b
execute if score #c2N tmp matches 3.. if score #mapIdx room matches 4.. run function rlk:cm/c2/plan_c
execute store result score #mobN tmp run data get storage rlk:c2 plan
''')
    w('cm/c2/plan_add', '''
$data modify storage rlk:c2 plan append value {id:"$(id)",n:0}
execute store result storage rlk:c2 plan[-1].n int 1 run scoreboard players get #c2n tmp
''')
    w('cm/c2/plan_small', '''
# 아주 작은 방: 무리 하나(5~6번째 맵은 창병 대열)
execute store result score #c2r tmp run random value 1..2
scoreboard players set #c2n tmp 4
execute if score #mapIdx room matches ..3 if score #c2r tmp matches 1 run return run function rlk:cm/c2/plan_add {id:"g_ns"}
scoreboard players set #c2n tmp 2
execute if score #mapIdx room matches ..3 run return run function rlk:cm/c2/plan_add {id:"g_sl"}
scoreboard players set #c2n tmp 3
function rlk:cm/c2/plan_add {id:"g_sp"}
''')
    w('cm/c2/plan_a', '''
# 1~2번째 맵: 졸개 무리 + 번개 슬라임 (방이 클수록 무리가 커짐)
scoreboard players set #c2n tmp 4
execute if score #c2N tmp matches 5.. run scoreboard players add #c2n tmp 1
execute if score #c2N tmp matches 7.. run scoreboard players add #c2n tmp 1
function rlk:cm/c2/plan_add {id:"g_ns"}
scoreboard players set #c2n tmp 2
execute if score #c2N tmp matches 6.. run scoreboard players set #c2n tmp 3
function rlk:cm/c2/plan_add {id:"g_sl"}
''')
    w('cm/c2/plan_b', '''
# 3~4번째 맵: 무리 1~2 + 정예 하나(카이라기 · 시킨 술사) + 가끔(35%) 북잡이
execute store result score #c2r tmp run random value 1..2
scoreboard players set #c2n tmp 4
execute if score #c2N tmp matches 7.. run scoreboard players set #c2n tmp 5
execute if score #c2N tmp matches 5.. run function rlk:cm/c2/plan_add {id:"g_ns"}
execute if score #c2N tmp matches ..4 if score #c2r tmp matches 1 run function rlk:cm/c2/plan_add {id:"g_ns"}
scoreboard players set #c2n tmp 2
execute if score #c2N tmp matches 5.. run function rlk:cm/c2/plan_add {id:"g_sl"}
execute if score #c2N tmp matches ..4 if score #c2r tmp matches 2 run function rlk:cm/c2/plan_add {id:"g_sl"}
scoreboard players set #c2n tmp 1
execute store result score #c2r tmp run random value 1..2
execute if score #c2r tmp matches 1 run function rlk:cm/c2/plan_add {id:"kr"}
execute if score #c2r tmp matches 2 run function rlk:cm/c2/plan_add {id:"cc"}
execute store result score #c2r tmp run random value 1..100
execute if score #c2r tmp matches ..35 run function rlk:cm/c2/plan_add {id:"dr"}
''')
    w('cm/c2/plan_c', '''
# 5~6번째 맵: 창병 대열 + 졸개 무리 + 정예 하나(그림자 닌자 50%, 카이라기 · 시킨 술사 25%씩) + 북잡이 60%, 아주 큰 방은 슬라임도
scoreboard players set #c2n tmp 3
function rlk:cm/c2/plan_add {id:"g_sp"}
scoreboard players set #c2n tmp 4
execute if score #c2N tmp matches 7.. run scoreboard players set #c2n tmp 5
function rlk:cm/c2/plan_add {id:"g_ns"}
scoreboard players set #c2n tmp 1
execute store result score #c2r tmp run random value 1..4
execute if score #c2r tmp matches 1..2 run function rlk:cm/c2/plan_add {id:"nj"}
execute if score #c2r tmp matches 3 run function rlk:cm/c2/plan_add {id:"kr"}
execute if score #c2r tmp matches 4 run function rlk:cm/c2/plan_add {id:"cc"}
execute store result score #c2r tmp run random value 1..100
execute if score #c2r tmp matches ..60 run function rlk:cm/c2/plan_add {id:"dr"}
scoreboard players set #c2n tmp 2
execute if score #c2N tmp matches 8.. run function rlk:cm/c2/plan_add {id:"g_sl"}
''')
    w('cm/c2/room_slot', f'''
# 2챕터 방 몹: 계획(rlk:c2 plan)의 맨 앞 무리를 실행 위치에 (room/mob_summon 에서). 몸 쪽을 보고 선다
execute unless data storage rlk:c2 plan[0] run data modify storage rlk:c2 plan append value {{id:"g_ns",n:4}}
data modify storage rlk:c2 cur set from storage rlk:c2 plan[0]
data remove storage rlk:c2 plan[0]
execute store result score #c2Size tmp run data get storage rlk:c2 cur.n
scoreboard players set #c2SizeSet tmp 1
execute if entity @e[tag=rlk_body,limit=1] facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:cm/c2/spawn_id with storage rlk:c2 cur
execute unless entity @e[tag=rlk_body,limit=1] run function rlk:cm/c2/spawn_id with storage rlk:c2 cur
scoreboard players set #c2SizeSet tmp 0
execute as @e[tag=rlk_newmob] run function rlk:room/mob_init
particle minecraft:poof ~ ~1 ~ 0.6 0.6 0.6 0.02 16
{w.snd('arrive', 'minecraft:entity.zombie.infect', 0.5, 0.8)}
''')
    w('cm/c2/spawn_id', '''
# 소환 id 를 실행 시점에 풀어 부름 (정예 id 는 다른 쪽 파일이라 직접 참조하지 않음)
$function rlk:cm/spawn/$(id)
''')


# ---------------------------------------------------------------- dispatch + shared-file hooks
def finish(w):
    """The swarm dispatchers. The elite ids are wired by their own module's hook lines (elite_lib.install_hooks, called
    by the entry when ch2mob/elite.py exists); the framework only gives them rlk_c2 (stats_chk), the drum haste tag,
    #c2X on cm/c2/tick and the multi-kill note."""
    tick = ['# 2챕터 두뇌 한 틱 (@s, at @s; cm/tick 에서, 플레이어가 쓰러져 있지 않을 때). #c2X = 이번 틱 가속 한 틱 더',
            'scoreboard players add @s c2Age 1',
            'scoreboard players set #c2X tmp 0',
            'execute if entity @s[tag=rlk_cm_haste] run function rlk:cm/c2/haste_on',
            'execute if entity @s[tag=rlk_c2hm,tag=!rlk_cm_haste] run function rlk:cm/c2/haste_off',
            'execute if score @s c2Age matches 1 if entity @s[tag=rlk_c2a] run function rlk:cm/c2/first']
    init = ['# 2챕터 두뇌 준비 (@s = 새 두뇌, at @s; cm/init 끝에서, #cid = cmId)',
            'scoreboard players set @s c2Age 0',
            'scoreboard players set @s c2H 0',
            'scoreboard players set @s cmAH 0',
            'scoreboard players set @s cmAR 0',
            'scoreboard players set @s cmAP -1',
            'execute store result score @s cmAF run random value 0..47']
    vis = []
    for i in A_IDS:
        tick.append(f'execute if entity @s[tag=rlk_cm_{i}] run return run function rlk:cm/{i}/tick')
        init.append(f'execute if entity @s[tag=rlk_cm_{i}] run return run function rlk:cm/{i}/init')
        vis.append(f'execute if entity @s[tag=rlk_cm_{i}] run return run function rlk:cm/{i}/rig/tick')
    w('cm/c2/tick', '\n'.join(tick))
    w('cm/c2/init', '\n'.join(init))
    w('cm/c2/vis', '# 무리 몹 모습 (@s = 두뇌, at @s; cm/vis 맨 앞)\n' + '\n'.join(vis))
    # {t:"help"} of rlk:cm/test: this chapter's section of cm/test_help (patch_shared rewrites cm/test_help after the flush)
    assert [i for i, _ in TEST_ROWS] == list(A_IDS + B_IDS + GROUPS), 'TEST_ROWS must list every chapter-2 spawn id'
    w(help_lib.CM_SECTION.format(n=2), help_lib.cm_test_section(2, TEST_ROWS))


def patch_shared(fn_root):
    P = Patcher(fn_root)
    # cm: brains, visuals, hurt flash, init, cancel, clean, world
    P.after('cm/tick', 'execute if score #cmDown tmp matches 0 if entity @s[tag=rlk_cm_cn] run function rlk:cm/cn/tick',
            'execute if score #cmDown tmp matches 0 if entity @s[tag=rlk_c2] run function rlk:cm/c2/tick')
    P.prefix('cm/vis', 'execute if entity @s[tag=rlk_c2a] run return run function rlk:cm/c2/vis')
    P.prefix('cm/flash', 'execute if entity @s[tag=rlk_c2a] run return run function rlk:cm/c2/hurt')
    P.after('cm/init', 'execute if entity @s[tag=rlk_cm_sh] run function rlk:cm/sh/rig/rebuild',
            'execute if entity @s[tag=rlk_c2] run function rlk:cm/c2/init')
    P.after('cm/cancel', 'function rlk:cm/pose_s', 'execute if entity @s[tag=rlk_c2a] run function rlk:cm/c2/cancel')
    P.prefix('cm/clean', 'function rlk:cm/c2/clean')
    P.before('cm/world', 'execute as @e[tag=rlk_cmb] at @s run function rlk:cm/tick',
             'execute if entity @e[tag=rlk_c2,limit=1] run function rlk:cm/c2/world')
    P.replace_line('cm/test', '# 시험용: /function rlk:cm/test',
                   '# 시험용: /function rlk:cm/test {t:"sw"} — 바라보는 쪽 5칸 앞에 1레벨로. 쓸 수 있는 id: {t:"help"} '
                   '(cm/test_help: tools/help_lib.py 의 1챕터 목록 + 챕터마다 몹 생성기가 쓰는 cm/c<N>/test_help)')
    # combat: multi-kill note, lighter rewards for the small fry (ss, half the 졸개)
    P.before('combat/apply', 'execute if score #mobHP tmp matches ..0 run function rlk:combat/heal_orb_roll',
             'execute if score #mobHP tmp matches ..0 if entity @s[tag=rlk_c2] run function rlk:cm/c2/kill_note')
    P.after('combat/gold_drop', 'execute if entity @s[tag=rlk_lobby] run return 0', 'execute if entity @s[tag=rlk_c2lite] run return 0')
    P.after('combat/heal_orb_roll', 'execute if entity @s[tag=rlk_lobby] run return 0', 'execute if entity @s[tag=rlk_c2lite] run return 0')
    # room: chapter-2 roster (chapter 1 and 3+ unchanged; #mobTmp 1 still means the old temporary mobs from chapter 2 on)
    P.before('room/mob_summon', 'execute unless score #mobTmp room matches 1 run return run function rlk:cm/summon_c1',
             'execute if score #chapter room matches 2 unless score #mobTmp room matches 1 run return run function rlk:cm/c2/room_slot')
    P.before('room/mob_wave', 'function rlk:room/mob_loop',
             'execute if score #chapter room matches 2 unless score #mobTmp room matches 1 run function rlk:cm/c2/plan')
    P.before('room/mob_init', '# 레벨 = (챕터 - 1) × 6 + 이번 맵의 순서(1~6). 체력은 레벨에 따라 늘어남(mob/level_apply), 공격력은 맞을 때 레벨로 보정',
             'execute if entity @s[tag=rlk_cmb] run function rlk:cm/c2/stats_chk')
    # load / uninstall
    P.after('load', 'team modify rlk_cmx collisionRule never', 'function rlk:cm/c2/load')
    P.after('uninstall', 'scoreboard objectives remove cmAD', 'function rlk:cm/c2/uninstall')
    # cm/test {t:"help"}: the list from chapter 1 + every cm/c<N>/test_help on disk (any chapter generator may rewrite it)
    if help_lib.cm_test_help(P.root):
        P.changed.append('cm/test_help')
    return P.changed
