scoreboard players set @s cmS 3
scoreboard players set @s cmT 40
scoreboard players set @s c2eF 0
execute facing entity @e[tag=rlk_rv_tsel,limit=1] feet rotated ~ 0 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute store result score @s cmYaw run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100
tag @s add rlk_c2_fix
playsound minecraft:entity.phantom.swoop master @a ~ ~ ~ 1 0.8
playsound minecraft:entity.blaze.shoot master @a ~ ~ ~ 0.7 0.7
