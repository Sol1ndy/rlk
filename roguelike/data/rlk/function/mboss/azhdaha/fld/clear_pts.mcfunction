# @s = the new field's centre marker (pattern fields only): never within r + 1.5 of the head-front point or the
# tail-lane point; pushed radially outward. #azNfR = r + pad (tenths -> the macro distance).
execute store result score #azX mb run data get storage rlk:mboss az.nf.r
scoreboard players add #azX mb 15
execute store result storage rlk:mboss az.cp.d double 0.1 run scoreboard players get #azX mb
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s rotated as @s rotated ~ 0 positioned ^0 ^ ^6.8 run function rlk:mboss/azhdaha/fld/cp_m with storage rlk:mboss az.cp
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s rotated as @s rotated ~ 0 positioned ^0 ^ ^-10.12 run function rlk:mboss/azhdaha/fld/cp_m with storage rlk:mboss az.cp
