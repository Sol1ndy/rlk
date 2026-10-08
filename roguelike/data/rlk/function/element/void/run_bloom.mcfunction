# 공허 개화: 붉은 꽃이 피었다 터짐
particle minecraft:cherry_leaves ~ ~1 ~ 0.8 0.5 0.8 0.1 30
particle minecraft:dust{color:[0.95,0.35,0.55],scale:1.4} ~ ~1 ~ 0.9 0.4 0.9 0 25
particle minecraft:dust{color:[0.88,0.12,0.22],scale:1.0} ~ ~1 ~ 0.5 0.3 0.5 0 15
playsound minecraft:block.spore_blossom.break master @a ~ ~ ~ 0.9 0.8
playsound minecraft:block.amethyst_block.resonate master @a ~ ~ ~ 0.6 1.3
scoreboard players set #qU tmp 0
execute as @e[tag=rlk_mob,distance=..2] at @s run function rlk:element/aoe_hit
