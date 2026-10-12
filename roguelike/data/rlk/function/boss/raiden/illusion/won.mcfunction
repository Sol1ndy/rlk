# As the shattered REAL illusion at its spot (object/break, before it is removed).
scoreboard players set #rdIlStep rd 4
scoreboard players set #rdIlClock rd 0
tag @e[tag=rlk_rd_ilact] remove rlk_rd_ilact
# Slashes that have not landed yet are cancelled together with their displays.
execute as @e[tag=rlk_rd_ilhaz] if score @s rdHAge < @s rdWind run function rlk:boss/raiden/hazard/expire
execute as @e[tag=rlk_rd_illusion,scores={rdReal=0}] at @s run function rlk:boss/raiden/illusion/dissolve
tp @e[tag=rlk_raiden,limit=1] ~ ~ ~
execute as @e[tag=rlk_raiden,limit=1] at @s run function rlk:boss/raiden/illusion/reform
function rlk:boss/raiden/line/ganpa
playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~1 ~ 0.8 0.9 0.2
playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~1 ~ 1 1.3 0.2
