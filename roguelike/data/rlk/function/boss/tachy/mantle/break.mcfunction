# G2 break (@s = body): the cocoon cracks and she drops (mantle_break 40 t), then stunned 120 t taking
# 150 % damage; the player gets 15 energy. The transition follows.
function rlk:boss/tachy/mantle/off
scoreboard players set #pat tk 52
scoreboard players set #pt tk 0
scoreboard players set #sh tk 0
function rlk:boss/tachy/rig_stub/play/mantle_break
execute at @s run playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
execute at @s run playsound minecraft:entity.zombie_villager.cure hostile @a[tag=player] ~ ~ ~ 0.5 0.6 0.17
execute at @s run particle minecraft:end_rod ~ ~1.2 ~ 0.6 0.8 0.6 0.1 40 force @a[tag=player]
scoreboard players set #enAdd tmp 1500
execute as @a[tag=player,limit=1] run function rlk:char/energy_add
function rlk:boss/tachy/hud/sub
