scoreboard players operation #t1 tmp = @s cmVx
scoreboard players operation #t1 tmp /= #3 tmp
scoreboard players operation @s cmPx += #t1 tmp
scoreboard players operation #t1 tmp = @s cmVy
scoreboard players operation #t1 tmp /= #3 tmp
scoreboard players operation @s cmPy += #t1 tmp
scoreboard players operation #t1 tmp = @s cmVz
scoreboard players operation #t1 tmp /= #3 tmp
scoreboard players operation @s cmPz += #t1 tmp
execute store result entity @s Pos[0] double 0.001 run scoreboard players get @s cmPx
execute store result entity @s Pos[1] double 0.001 run scoreboard players get @s cmPy
execute store result entity @s Pos[2] double 0.001 run scoreboard players get @s cmPz
scoreboard players set #pj tmp 0
execute at @s unless block ~ ~ ~ #rlk:cm_pass run scoreboard players set #pj tmp 2
execute at @s positioned ~-0.65 ~-0.65 ~-0.65 as @e[tag=rlk_body,dx=0,dy=0,dz=0] positioned ~0.3 ~0.3 ~0.3 if entity @s[dx=0,dy=0,dz=0] run scoreboard players set #pj tmp 1
execute if score #pj tmp matches 1.. at @s run return run function rlk:cm/pj/cb_boom
scoreboard players remove #pst tmp 1
execute if score #pst tmp matches 1.. run function rlk:cm/pj/cb_step
