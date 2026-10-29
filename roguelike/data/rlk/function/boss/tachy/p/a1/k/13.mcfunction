# A1 pattern tick 13
function rlk:mboss/mv/dist
scoreboard players operation #t tk = #mbDist mb
scoreboard players remove #t tk 20
scoreboard players operation #t tk /= #c5 tk
execute if score #t tk matches ..-1 run scoreboard players set #t tk 0
execute if score #t tk matches 25.. run scoreboard players set #t tk 24
function rlk:boss/tachy/core/dash/probe
scoreboard players operation #a1_dl tk = #t2 tk
execute positioned as @e[type=minecraft:marker,tag=rlk_tk_dp,limit=1] run function rlk:mboss/mv/glide {t:6}
kill @e[type=minecraft:marker,tag=rlk_tk_dp]
function rlk:mboss/grp_new
data modify storage rlk:tk core.dl set value {len:0,w:16,tell:1,dmg:100}
execute store result storage rlk:tk core.dl.len int 5 run scoreboard players get #a1_dl tk
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 6
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
scoreboard players operation #hzEl mb = #el tk
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line with storage rlk:tk core.dl
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/tachy/core/hz_tag/a1
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_tk_dl
