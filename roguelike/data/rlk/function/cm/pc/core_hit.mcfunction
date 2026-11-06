# combat/apply hook (@s = this brain, while rlk_c3_core): the exposed core takes x1.5 from every hit
scoreboard players operation #dmg tmp *= #3 tmp
scoreboard players operation #dmg tmp /= #2 tmp
particle minecraft:crit ~ ~1.5 ~ 0.25 0.25 0.25 0.3 8
playsound minecraft:block.amethyst_block.hit master @a ~ ~ ~ 0.6 0.7
