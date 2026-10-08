# 서리 파편: 주변 적(가까운 순 5명)에게 하나씩, 남는 파편은 대상 자신에게(밖으로 튀었다가 휘어 돌아온다)
tag @s add rlk_rnc
execute unless score @s rnId matches 1.. run function rlk:element/void/assign_id
scoreboard players set #shN tmp 0
execute as @e[tag=rlk_mob,tag=!rlk_rnc,distance=..6,sort=nearest,limit=5] run function rlk:element/void/sh_other
scoreboard players operation #shTg tmp = @s rnId
function rlk:element/void/sh_rest
tag @s remove rlk_rnc
particle minecraft:snowflake ~ ~1.2 ~ 0.4 0.5 0.4 0.15 30
particle minecraft:block{block_state:"minecraft:packed_ice"} ~ ~1.2 ~ 0.3 0.4 0.3 0.1 20
playsound minecraft:block.glass.break master @a ~ ~ ~ 0.8 0.7
playsound minecraft:block.amethyst_block.break master @a ~ ~ ~ 0.8 1.5
