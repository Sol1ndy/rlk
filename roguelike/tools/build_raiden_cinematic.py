"""Camera entry points and the death flow of the Narukami encounter (owner S2-TENMA, plan rd/plan.md E.0).

만겁 is the footage version (plan §F.2.1, user decision): a free camera and an arena-wide slash, so the cinematic camera
lock is gone. camera/hold (called by view/tick while a player's rdCam is 1) and camera/release_all stay as entry points;
they only drop a stale lock that a fight saved by an older build may have left behind.

Death (plan A.1): at HP 0 in any non-immune state; the `death` clip (48 t, keeps the form) and the line
「그 무엇도 영원한 것은 없다.」, then the cleanup.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'data/rlk/function/boss/raiden'


def write(name, content):
    p = BASE / (name + '.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip() + '\n', encoding='utf-8')


write('camera/hold', '''
# No camera lock any more (만겁 footage version, free camera). view/tick calls this while @s (a player) has rdCam 1,
# which only a fight saved by an older build can leave behind: drop the flag and the camera seat.
scoreboard players set @s rdCam 0
ride @s dismount
''')
write('camera/release_all', '''
# No camera lock any more; kept as the entry point init / pause / finish / cleanup call.
execute as @a[scores={rdCam=1}] run function rlk:boss/raiden/camera/hold
''')
write('death/start', '''
# The first lethal hit already awarded loot. Keep the brain alive only for the death clip (it keeps the current form).
execute if score @s rdDeath matches 1 run return 0
scoreboard players set @s rdDeath 1
scoreboard players set @s rdDeathTime 0
scoreboard players set @s mhpC 0
scoreboard players set @s rdPat 0
scoreboard players set @s rdTime 0
scoreboard players set @s rdBlink 0
scoreboard players set @s rdWalk 0
scoreboard players set @s rdGo 0
function rlk:boss/raiden/illusion/cleanup
function rlk:boss/raiden/movement/cleanup
function rlk:boss/raiden/object/clear
function rlk:boss/raiden/object_vfx/clear
kill @e[tag=rlk_rd_tmp]
function rlk:boss/raiden/hazard/clear
kill @e[tag=rlk_rd_dome]
kill @e[tag=rlk_rd_sfx]
kill @e[tag=rlk_rd_clap]
kill @e[tag=rlk_rd_shadow]
execute on passengers run kill @s
# The fight is won: both boss bars disappear now, not after the collapse.
bossbar set rlk:narukami value 0
function rlk:boss/raiden/bars_hide
function rlk:boss/raiden/caption/clear
function rlk:boss/raiden/line/nothing
playsound minecraft:entity.iron_golem.death hostile @a[tag=player] ~ ~ ~ .7 .7 .3
function rlk:boss/raiden/rig/start/death
''')
write('death/tick', '''
function rlk:boss/raiden/line/tick
scoreboard players add @s rdDeathTime 1
data merge entity @s {Motion:[0d,0d,0d],Health:1024f,Fire:-1s}
execute if score @s rdDeathTime matches 48.. run return run function rlk:boss/raiden/death/finish
function rlk:boss/raiden/rig/tick
''')
write('death/finish', '''
function rlk:boss/raiden/cleanup
function rlk:room/raiden/look_shogun
kill @s
''')
print('Generated the camera entry points and the death flow.')
