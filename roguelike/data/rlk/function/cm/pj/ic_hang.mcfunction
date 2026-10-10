# 주인(얼음 마법사)이 죽었으면 떨어지기 전에 사라짐
scoreboard players operation #oid tmp = @s cmId
scoreboard players set #own tmp 0
execute as @e[tag=rlk_cm_im] if score @s cmId = #oid tmp run scoreboard players set #own tmp 1
execute if score #own tmp matches 0 run return run function rlk:cm/pj/ic_fizzle
scoreboard players remove @s cmT 1
particle minecraft:snowflake ~ ~0.3 ~ 0.15 0.1 0.15 0 1
