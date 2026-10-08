# 과부하: 반경 4칸 불 피해 + 살짝 띄움
particle minecraft:explosion ~ ~1 ~ 0.6 0.6 0.6 0 4
particle minecraft:flame ~ ~1 ~ 1.2 0.8 1.2 0.08 40
playsound minecraft:entity.generic.explode master @a ~ ~ ~ 0.7 1.3
scoreboard players set #qU tmp 0
execute as @e[tag=rlk_mob,tag=!boss,distance=..4] run data merge entity @s {Motion:[0.0d,0.42d,0.0d]}
execute as @e[tag=rlk_mob,distance=..4] at @s run function rlk:element/aoe_hit
