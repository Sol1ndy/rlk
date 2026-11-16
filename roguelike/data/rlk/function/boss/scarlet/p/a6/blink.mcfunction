# A6 blink (@s = the body, tick 0): probe 12 b straight back from the player, else 8-10 b to the left / right; glide there in 3 t.
scoreboard players set #t hr 24
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 run function rlk:boss/scarlet/core/dash/probe
scoreboard players operation #a6_n hr = #t2 hr
execute if score #a6_n hr matches 16.. run return run function rlk:boss/scarlet/p/a6/go
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
scoreboard players set #t hr 20
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~90 0 run function rlk:boss/scarlet/core/dash/probe
execute if score #t2 hr matches 16.. run return run function rlk:boss/scarlet/p/a6/go
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~-90 0 run function rlk:boss/scarlet/core/dash/probe
execute if score #t2 hr matches 16.. run return run function rlk:boss/scarlet/p/a6/go
kill @e[type=minecraft:marker,tag=rlk_hr_dp]
scoreboard players set #t hr 24
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 run function rlk:boss/scarlet/core/dash/probe
function rlk:boss/scarlet/p/a6/go
