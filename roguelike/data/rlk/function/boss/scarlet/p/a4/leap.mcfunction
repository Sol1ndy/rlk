# A4 leap (@s = the body, tick 2): the floor point <= 10 b toward the player (probe), then a
# straight rise of 3.4 b to above it in 4 t.
function rlk:mboss/mv/dist
scoreboard players operation #t hr = #mbDist mb
scoreboard players remove #t hr 30
scoreboard players operation #t hr /= #c5 hr
execute if score #t hr matches ..-1 run scoreboard players set #t hr 0
execute if score #t hr matches 21.. run scoreboard players set #t hr 20
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/scarlet/core/dash/probe
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_dp,limit=1] positioned ~ 204.4 ~ run function rlk:mboss/mv/glide {t:4}
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
