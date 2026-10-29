# K stage gl tick 15
scoreboard players set #t tk 12
function rlk:boss/tachy/core/dash/probe
scoreboard players operation #k_dl tk = #t2 tk
execute positioned as @e[type=minecraft:marker,tag=rlk_tk_dp,limit=1] run function rlk:mboss/mv/glide {t:4}
kill @e[type=minecraft:marker,tag=rlk_tk_dp]
data modify storage rlk:tk core.dl set value {len:0,w:18,tell:1,dmg:135}
execute store result storage rlk:tk core.dl.len int 5 run scoreboard players get #k_dl tk
scoreboard players set #hzAct mb 4
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players operation #hzEl mb = #el tk
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line with storage rlk:tk core.dl
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/tachy/core/hz_tag/k
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_tk_dl
