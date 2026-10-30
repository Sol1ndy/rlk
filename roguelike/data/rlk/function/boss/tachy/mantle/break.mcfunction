# G2 break (@s = body): the cocoon cracks and she drops (mantle_break 40 t), then stunned 120 t taking
# 150 % damage; the player gets 15 energy. The transition follows.
function rlk:boss/tachy/mantle/off
scoreboard players set #pat tk 52
scoreboard players set #pt tk 0
scoreboard players set #sh tk 0
function rlk:boss/tachy/rig/play/mantle_break
execute at @s run function rlk:boss/tachy/fx/snd/mantle_break
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.5 ~ run function rlk:boss/tachy/fx/p/cocoon_crack
scoreboard players set #enAdd tmp 1500
execute as @a[tag=player,limit=1] run function rlk:char/energy_add
function rlk:boss/tachy/hud/sub
