# F1 pattern tick 196
scoreboard players set #bolw kn 1
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run particle minecraft:explosion ~ ~ ~ 6 0.5 6 0 24 force @a[tag=player]
execute at @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
execute at @s run playsound minecraft:entity.wither.break_block hostile @a[tag=player] ~ ~ ~ 0.4 1.2 0.13
execute at @s run playsound minecraft:block.basalt.break hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
function rlk:boss/arlecchino/rig_stub/look/glow/normal
