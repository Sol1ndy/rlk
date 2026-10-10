# 발화: 반경 4칸 풀 피해 300%
scoreboard players set #rx tmp 13
function rlk:engravings/on_rx
execute positioned ~ ~-1.5 ~ run function rlk:element/rx_text
particle minecraft:flame ~ ~0.5 ~ 1.2 0.8 1.2 0.08 50
particle minecraft:explosion ~ ~0.5 ~ 0.5 0.5 0.5 0 3
execute unless score #k37 snd matches 1 run function rlk:snd/f39
scoreboard players operation #qDmg tmp = @s rxDmg3
scoreboard players set #qEl tmp 7
scoreboard players set #qU tmp 0
execute as @e[tag=rlk_mob,distance=..4] at @s run function rlk:element/aoe_hit
kill @s
