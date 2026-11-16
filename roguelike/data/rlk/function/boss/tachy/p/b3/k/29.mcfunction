# B3 pattern tick 29
function rlk:mboss/mv/face
function rlk:mboss/mv/dist
scoreboard players operation #t tk = #mbDist mb
scoreboard players remove #t tk 25
scoreboard players operation #t tk /= #c5 tk
execute if score #t tk matches ..-1 run scoreboard players set #t tk 0
execute if score #t tk matches 25.. run scoreboard players set #t tk 24
function rlk:boss/tachy/core/dash/probe
scoreboard players operation #b3_dl tk = #t2 tk
execute positioned as @e[type=minecraft:marker,tag=rlk_tk_dp,limit=1] run function rlk:mboss/mv/glide {t:10}
kill @e[type=minecraft:marker,tag=rlk_tk_dp]
