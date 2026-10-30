# the landing must be safe ground inside the box and the straight path from the bird to it open (feet + 0.25 / 0.95 / 1.7)
execute at @e[tag=rlk_rv_tsel,limit=1] unless block ~ ~0.1 ~ #rlk:dash_pass run return 0
execute at @e[tag=rlk_rv_tsel,limit=1] unless block ~ ~1.1 ~ #rlk:dash_pass run return 0
execute at @e[tag=rlk_rv_tsel,limit=1] unless block ~ ~1.75 ~ #rlk:dash_pass run return 0
execute at @e[tag=rlk_rv_tsel,limit=1] if block ~ ~-0.3 ~ #rlk:cm_pass run return 0
execute store result score #ox tmp run data get entity @e[tag=rlk_rv_tsel,limit=1] Pos[0] 100
execute store result score #oz tmp run data get entity @e[tag=rlk_rv_tsel,limit=1] Pos[2] 100
execute if score #ox tmp < @s cmAX run return 0
execute if score #ox tmp > @s cmVx run return 0
execute if score #oz tmp < @s cmAZ run return 0
execute if score #oz tmp > @s cmVz run return 0
scoreboard players set #n tmp 96
scoreboard players set #ok tmp 0
execute facing entity @e[tag=rlk_rv_tsel,limit=1] feet run function rlk:cm/rv/ray
execute if score #ok tmp matches 0 run return 0
return 1
