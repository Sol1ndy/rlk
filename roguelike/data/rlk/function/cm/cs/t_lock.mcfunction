# the last 6 t: the stab line is fixed and drawn on the ground
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute store result score @s cmYaw run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100
tag @s add rlk_c2_fix
playsound minecraft:block.note_block.bit master @a ~ ~ ~ 0.8 1.8
