# As the boss. Not found in time: no punishment strike, she simply reforms.
scoreboard players set #rdIlStep rd 3
scoreboard players set #rdIlClock rd 0
tag @e[tag=rlk_rd_ilact] remove rlk_rd_ilact
execute as @e[tag=rlk_rd_illusion,scores={rdReal=0}] at @s run function rlk:boss/raiden/illusion/dissolve
# The body reforms on the real illusion's spot (or stays at the centre without one).
execute as @e[tag=rlk_rd_illusion,scores={rdReal=1},limit=1] at @s run tp @e[tag=rlk_raiden,limit=1] ~ ~ ~
execute as @e[tag=rlk_rd_illusion,scores={rdReal=1}] at @s run function rlk:boss/raiden/illusion/vanish
execute at @s run function rlk:boss/raiden/illusion/reform
playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~ ~ 0.8 0.7 0.2
