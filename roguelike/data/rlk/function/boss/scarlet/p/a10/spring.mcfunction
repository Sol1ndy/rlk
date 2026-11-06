# A10 spring (@s = the body, tick 2): up 5 b in 6 t, drifting <= 2.4 b toward the player.
function rlk:mboss/mv/dist
scoreboard players operation #t hr = #mbDist mb
scoreboard players remove #t hr 15
scoreboard players operation #t hr /= #c5 hr
execute if score #t hr matches ..-1 run scoreboard players set #t hr 0
execute if score #t hr matches 5.. run scoreboard players set #t hr 4
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/scarlet/core/dash/probe
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] positioned ~ 206.0 ~ run function rlk:mboss/mv/glide {t:6}
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
