# 개화 폭발: 반경 4칸 풀 피해 200%
particle minecraft:item{item:{id:"minecraft:slime_ball"}} ~ ~0.3 ~ 0.8 0.5 0.8 0.15 40
playsound minecraft:block.slime_block.break master @a ~ ~ ~ 0.9 0.8
scoreboard players operation #qDmg tmp = @s rxDmg
scoreboard players set #qEl tmp 7
scoreboard players set #qU tmp 0
execute as @e[tag=rlk_mob,distance=..4] at @s run function rlk:element/aoe_hit
kill @s
