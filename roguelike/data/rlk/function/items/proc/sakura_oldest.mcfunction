scoreboard players set #t1 itv 999999
execute as @e[tag=rlk_sakura] run scoreboard players operation #t1 itv < @s life
execute as @e[tag=rlk_sakura] if score @s life = #t1 itv run kill @s
