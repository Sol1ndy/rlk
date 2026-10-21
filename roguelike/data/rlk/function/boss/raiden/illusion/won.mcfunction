# As the shattered REAL clone at its spot (object/break, before it is removed).
scoreboard players set #rdIlStep rd 4
# Slashes that have not launched yet go with their displays.
execute as @e[tag=rlk_rd_ilhaz] if score @s rdHAge < @s rdWind run function rlk:boss/raiden/hazard/expire
execute as @e[tag=rlk_rd_illusion,scores={rdReal=0}] at @s run function rlk:boss/raiden/illusion/dissolve
tp @e[tag=rlk_raiden,limit=1] ~ ~ ~
execute as @e[tag=rlk_raiden,limit=1] at @s run function rlk:boss/raiden/illusion/found
