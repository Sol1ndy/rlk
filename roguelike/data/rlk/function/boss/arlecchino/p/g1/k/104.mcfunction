# G1 pattern tick 104
scoreboard players set #bolw kn 1
execute at @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
execute at @s run playsound minecraft:entity.wither.break_block hostile @a[tag=player] ~ ~ ~ 0.4 1.2 0.13
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 9 1.5 9 0 200 force @a[tag=player]
execute as @e[type=minecraft:item_display,tag=rlk_kn_blade,tag=rlk_kn_p_g1] at @s run execute positioned ~ ~1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.6 1 0.6 0 12 force @a[tag=player]
function rlk:boss/arlecchino/rig_stub/look/glow/normal
