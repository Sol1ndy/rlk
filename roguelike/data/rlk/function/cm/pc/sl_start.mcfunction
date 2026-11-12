scoreboard players set @s cmS 3
scoreboard players set @s cmT 14
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute store result score @s cmYaw run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100
tag @s add rlk_c2_fix
playsound minecraft:block.beacon.power_select master @a ~ ~ ~ 0.9 0.7
playsound minecraft:entity.iron_golem.repair master @a ~ ~ ~ 0.8 0.6
