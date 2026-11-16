# P2 cut (any executor; selectors): markers, a leap in the air (the body back on the floor), the jump proxy state
# (not while dying: the framework set the proxies dead). A kit front ring already drawn runs out by itself (<= 9 t,
# like the front preset; pause / death / test cut clear the kit telegraphs; wire F5 allows no tele/wave_end).
kill @e[tag=rlk_mb_az_p2]
execute if score #azLeap mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:mboss/mv/stop
execute if score #azLeap mb matches 1 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run tp @s ~ 201 ~
execute if score #azPx mb matches 1 unless score #mbSt mb matches 2 run function rlk:boss/azhdaha/px/normal
scoreboard players set #azLeap mb 0
