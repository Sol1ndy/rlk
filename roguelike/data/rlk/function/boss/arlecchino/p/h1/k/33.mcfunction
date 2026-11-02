# H1 pattern tick 33
execute as @e[type=minecraft:item_display,tag=rlk_kn_clone,tag=rlk_kn_p_h1] at @s run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.3 0.6 0.3 0 8 force @a[tag=player]
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzBack mb 50
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~40 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:50,w:20,tell:1,dmg:45}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/arlecchino/core/hz_tag/h1
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzBack mb 50
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] rotated ~-40 0 positioned ~ 201 ~ run function rlk:mboss/hz/line {len:50,w:20,tell:1,dmg:45}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/arlecchino/core/hz_tag/h1
