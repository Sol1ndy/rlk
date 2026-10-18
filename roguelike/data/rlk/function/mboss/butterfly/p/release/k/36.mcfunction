# release clock 36
# the ground flash: a lime mist cone from the floor at R
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] run function rlk:mboss/butterfly/fx/p/rel_ground_flash
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] run particle minecraft:dust{color:[0.827f,0.941f,0.722f],scale:1.4} ~ ~1.5 ~ 0.6 1.5 0.6 0 20 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] run particle minecraft:flash{color:[0.93,0.98,0.86,0.8]} ~ ~0.5 ~ 0 0 0 0 1 force @a[tag=player]
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.7 1 0.23
