scoreboard players operation #rdG rd = @s rdHGrp
execute as @e[tag=rlk_rd_hazard] if score @s rdHGrp = #rdG rd run scoreboard players operation @s rdHHit > @s rdHMax
