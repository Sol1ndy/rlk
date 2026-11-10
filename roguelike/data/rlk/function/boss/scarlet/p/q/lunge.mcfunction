# Q ghost lunge (@s = the body, tick 16): along the locked aim to 1.6 b before the player, at most 14 b (probe,
# mv/ok), in 4 t.
function rlk:mboss/mv/dist
scoreboard players operation #t hr = #mbDist mb
scoreboard players remove #t hr 16
scoreboard players operation #t hr /= #c5 hr
execute if score #t hr matches ..-1 run scoreboard players set #t hr 0
execute if score #t hr matches 29.. run scoreboard players set #t hr 28
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/core/dash/probe
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] run function rlk:mboss/mv/glide {t:4}
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
