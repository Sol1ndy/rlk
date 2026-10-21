# object/break, as the shattered clone at itself (display already removed).
execute unless score #rdIlStep rd matches 1 run return 0
execute if score @s rdReal matches 1 run return run function rlk:boss/raiden/illusion/won
# A shattered fake loses its pending slab.
tag @s remove rlk_rd_illusion
execute as @e[tag=rlk_rd_ilhaz,distance=..0.2] if score @s rdHAge < @s rdWind run function rlk:boss/raiden/hazard/expire
playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~1 ~ 0.7 1.25 0.2
