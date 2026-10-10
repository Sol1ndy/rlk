scoreboard players operation #t1 tmp = #svx tmp
scoreboard players operation #t1 tmp /= #3 tmp
scoreboard players operation #sx tmp += #t1 tmp
scoreboard players operation #t1 tmp = #svy tmp
scoreboard players operation #t1 tmp /= #3 tmp
scoreboard players operation #sy tmp += #t1 tmp
scoreboard players operation #t1 tmp = #svz tmp
scoreboard players operation #t1 tmp /= #3 tmp
scoreboard players operation #sz tmp += #t1 tmp
execute store result entity @s Pos[0] double 0.001 run scoreboard players get #sx tmp
execute store result entity @s Pos[1] double 0.001 run scoreboard players get #sy tmp
execute store result entity @s Pos[2] double 0.001 run scoreboard players get #sz tmp
execute at @s unless block ~ ~ ~ #rlk:cm_pass run return run function rlk:cm/cn/sim_hit
scoreboard players remove #pst tmp 1
execute if score #pst tmp matches 1.. run function rlk:cm/cn/sim_s
