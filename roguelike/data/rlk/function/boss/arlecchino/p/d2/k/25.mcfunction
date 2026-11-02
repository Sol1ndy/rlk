# D2 pattern tick 25
function rlk:mboss/grp_new
function rlk:mboss/mv/dist
scoreboard players operation #t kn = #mbDist mb
scoreboard players add #t kn 15
scoreboard players operation #t kn /= #c5 kn
execute if score #t kn matches 29.. run scoreboard players set #t kn 28
function rlk:boss/arlecchino/core/dash/probe
scoreboard players operation #d2_dl kn = #t2 kn
execute positioned as @e[type=minecraft:marker,tag=rlk_kn_dp,limit=1] run function rlk:mboss/mv/glide {t:4}
kill @e[type=minecraft:marker,tag=rlk_kn_dp]
data modify storage rlk:kn core.dl set value {len:0,w:20,tell:1,dmg:45}
execute store result storage rlk:kn core.dl.len int 5 run scoreboard players get #d2_dl kn
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzAct mb 4
scoreboard players set #hzEl mb 1
scoreboard players set #hzKB mb 0
scoreboard players set #hzSfx mb 0
scoreboard players set #hzQuiet mb 1
execute at @s rotated as @s rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/hz/line with storage rlk:kn core.dl
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run function rlk:boss/arlecchino/core/hz_tag/d2
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_kn_dl
