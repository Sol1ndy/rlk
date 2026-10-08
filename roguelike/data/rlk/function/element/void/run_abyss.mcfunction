# 심연: 주변 적을 끌어당기고 물 범위 피해
tag @s add rlk_rnc
execute as @e[tag=rlk_mob,tag=!rlk_rnc,tag=!boss,distance=..3.5] at @s run function rlk:element/void/pull
tag @s remove rlk_rnc
particle minecraft:bubble_pop ~ ~1 ~ 1.4 0.4 1.4 0.05 40
particle minecraft:splash ~ ~1 ~ 1.4 0.4 1.4 0.2 50
particle minecraft:dust{color:[0.25,0.35,0.95],scale:1.4} ~ ~0.6 ~ 1.5 0.2 1.5 0 30
particle minecraft:dust{color:[0.88,0.12,0.22],scale:1.2} ~ ~0.6 ~ 0.8 0.2 0.8 0 15
playsound minecraft:entity.player.splash.high_speed master @a ~ ~ ~ 0.8 0.6
playsound minecraft:block.conduit.deactivate master @a ~ ~ ~ 0.6 1.2
scoreboard players set #qU tmp 0
execute as @e[tag=rlk_mob,distance=..3.5] at @s run function rlk:element/aoe_hit
