# TRI lunge (@s = the body, tick 12): along the locked aim to 1.5 b before the player, at most 6 b (probe, mv/ok),
# in 2 t.
function rlk:mboss/mv/dist
scoreboard players operation #t hr = #mbDist mb
scoreboard players remove #t hr 15
scoreboard players operation #t hr /= #c5 hr
execute if score #t hr matches ..-1 run scoreboard players set #t hr 0
execute if score #t hr matches 13.. run scoreboard players set #t hr 12
execute at @s rotated as @s rotated ~ 0 run function rlk:boss/scarlet/core/dash/probe
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] run function rlk:mboss/mv/glide {t:2}
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
